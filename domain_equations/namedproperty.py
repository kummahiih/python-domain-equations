"""
   @copyright: 2018-2019 by Pauli Rikula <pauli.rikula@gmail.com>
   @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""

from .naming import Naming, ContainerNaming, TypeDescriptor

class PropertyList:
    """
    >>> c = PropertyList()
    >>> c.add(Naming("foo_bar"))
    >>> c.add(Naming("bar"))
    >>> c.add(Naming("foo"))
    >>> c.add(Naming("foo"))
    >>> c
    ["Bar", "Foo", "FooBar"]
    
    >>> import copy
    >>> c == copy.copy(c)
    True

    """
    def __init__(self):
        self._properties = set()

    def add(self, naming: TypeDescriptor):
        """
        Add naming component
        """
        if not isinstance(naming, TypeDescriptor):
            raise ValueError("name should be type of TypeDescriptor")
        self._properties.add(naming)

    @property
    def properties(self):
        """
        The naming components in sorted list
        """
        property_list = list(self._properties)
        property_list.sort(key=lambda c: c.class_name)
        return property_list

    def __eq__(self, other):
        return isinstance(other, PropertyList) and \
            self.properties == other.properties

    def __str__(self) -> str:
        return "[{}]".format(
            ", ".join(
                map(
                    lambda c: '"{}"'.format(c.class_name),
                    self.properties)))

    def __repr__(self):
        return str(self)


class NamedProperty:
    """
    >>> cl = PropertyList()
    >>> cl.add(Naming("distance"))
    >>> duration = Naming("duration")
    >>> cl.add(duration)
    >>> c = NamedProperty(Naming("speed"), cl)
    >>> c
    {"naming": {"type": "Speed", "value": "speed", "plural": "speeds", "docstring": "speed"}, "properties": ["Distance", "Duration"]}
    >>> d = NamedProperty(Naming("speed"), None)
    >>> d
    {"naming": {"type": "Speed", "value": "speed", "plural": "speeds", "docstring": "speed"}}

    >>> c == NamedProperty(Naming("speed"), cl)
    True

    >>> c == NamedProperty(Naming("foo"), cl)
    False

    >>> dl = PropertyList()
    >>> dl.add(TypeDescriptor(class_name = "float"))
    >>> duration_property = NamedProperty(duration, dl)
    >>> duration_property
    {"naming": {"type": "Duration", "value": "duration", "plural": "durations", "docstring": "duration"}, "properties": ["float"]}

    """

    def __init__(self, naming: Naming, property_list: PropertyList):
        if not isinstance(naming, Naming):
            raise ValueError()
        if not isinstance(property_list, PropertyList) and property_list is not None:
            raise ValueError()
        self._naming = naming
        self._property_list = property_list

    @property
    def naming(self):
        return self._naming

    @property
    def properties(self):
        if self._property_list is None:
            return []
        return self._property_list.properties

    def __str__(self) -> str:
        if self._property_list is None:
            return '{{"naming": {}}}'.format(self.naming)

        return '{{"naming": {}, "properties": {}}}'.format(
            self.naming,
            self._property_list)

    def __eq__(self, other):
        return isinstance(other, NamedProperty) and \
            self.naming == other.naming and \
            self.properties == other.properties

    def __repr__(self):
        return str(self)

class Module:
    def __init__(self, module_name:str, property_list, used_named_properties):
        """
        >>> cl = PropertyList()
        >>> distance = Naming("distance", module_name="measure")
        >>> cl.add(distance)
        >>> duration = Naming("duration", module_name="measure")
        >>> cl.add(duration)
        >>> c = NamedProperty(Naming("speed", module_name="measure"), cl)
        >>> types_in_module = PropertyList()
        >>> types_in_module.add(distance)
        >>> types_in_module.add(duration)
        >>> types_in_module.add(c.naming)

        >>> m1 = Module('measure', types_in_module, [c])
        >>> m1
        {"module": measure, "types": ["measure.Distance", "measure.Duration", "measure.Speed"]}

        >>> import copy
        >>> m2 = Module('measure', copy.copy(types_in_module), [c])
        >>> m2 == m1
        True


        """
        if not isinstance(module_name, str):
            raise ValueError()
        if not isinstance(property_list, PropertyList) and property_list is not None:
            raise ValueError()

        self._module_name = module_name
        self._property_list = property_list

        self._named_propertie_by_name = dict([(i.naming.class_name, i) for i in used_named_properties])
    
    def __str__(self) -> str:
        if self._property_list is None:
            return '{{"module": {}}}'.format(self._module_name)

        return '{{"module": {}, "types": {}}}'.format(
            self._module_name,
            self._property_list)
    
    def get_named_property(self, class_name):
        return self._named_propertie_by_name.get(class_name, None)

    @property
    def module_name(self):
        return self._module_name

    def __eq__(self, other):
        return isinstance(other, Module) and \
            self.module_name == other.module_name and \
            self.properties == other.properties
    
    @property
    def properties(self):
        if self._property_list is None:
            return []
        return self._property_list.properties

    def __repr__(self):
        return str(self)
