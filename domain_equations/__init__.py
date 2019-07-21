"""
@copyright: 2018 - 2019 by Pauli Rikula <pauli.rikula@gmail.com>

@license: MIT <http://www.opensource.org/licenses/mit-license.php>


Generate and represent domain model classes via category-like equations which
can be simplified to get the optimal class structure for the modeled domain.

"""

from .property_graph import PropertyGraph
from .naming import TypeDescriptor, Naming, ContainerNaming
from .namedproperty import NamedProperty, PropertyList, Module
from .interface_generator import InterfaceGenerator
from .protobuf_generator import ProtobufScalars, ProtobufGenerator

__all__ = [
    'PropertyGraph', 'Naming', 'NamedProperty', 'PropertyList', 'InterfaceGenerator', 'TypeDescriptor', 'ProtobufScalars', 'Module', 'ProtobufGenerator']
