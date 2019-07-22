"""
   @copyright: 2018-2019 by Pauli Rikula <pauli.rikula@gmail.com>
   @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""

from .naming import Naming, ContainerNaming, TypeDescriptor
from .namedproperty import NamedProperty, PropertyList, Module

class ProtobufScalars:
    """
    >>> list(filter(lambda x: x.find('__') == -1, dir(ProtobufScalars)))
    ['bool', 'bytes', 'double', 'fixed32', 'fixed64', 'float', 'int32', 'int64', 'sfixed32', 'sfixed64', 'sint32', 'sint64', 'string', 'uint32', 'uint64']

    >>> getattr(ProtobufScalars, "float")
    {"type": "float"}

    """

    double = TypeDescriptor(class_name="double")
    float = TypeDescriptor(class_name="float")	
    int32 = TypeDescriptor(class_name="int32")	
    int64 = TypeDescriptor(class_name="int64")	
    uint32 = TypeDescriptor(class_name="uint32")	
    uint64 = TypeDescriptor(class_name="uint64")	
    sint32 = TypeDescriptor(class_name="sint32")	
    sint64 = TypeDescriptor(class_name="sint64")
    fixed32 = TypeDescriptor(class_name="fixed32")	
    fixed64 = TypeDescriptor(class_name="fixed64")	
    sfixed32 = TypeDescriptor(class_name="sfixed32")
    sfixed64 = TypeDescriptor(class_name="sfixed64")
    bool = TypeDescriptor(class_name="bool")
    string = TypeDescriptor(class_name="string")	
    bytes = TypeDescriptor(class_name="bytes")

# this is a mess. needs improved pattern mathing capabilities
def is_value_property(property_definition):
    for sub_property_naming in property_definition.properties:
        if type(sub_property_naming) == TypeDescriptor:
            return True
    return False

# this is a mess. needs improved pattern mathing capabilities
def get_value_property_type(property_definition):
    for sub_property_naming in property_definition.properties:
        if type(sub_property_naming) == TypeDescriptor:
            return sub_property_naming
    return None

class ProtobufGenerator:
    @staticmethod
    def get_property_file_content(module: Module) -> str:
        
        file_content =  ['syntax = "proto2";']

        if module.module_name != None:
            file_content.append('package {};'.format(module.module_name))
        
        sub_modules = set()
        for named_property in module.properties:
            property_definition = module.get_named_property(named_property.class_name)
            if property_definition:
                for sub_property_naming in property_definition.properties:
                    if sub_property_naming.module_name is not None:
                        sub_modules.add(sub_property_naming.module_name)
        sub_modules = sorted(list(sub_modules))
        for sub_module in sub_modules:
            if sub_module != module.module_name:
                file_content.append('import {};'.format(sub_module))

            
        # this is a mess. needs improved pattern mathing capabilities
        for named_property in module.properties:
            if type(named_property) == Naming:
                property_definition = module.get_named_property(named_property.class_name)
                
                if property_definition:
                    if is_value_property(property_definition):
                        continue

                    file_content.append('message {} {{'.format(named_property.moduleless_class_name))
                    for i, sub_property_naming in enumerate(property_definition.properties):
                        sub_property_definition = module.get_named_property(sub_property_naming.class_name)
                        if sub_property_definition is not None:                                
                            if is_value_property(sub_property_definition):
                                value_type = get_value_property_type(sub_property_definition)

                                type_name = sub_property_naming.class_name
                                if sub_property_naming.module_name == module.module_name:
                                    type_name = sub_property_naming.moduleless_class_name
                                
                                file_content.append('    required {} {} = {};'.format(
                                    value_type.class_name,
                                    sub_property_naming.value_name,
                                    i+1))

                            else:
                                type_name = sub_property_naming.moduleless_class_name
                                
                                file_content.append('    required {} {} = {};'.format(
                                    type_name,
                                    sub_property_naming.value_name,
                                    i+1))
                    file_content.append('}')
                
            elif type(named_property) == ContainerNaming:
                property_definition = module.get_named_property(named_property.class_name)
                file_content.append('message {} {{'.format(named_property.moduleless_class_name))
                sub_property_naming = property_definition.properties[0]
                sub_property_definition = module.get_named_property(sub_property_naming.class_name)
                if is_value_property(sub_property_definition):
                    value_type = get_value_property_type(sub_property_definition)

                    file_content.append('    repeated {} {} = 1;'.format(
                        value_type.class_name,
                        sub_property_naming.plural_value_name))
                else:
                    type_name = sub_property_naming.moduleless_class_name
                    
                    file_content.append('    repeated {} {} = 1;'.format(
                        type_name,
                        sub_property_naming.plural_value_name))
                file_content.append('}')
        
        return "\n".join(file_content)
        
