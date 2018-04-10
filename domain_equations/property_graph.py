"""
   @copyright: 2018 by Pauli Rikula <pauli.rikula@gmail.com>
   @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""

import re
import abc
import types
import copy

from category_equations import from_operator, get_topmost_tail_products



class Naming:
    """
    Representation of type and variable naming
    """
    def __init__(self, name: str):
        """
        >>> Naming("foo_bar")
        {"type": "FooBar", "value": "foo_bar", "docstring": "foo bar"}
        """
        if not isinstance(name, str) or not re.match(r'[a-z][a-z_]*', name):
            raise ValueError("name should be a non empty lowercase string matching [a-z][a-z_]*")
        self._value_name = name
        self._class_name = Naming.camel_case(name)
        self._components = set()

    @property
    def value_name(self) -> str:
        """
        Name for values
        """
        return self._value_name
    
    @property
    def docstring_name(self) -> str:
        """
        Name for docstring
        """
        return self._value_name.replace('_', ' ')

    @property
    def class_name(self) -> str:
        """
        Name for class
        """
        return self._class_name
    
    @property
    def interface_name(self) -> str:
        """
        Name for class
        """
        return "I" + self._class_name

    def __eq__(self, other):
        return isinstance(other, Naming) and \
            self.value_name == other.value_name

    def __hash__(self):
        return self.value_name.__hash__()

    def __str__(self)  -> str:
        return '{{"type": "{}", "value": "{}", "docstring": "{}"}}'.format(self.class_name, self.value_name, self.docstring_name)

    def __repr__(self):
        return str(self)
        
    @staticmethod
    def camel_case(word: str):
        """
        >>> Naming.camel_case("some_words")
        'SomeWords'
        """

        return "".join(map(Naming.capitalize, word.split("_")))

    @staticmethod
    def capitalize(word: str):
        """
        >>> Naming.capitalize("")
        ''

        >>> Naming.capitalize("foo")
        'Foo'
        """
        if word == "":
            return word
        return word[0].upper() + word[1:]


class PropertyList:
    """
    >>> c = PropertyList()
    >>> c.add(Naming("foo_bar"))
    >>> c.add(Naming("bar"))
    >>> c.add(Naming("foo"))
    >>> c.add(Naming("foo"))
    >>> c
    ["Bar", "Foo", "FooBar"]
    
    >>> c == copy.copy(c)
    True

    """
    def __init__(self):
        self._properties = set()

    def add(self, naming: Naming):
        """
        Add naming component
        """
        if not isinstance(naming, Naming):
            raise ValueError("name should be type of Naming")
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
    >>> cl.add(Naming("duration"))
    >>> c = NamedProperty(Naming("speed"), cl)
    >>> c
    {"naming": {"type": "Speed", "value": "speed", "docstring": "speed"}, "properties": ["Distance", "Duration"]}
    >>> d = NamedProperty(Naming("speed"), None)
    >>> d
    {"naming": {"type": "Speed", "value": "speed", "docstring": "speed"}}

    >>> c == NamedProperty(Naming("speed"), cl)
    True

    >>> c == NamedProperty(Naming("foo"), cl)
    False

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

        class ClassTemplate(metaclass=abc.ABCMeta):
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
            getter = abc.abstractmethod(getter)

            setattr(template, sub_property_naming.value_name, getter)
            doc_str = "The {} of the {} instance.".format(
                sub_property_naming.docstring_name, class_naming.naming.docstring_name)

            p = property(fget=getter, doc=doc_str)

            setattr(template, sub_property_naming.value_name, p)

        template.__abstractmethods__ = frozenset(getters)

        return template

# TODO: get rid of the callback -thing

class PropertyGraph:
    """Generate and represent domain model classes via category-like equations
which can be simplified to get the optimal class structure for the modeled domain.

## Rationale

If you have a problem, it sometime helps if you formulate the problem in a new perspective.

The PropertyGraph -class can be used to domain model class structure modeling and generation.
The trick here is to transform the problem to category-like equations which
can be simplified to get the optimal class structure for the modeled domain.

More details of the equation system can be found from the site: https://github.com/kummahiih/python-category-equations

As shown on the end of the next section this notation might also allow you to develope your domain model while coding with less 
refactoring.

## Usage

To model your domain, create a property graph:

    >>> g  = PropertyGraph()

Please note that the I, O and C here are for the property graph instance g:

    >>> I, O, C = g.I, g.O, g.C

For example to measure speed you have to get interval and distance. First you have to define
the used properties by using the wrapper class C:

    >>> speed = C('speed')
    >>> distance = C('distance')
    >>> duration = C('duration')

You can represent the need of something with the operator '*' and then
have the properties set into the graph g like this:

    >>> for i in g.get_properties_from( speed*(distance+duration) ):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "docstring": "duration"}}
    {"naming": {"type": "Speed", "value": "speed", "docstring": "speed"}, "properties": ["Distance", "Duration"]}


    >>> for i in g.properties:
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "docstring": "duration"}}
    {"naming": {"type": "Speed", "value": "speed", "docstring": "speed"}, "properties": ["Distance", "Duration"]}

