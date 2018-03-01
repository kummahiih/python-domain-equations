"""
   @copyright: 2018 by Pauli Rikula <pauli.rikula@gmail.com>
   @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""

from category_equations import from_operator
import re


class _StringOperations:
    @staticmethod
    def camel_case(word: str):
        """
        >>> _StringOperations.camel_case("some_words")
        'SomeWords'
        """

        return "".join(map(_StringOperations.capitalize, word.split("_")))

    @staticmethod
    def capitalize(word: str):
        """
        >>> _StringOperations.capitalize("")
        ''

        >>> _StringOperations.capitalize("foo")
        'Foo'
        """
        if word == "":
            return word
        return word[0].upper() + word[1:]


class Naming:
    """
    Representation of type and variable naming
    """
    def __init__(self, name: str):
        """
        >>> Naming("foo_bar")
        {"type": "FooBar", "value": "foo_bar"}
        """
        if not isinstance(name, str) or not re.match(r'[a-z_]+', name):
            raise ValueError("name should be a non empty lowercase string matching [a-z_]+")
        self._value_name = name
        self._class_name = _StringOperations.camel_case(name)
        self._components = set()

    @property
    def value_name(self) -> str:
        """
        Name for values
        """
        return self._value_name

    @property
    def class_name(self) -> str:
        """
        Name for class
        """
        return self._class_name

    def __eq__(self, other):
        return isinstance(other, Naming) and \
            self.value_name == other.value_name

    def __hash__(self):
        return self.value_name.__hash__()

    def __str__(self)  -> str:
        return '{{"type": "{}", "value": "{}"}}'.format(self.class_name, self.value_name)

    def __repr__(self) -> str:
        return str(self)


class PropertyList:
    """
    >>> c = PropertyList()
    >>> c.add(Naming("foo_bar"))
    >>> c.add(Naming("bar"))
    >>> c.add(Naming("foo"))
    >>> c.add(Naming("foo"))
    >>> c
    ["Bar", "Foo", "FooBar"]

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

    def __str__(self) -> str:
        return "[{}]".format(
            ", ".join(
                map(
                    lambda c: '"{}"'.format(c.class_name),
                    self.properties)))

    def __repr__(self) -> str:
        return str(self)


class Property:
    """
    >>> cl = PropertyList()
    >>> cl.add(Naming("distance"))
    >>> cl.add(Naming("duration"))
    >>> c = Property(Naming("speed"), cl)
    >>> c
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    >>> c = Property(Naming("speed"), None)
    >>> c
    {"naming": {"type": "Speed", "value": "speed"}}

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
        return isinstance(other, Property) and \
            self.naming == other.naming and \
            self.properties == other.properties

    def __repr__(self) -> str:
        return str(self)


#TODO: refactor the equation system to get rid of the callback -thing
#instead get the list of connection points as a return value from .evalute()

class PropertyGraph:
    """
To model your domain, create a property graph:

    >>> g  = PropertyGraph()

Please note that the I, O and C here are for the property graph instance g:

    >>> I, O, C = g.I, g.O, g.C

To measure speed you have to get interval and distance. To model this you can write:

    >>> speed = C('speed')
    >>> speed
    C(speed)

    >>> distance = C('distance')
    >>> duration = C('duration')

You can represent the need of something with the operator '*' and then 
have the properties set into the graph g like this:

    >>> for i in g.get_properties_from( speed*(distance+duration) ):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}


    >>> for i in g.properties:
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}

For fines you have to know (at least in Finland) also:

    >>> fine = C('fine')
    >>> monthly_income =  C('monthly_income')
    >>> speed_limit =  C('speed_limit')
    >>> for i in g.get_properties_from(speed*(distance + duration) + fine*(speed + monthly_income + speed_limit)):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}

Because these equations are the same (note the usage of the O)

    >>> O * (speed*(distance + duration) + fine*(speed + monthly_income + speed_limit)) * O == \
     O *  fine*(speed*(distance + duration)*O + monthly_income + speed_limit) * O
    True

also the generated properties are the same

    >>> for i in g.get_properties_from(fine*(speed*(distance + duration)*O + monthly_income + speed_limit)):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}

And so the generated property lists are also equal

    >>> list(g.get_properties_from(fine*(speed*(distance + duration)*O + monthly_income + speed_limit))) == \
        list(g.get_properties_from(speed*(distance + duration) + fine*(speed + monthly_income + speed_limit)))
    True

Nice and simple, but then the reality starts to kick in and you have to model the real thing where you have for example
different rules for small fines which do not need monthly income:

    >>> small_fine = C("small_fine")
    >>> for i in g.get_properties_from( \
        fine*(speed*(distance + duration)*O + monthly_income + speed_limit) + \
        small_fine*speed*(distance + duration)*O):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "SmallFine", "value": "small_fine"}, "properties": ["Speed"]}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}

Here one could inheritate the small fine and fine from the same base class which is same as the following trick
with the equation system:

    >>> for i in g.get_properties_from( \
          (fine* ( I + monthly_income*O + speed_limit*O) + small_fine)*speed*(distance + duration)):
    ...    print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "SmallFine", "value": "small_fine"}, "properties": ["Speed"]}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}

In other words: if you manage to minimize the equation, you get the optimal class structure from it. 

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
            yield Property(naming, properties)

    def get_properties_from(self, term):
        """
        Get the properties from the given term which has been done using the wrapper
        provided on the same class instance
        """
        self.clear()
        (self.O * term * self.O).evaluate()
        yield from self.properties


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




if __name__ == '__main__':
    import doctest
    doctest.testmod()
    