"""
   @copyright: 2018-2019 by Pauli Rikula <pauli.rikula@gmail.com>
   @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""

from abc import abstractmethod, ABCMeta
import types

from .naming import Naming, ContainerNaming
from .namedproperty import NamedProperty, PropertyList



# TODO: wtf is python's description protocol?
class InterfaceGenerator:
    @staticmethod
    def get_class_template(naming: Naming):
        """
        >>> InterfaceGenerator.get_class_template(Naming("distance")) == InterfaceGenerator.get_class_template(Naming("distance"))
        False

        >>> t = InterfaceGenerator.get_class_template(Naming("distance"))
        >>> t.__name__
        'IDistance'

        """

        class ClassTemplate(metaclass=ABCMeta):
            pass
        ClassTemplate.__name__ = naming.interface_name
        ClassTemplate.__qualname__ = naming.interface_name
        return ClassTemplate

    @staticmethod
    def generate_abstract_class(class_naming: NamedProperty):
        """
        >>> cl = PropertyList()
        >>> cl.add(Naming("distance"))
        >>> cl.add(Naming("duration"))
        >>> c = NamedProperty(Naming("speed"), cl)
        >>> ISpeed = InterfaceGenerator.generate_abstract_class(c)
        >>> import types
        >>> class Speed(ISpeed, types.SimpleNamespace):
        ...     def __init__(self, distance, duration):
        ...         super().__init__(distance=distance, duration=duration)
        >>> s = Speed(1,2)
        >>> s
        Speed(distance=1, duration=2)
        >>> class Speed(ISpeed):
        ...  def __init__(self):
        ...    super().__init__()
        >>> s = Speed()
        Traceback (most recent call last):
        ...
        TypeError: Can't instantiate abstract class Speed with abstract methods distance, duration

        """
        template = InterfaceGenerator.get_class_template(class_naming.naming)
        getters = set()

        for sub_property_naming in class_naming.properties:
            getters.add(sub_property_naming.value_name)

            def getter(self):
                raise NotImplementedError("Getter for property {} is not impplemented".format(
                    sub_property_naming.value_name))
            getter.__name__ = sub_property_naming.value_name
            getter = abstractmethod(getter)

            setattr(template, sub_property_naming.value_name, getter)
            doc_str = "The {} of the {} instance.".format(
                sub_property_naming.docstring_name, class_naming.naming.docstring_name)

            p = property(fget=getter, doc=doc_str)

            setattr(template, sub_property_naming.value_name, p)

        template.__abstractmethods__ = frozenset(getters)

        return template
    
    @staticmethod
    def generate_abstract_container(class_naming: NamedProperty, item_naming: Naming):
        template = InterfaceGenerator.get_class_template(class_naming.naming)

        items_name = str(item_naming.plural_value_name)

        def getter(self):
            raise NotImplementedError("Getter for property {} is not impplemented".format(
                items_name))
        getter.__name__ = items_name
        getter = abstractmethod(getter)

        doc_str = "Returns all contained {} of the {} instance.".format(
                item_naming.docstring_name, class_naming.naming.docstring_name)
        setattr(template, items_name, getter)

        p = property(fget=getter, doc=doc_str)

        setattr(template, items_name, p)

        template.__abstractmethods__ = frozenset([items_name])

        #print(template.knives)
        return template