For fines you have to know (at least in Finland) also:

    >>> fine = C('fine')
    >>> monthly_income =  C('monthly_income')
    >>> speed_limit =  C('speed_limit')
    >>> first_model = O * (speed*(distance + duration) + fine*(speed + monthly_income + speed_limit)) * O
    >>> for i in g.get_properties_from(first_model):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "docstring": "duration"}}
    {"naming": {"type": "Fine", "value": "fine", "docstring": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income", "docstring": "monthly income"}}
    {"naming": {"type": "Speed", "value": "speed", "docstring": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit", "docstring": "speed limit"}}

Because these equations are the same (note the usage of the O at the begin and end)

    >>> simplified_model =  O *  fine*(speed*(distance + duration)*O + monthly_income + speed_limit) * O
    >>> first_model == simplified_model
    True

also the generated properties are the same:

    >>> for i in g.get_properties_from(simplified_model):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "docstring": "duration"}}
    {"naming": {"type": "Fine", "value": "fine", "docstring": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income", "docstring": "monthly income"}}
    {"naming": {"type": "Speed", "value": "speed", "docstring": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit", "docstring": "speed limit"}}

Nice and simple, but then the reality starts to kick in and you have to model the real thing where you have for example
different rules for small fines which do not need monthly income:

    >>> small_fine = C("small_fine")
    >>> second_model =O*(fine* (speed*(distance + duration)*O + monthly_income + speed_limit) + small_fine*(speed + speed_limit))*O
    >>> for i in g.get_properties_from(second_model):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "docstring": "duration"}}
    {"naming": {"type": "Fine", "value": "fine", "docstring": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income", "docstring": "monthly income"}}
    {"naming": {"type": "SmallFine", "value": "small_fine", "docstring": "small fine"}, "properties": ["Speed", "SpeedLimit"]}
    {"naming": {"type": "Speed", "value": "speed", "docstring": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit", "docstring": "speed limit"}}

Here one could create an intermediate class and use it as a member on both fines or inherit the small fine and fine from the same base class.
If you write it by using the provided equation system, it looks like this:
    
    >>> second_model_simplified = O * (fine* ( I + monthly_income*O ) + small_fine)*(speed + speed_limit*O)*(distance + duration) * O
    >>> second_model_simplified == second_model
    True

In other words: if you manage to minimize the equation by finding the common divisors, you can get the optimal class composition
structure from it.

In case you are wondering how to spot the potential intermediate constructs from the model equation, the trick is to search for the
product terms which end to the terminator O:

    >>> for term in g.extract_intermediate_terms(second_model_simplified):
    ...   print(term)
    (((C(speed)) + ((C(speed_limit)) * (O))) * ((C(distance)) + (C(duration)))) * (O)
    ((C(distance)) + (C(duration))) * (O)

And of course it is possible to generate abstract class definitions from the model:

    >>> interfaces = g.get_abstract_classes()
    >>> interfaces
    namespace(IDistance=<class '__main__.IDistance'>, IDuration=<class '__main__.IDuration'>, IFine=<class '__main__.IFine'>, IMonthlyIncome=<class '__main__.IMonthlyIncome'>, ISmallFine=<class '__main__.ISmallFine'>, ISpeed=<class '__main__.ISpeed'>, ISpeedLimit=<class '__main__.ISpeedLimit'>)

And if you inherit em, they work as abstract classes should:

    >>> class Fine(interfaces.IFine): pass
    >>> f = Fine()
    Traceback (most recent call last):
    ...
    TypeError: Can't instantiate abstract class Fine with abstract methods monthly_income, speed, speed_limit


The nice thing with these unoptimized abstact classes  is, that they do not change as long as the modeling equation wont change. In other words:

    >>> second_model_simplified == second_model
    True
    
means that these behave in similar way:

    >>> _ = g.get_properties_from(second_model_simplified)
    >>> interfaces = g.get_abstract_classes()
    >>> class Fine(interfaces.IFine): pass
    >>> f = Fine()
    Traceback (most recent call last):
    ...
    TypeError: Can't instantiate abstract class Fine with abstract methods monthly_income, speed, speed_limit


When you dont yet know your domain model well, with this you could write your code first and clean the 
inheritance or composition arrangements later without changing a bit from the abstract classes you actually use.

    """

    def __init__(self):
        self.clear()
        self.I, self.O, self.C = from_operator(self._connect)


    def clear(self):
        """
        Clear the defined properties
        """
        self.properties_by_value_name = {}
        self.namings_by_value_name = {}

    @property
    def properties(self):
        """
        Creates the defined properties (iterator)
        """
        keys = list(self.namings_by_value_name.keys())
        keys.sort()
        for value_name in keys:
            naming = self.namings_by_value_name[value_name]
            properties = self.properties_by_value_name.get(value_name, None)
            yield NamedProperty(naming, properties)

    def get_properties_from(self, term):
        """
        Get the properties from the given term which has been done using the wrapper
        provided on the same class instance
        """
        self.clear()
        (self.O * term * self.O).evaluate()
        yield from self.properties

    def extract_intermediate_terms(self, term):
        for intermediate_term in get_topmost_tail_products(term):
            if not intermediate_term in [term, self.O, self.I]:
                if self.O * intermediate_term != term:
                    yield  intermediate_term
                

    def _update_naming(self, name):
        naming = Naming(name)
        found = self.namings_by_value_name.get(naming.value_name, None)

        if found is None:
            self.namings_by_value_name[naming.value_name] = naming

    def _connect(self, source_name: str, sink_name: str):
        self._update_naming(source_name)
        source = self.namings_by_value_name.get(source_name)

        self._update_naming(sink_name)
        sink = self.namings_by_value_name.get(sink_name)

        component_list = self.properties_by_value_name.get(
            source.value_name,
            PropertyList())

        component_list.add(sink)
        self.properties_by_value_name[source.value_name] = component_list


    def get_abstract_classes(self):
        """
        Generate abstract class definitions for the defined properties
        """
        types_dict = dict()
        for class_definition in self.properties:
            types_dict[class_definition.naming.interface_name] = InterfaceGenerator.generate_abstract_class(class_definition)
        return types.SimpleNamespace(**types_dict)



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    