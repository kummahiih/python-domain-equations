
"""
   @copyright: 2018-2019 by Pauli Rikula <pauli.rikula@gmail.com>
   @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""

import re

class TypeDescriptor:
    def __init__(self, class_name: str = None, module_name: str = None):
        self._module_name = module_name
        self._class_name = class_name

    @property
    def module_name(self) -> str:
        """
        Name for module of the class
        >>> TypeDescriptor(class_name="foo_bar", module_name="module").module_name
        'module'

        """
        return self._module_name

    @property
    def class_name(self) -> str:
        """
        Name for class

        """
        prefix = ""
        if not self._module_name is None:
            prefix = self._module_name + "."
        return prefix + self._class_name
    
    @property
    def moduleless_class_name(self):
        """
        Name for class without module prefix

        """

        return self._class_name

    
    def __eq__(self, other):
        return isinstance(other, TypeDescriptor) and \
            self.class_name == other.class_name

    def __hash__(self):
        return self.class_name.__hash__()

    def __str__(self)  -> str:
        return '{{"type": "{}"}}'.format(self.class_name)

    def __repr__(self):
        return str(self)
    
    def __lt__(self, another):
        """
        >>> TypeDescriptor("foo_bar") < TypeDescriptor("foo")
        False
        >>> TypeDescriptor("foo") < TypeDescriptor("foo_bar")
        True

        """
        return self.class_name < another.class_name


class Naming(TypeDescriptor):
    """
    Representation of type and variable naming
    """
    def __init__(self, name: str, plural:str = None, module_name: str=None):
        """
        >>> Naming("foo_bar")
        {"type": "FooBar", "value": "foo_bar", "plural": "foo_bars", "docstring": "foo bar"}
        >>> Naming("foo_bar", module_name="module")
        {"type": "module.FooBar", "value": "foo_bar", "plural": "foo_bars", "docstring": "foo bar"}

        """
        if not isinstance(name, str) or not re.match(r'[a-z][a-z_]*', name):
            raise ValueError("name should be a non empty lowercase string matching [a-z][a-z_]*")
        if plural is not None and (not isinstance(plural, str) or not re.match(r'[a-z][a-z_]*', plural)):
            raise ValueError("name plural be a non empty lowercase string matching [a-z][a-z_]*")
        self._value_name = name
        self._plural_value_name = plural if plural is not None else Naming.plural(name)
        module_name = module_name
        class_name = Naming.camel_case(name)
        self._docstring_name = name.replace('_', ' ')
        super().__init__(
            module_name=module_name,
            class_name=class_name)
        

    @property
    def value_name(self) -> str:
        """
        Name for values

        """
        return self._value_name

    @property
    def plural_value_name(self):
        """
        Name for plural values

        """
        return self._plural_value_name
    
    @property
    def docstring_name(self) -> str:
        """
        Name for docstring

        """
        return self._docstring_name
    
    @property
    def interface_name(self) -> str:
        """
        Name for class

        """
        return "I" + self._class_name

    def __str__(self)  -> str:
        return '{{"type": "{}", "value": "{}", "plural": "{}", "docstring": "{}"}}'.format(self.class_name, self.value_name, self.plural_value_name, self.docstring_name)
        
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
    
    @staticmethod
    def plural(word: str) -> str:
        """
        >>> Naming.plural('test')
        'tests'

        >>> Naming.plural('phalanx')
        'phalanxes'

        >> Naming.plural('ssh')
        'sshes'

        >> Naming.plural('snakes')
        'snakeses'

        >> Naming.plural('py')
        'pyses'

        >> Naming.plural('way')
        'ways'

        """
        if word[-1] in ['x', 's']:
                return word + 'es'
        if len(word) >= 2:
            if word[-1] == 'y':
                if word[-2] in ['a', 'e', 'i', 'o', 'u']:
                    return word + "s"
                else:
                    return word[:-1] + "es"
            if word[-2:] in ["sh", "ch"]:
                return word + 'es'

        return word + "s"
            
class ContainerNaming(Naming):
    def __init__(self, naming:Naming, module_name:str = None):
        """
        >>> ContainerNaming(Naming("test"))
        {"type": "TestContainer", "value": "test_container", "plural": "test_containers", "docstring": "test container"}

        """

        if not isinstance(naming, Naming):
            raise ValueError("containers can be made only from Namings")
        self._item_class_name = naming.class_name
        name = naming.value_name + "_container"

        super().__init__(name=name, module_name=module_name)

    @property
    def item_class_name(self):
        return self._item_class_name
