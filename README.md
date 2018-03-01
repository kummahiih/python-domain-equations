# python-domain-equations


@copyright: 2018 by Pauli Rikula <pauli.rikula@gmail.com>

@license: MIT <http://www.opensource.org/licenses/mit-license.php>


Generate and represent domain model classes via category-like equations which
can be simplified to get the optimal class structure for the modeled domain.




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

    >>> O * (speed*(distance + duration) + fine*(speed + monthly_income + speed_limit)) * O ==      O *  fine*(speed*(distance + duration)*O + monthly_income + speed_limit) * O
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

    >>> list(g.get_properties_from(fine*(speed*(distance + duration)*O + monthly_income + speed_limit))) ==         list(g.get_properties_from(speed*(distance + duration) + fine*(speed + monthly_income + speed_limit)))
    True

Nice and simple, but then the reality starts to kick in and you have to model the real thing where you have for example
different rules for small fines which do not need monthly income:

    >>> small_fine = C("small_fine")
    >>> for i in g.get_properties_from(         fine*(speed*(distance + duration)*O + monthly_income + speed_limit) +         small_fine*speed*(distance + duration)*O):
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

    >>> for i in g.get_properties_from(           (fine* ( I + monthly_income*O + speed_limit*O) + small_fine)*speed*(distance + duration)):
    ...    print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "SmallFine", "value": "small_fine"}, "properties": ["Speed"]}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}

In other words: if you manage to minimize the equation, you get the optimal class structure from it. 

    