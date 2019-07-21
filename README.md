# python-domain-equations

Generate and represent domain model classes via category-like equations
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
    {"naming": {"type": "Distance", "value": "distance", "plural": "distances", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "plural": "durations", "docstring": "duration"}}
    {"naming": {"type": "Speed", "value": "speed", "plural": "speeds", "docstring": "speed"}, "properties": ["Distance", "Duration"]}


    >>> for i in g.properties:
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance", "plural": "distances", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "plural": "durations", "docstring": "duration"}}
    {"naming": {"type": "Speed", "value": "speed", "plural": "speeds", "docstring": "speed"}, "properties": ["Distance", "Duration"]}

For fines you have to know (at least in Finland) also:

    >>> fine = C('fine')
    >>> monthly_income =  C('monthly_income')
    >>> speed_limit =  C('speed_limit')
    >>> first_model = O * (speed*(distance + duration) + fine*(speed + monthly_income + speed_limit)) * O
    >>> for i in g.get_properties_from(first_model):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance", "plural": "distances", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "plural": "durations", "docstring": "duration"}}
    {"naming": {"type": "Fine", "value": "fine", "plural": "fines", "docstring": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income", "plural": "monthly_incomes", "docstring": "monthly income"}}
    {"naming": {"type": "Speed", "value": "speed", "plural": "speeds", "docstring": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit", "plural": "speed_limits", "docstring": "speed limit"}}

Because these equations are the same (note the usage of the O at the begin and end)

    >>> simplified_model =  O *  fine*(speed*(distance + duration)*O + monthly_income + speed_limit) * O
    >>> first_model == simplified_model
    True

also the generated properties are the same:

    >>> for i in g.get_properties_from(simplified_model):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance", "plural": "distances", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "plural": "durations", "docstring": "duration"}}
    {"naming": {"type": "Fine", "value": "fine", "plural": "fines", "docstring": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income", "plural": "monthly_incomes", "docstring": "monthly income"}}
    {"naming": {"type": "Speed", "value": "speed", "plural": "speeds", "docstring": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit", "plural": "speed_limits", "docstring": "speed limit"}}


Nice and simple, but then the reality starts to kick in and you have to model the real thing where you have for example
different rules for small fines which do not need monthly income:

    >>> small_fine = C("small_fine")
    >>> second_model =O*(fine* (speed*(distance + duration)*O + monthly_income + speed_limit) + small_fine*(speed + speed_limit))*O
    >>> for i in g.get_properties_from(second_model):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance", "plural": "distances", "docstring": "distance"}}
    {"naming": {"type": "Duration", "value": "duration", "plural": "durations", "docstring": "duration"}}
    {"naming": {"type": "Fine", "value": "fine", "plural": "fines", "docstring": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income", "plural": "monthly_incomes", "docstring": "monthly income"}}
    {"naming": {"type": "SmallFine", "value": "small_fine", "plural": "small_fines", "docstring": "small fine"}, "properties": ["Speed", "SpeedLimit"]}
    {"naming": {"type": "Speed", "value": "speed", "plural": "speeds", "docstring": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit", "plural": "speed_limits", "docstring": "speed limit"}}


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
    namespace(IDistance=<class 'domain_equations.interface_generator.IDistance'>, IDuration=<class 'domain_equations.interface_generator.IDuration'>, IFine=<class 'domain_equations.interface_generator.IFine'>, IMonthlyIncome=<class 'domain_equations.interface_generator.IMonthlyIncome'>, ISmallFine=<class 'domain_equations.interface_generator.ISmallFine'>, ISpeed=<class 'domain_equations.interface_generator.ISpeed'>, ISpeedLimit=<class 'domain_equations.interface_generator.ISpeedLimit'>)

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

The container types are supported this far:

    >>> R = g.R
    >>> fine_container = R('fine')
    >>> fine_container * fine
    (C(fine_container)) * (C(fine))

Or

    >>> g  = PropertyGraph()
    >>> I, O, C, N, R, T = g.I, g.O, g.C, g.N, g.R, g.T


    >>> knife = N(name="knife", plural="knives", module_name="accessories")
    >>> knife
    C(accessories.Knife)
    >>> knife_container = R('knife', item_module="accessories")
    >>> model = O * knife_container * knife * O
    >>> model
    (((O) * (C(knife_container))) * (C(accessories.Knife))) * (O)

And the abstract class generation works as well:

    >>> for term in g.get_properties_from(model):
    ...   print(term)
    {"naming": {"type": "KnifeContainer", "value": "knife_container", "plural": "knife_containers", "docstring": "knife container"}, "properties": ["accessories.Knife"]}
    {"naming": {"type": "accessories.Knife", "value": "knife", "plural": "knives", "docstring": "knife"}}


    >>> interfaces = g.get_abstract_classes()
    >>> class KnifeContainer(interfaces.IKnifeContainer): pass
    >>> f = KnifeContainer()
    Traceback (most recent call last):
    ...
    TypeError: Can't instantiate abstract class KnifeContainer with abstract methods knives


Base types are can be taken here with a decorator 'T' obtained above and they work with modules like this:

    >>> g  = PropertyGraph()
    >>> I, O, C, N, R, T = g.I, g.O, g.C, g.N, g.R, g.T
    >>> knife = N(name="knife", plural="knives", module_name="accessories")
    >>> bytes = T('bytes')
    >>> for term in g.buildin_types:
    ...   print(term)
    {"type": "bytes"}

    >>> model = O *(R('knife', item_module="accessories", container_module="kitchen") * knife * O + knife * bytes) * O
    >>> model
    ((O) * ((((C(kitchen.KnifeContainer)) * (C(accessories.Knife))) * (O)) + ((C(accessories.Knife)) * (C(bytes))))) * (O)

    >>> for term in g.get_properties_from(model):
    ...   print(term)
    {"naming": {"type": "accessories.Knife", "value": "knife", "plural": "knives", "docstring": "knife"}, "properties": ["bytes"]}
    {"naming": {"type": "kitchen.KnifeContainer", "value": "knife_container", "plural": "knife_containers", "docstring": "knife container"}, "properties": ["accessories.Knife"]}

    >>> for term in g.buildin_types:
    ...   print(term)
    {"type": "bytes"}


    >>> for module in g.modules:
    ...   print(module)
    {"module": accessories, "types": ["accessories.Knife"]}
    {"module": kitchen, "types": ["kitchen.KnifeContainer"]}


    >>> for module in g.modules:
    ...    print("-"*20)
    ...    print(module.module_name)
    ...    print("-"*20)
    ...    print(ProtobufGenerator.get_property_file_content(module))
    --------------------
    accessories
    --------------------
    syntax = "proto2";
    package accessories;
    --------------------
    kitchen
    --------------------
    syntax = "proto2";
    package kitchen;
    import accessories;
    message KnifeContainer {
        repeated bytes knives = 1;
    }



    >>> g  = PropertyGraph()
    >>> I, O, C, N, R, T = g.I, g.O, g.C, g.N, g.R, g.T
    >>> knife = N(name="knife", plural="knives", module_name="accessories")
    >>> bytes = T('bytes')
    >>> length_type = T('float')
    >>> knife_def = knife * ( C("name") * bytes * O + C("length") * length_type * O)
    >>> knife_container_def = R('knife', item_module="accessories", container_module="kitchen") * knife * O
    >>> model = O *(knife_container_def + knife_def ) * O
    >>> model.evaluate()
    >>> for term in g.properties:
    ...   print(term)
    {"naming": {"type": "Length", "value": "length", "plural": "lengths", "docstring": "length"}, "properties": ["float"]}
    {"naming": {"type": "Name", "value": "name", "plural": "names", "docstring": "name"}, "properties": ["bytes"]}
    {"naming": {"type": "accessories.Knife", "value": "knife", "plural": "knives", "docstring": "knife"}, "properties": ["Length", "Name"]}
    {"naming": {"type": "kitchen.KnifeContainer", "value": "knife_container", "plural": "knife_containers", "docstring": "knife container"}, "properties": ["accessories.Knife"]}


    >>> for module in g.modules:
    ...    print("-"*20)
    ...    print(module.module_name + ".proto")
    ...    print("-"*20)
    ...    print(ProtobufGenerator.get_property_file_content(module))
    --------------------
    accessories.proto
    --------------------
    syntax = "proto2";
    package accessories;
    message Knife {
        required float length = 1;
        required bytes name = 2;
    }
    --------------------
    kitchen.proto
    --------------------
    syntax = "proto2";
    package kitchen;
    import accessories;
    message KnifeContainer {
        repeated Knife knives = 1;
    }



    