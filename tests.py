

if __name__ == '__main__':
    import doctest
    import domain_equations
    import copy
    import types
    globs = {
        'ProtobufGenerator': domain_equations.ProtobufGenerator,
        'Module': domain_equations.Module,
        'ProtobufScalars' : domain_equations.ProtobufScalars,
        'TypeDescriptor' : domain_equations.TypeDescriptor,
        'ContainerNaming': domain_equations.ContainerNaming,
        'Naming': domain_equations.Naming,
        'PropertyList': domain_equations.PropertyList,
        'NamedProperty': domain_equations.NamedProperty,
        'InterfaceGenerator': domain_equations.InterfaceGenerator,
        'PropertyGraph': domain_equations.PropertyGraph}
    doctest.testfile(filename="naming.py", module_relative=True, package=domain_equations, globs=globs)
    doctest.testfile(filename="namedproperty.py", module_relative=True, package=domain_equations, globs=globs)
    doctest.testfile(filename="interface_generator.py", module_relative=True, package=domain_equations, globs=globs)
    doctest.testfile(filename="protobuf_generator.py", module_relative=True, package=domain_equations, globs=globs)
    doctest.testfile(filename="property_graph.py", module_relative=True, package=domain_equations, globs=globs)
    #print(domain_equations.__doc__)
    #doctest.testmod(m=domain_equations, verbose=True)