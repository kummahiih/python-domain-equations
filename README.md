# python-domain-equations

Generate and represent domain model classes via category-like equations
which can be simplified to get the optimal class structure for the modeled domain.

## Rationale

If you have a problem, it sometime helps if you formulate the problem in a new perspective.

The PropertyGraph -class can be used to domain model class structure modeling and generation.
The trick here is to transform the problem to category-like equations which
can be simplified to get the optimal class structure for the modeled domain.

More details of the equation system can be found from the site: https://github.com/kummahiih/python-category-equations

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
    >>> first_model = O * (speed*(distance + duration) + fine*(speed + monthly_income + speed_limit)) * O
    >>> for i in g.get_properties_from(first_model):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}

Because these equations are the same (note the usage of the O at the begin and end)

    >>> simplified_model =  O *  fine*(speed*(distance + duration)*O + monthly_income + speed_limit) * O
    >>> first_model == simplified_model
    True

also the generated properties are the same:

    >>> for i in g.get_properties_from(simplified_model):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}

Nice and simple, but then the reality starts to kick in and you have to model the real thing where you have for example
different rules for small fines which do not need monthly income:

    >>> small_fine = C("small_fine")
    >>> second_model =O*(fine* (speed*(distance + duration)*O + monthly_income + speed_limit) + small_fine*(speed + speed_limit))*O
    >>> for i in g.get_properties_from(second_model):
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "SmallFine", "value": "small_fine"}, "properties": ["Speed", "SpeedLimit"]}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}

Here one could create an intermediate class and use it as a member on both fines or inherit the small fine and fine from the same base class.
If you write it by using the provided equation system, it looks like this:
    
    >>> second_model_simplified = O * (fine* ( I + monthly_income*O ) + small_fine)*(speed + speed_limit*O)*(distance + duration) * O
    >>> second_model_simplified == second_model
    True

In other words: if you manage to minimize the equation by finding the common divisors, you can get the optimal class composition
structure from it.

In case you are wondering how to spot the potential intermediate constructs from the model, the trick is to search for the 
summed product terms which end to a term O:

    >>> for term in g.extract_intermediate_terms(second_model_simplified):
    ...   print(term)
    (((C(speed)) + ((C(speed_limit)) * (O))) * ((C(distance)) + (C(duration)))) * (O)
    ((C(distance)) + (C(duration))) * (O)


    