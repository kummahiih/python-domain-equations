# python-domain-equations


@copyright: 2018 by Pauli Rikula <pauli.rikula@gmail.com>

@license: MIT <http://www.opensource.org/licenses/mit-license.php>


Represent and generate domain model classes from category-like equations.




    >>> g  = PropertyGraph()
    >>> I, O, C = g.I, g.O, g.C

One can represent the need of something with the operator '*' in the following way:
To measure speed you have to get interval and distance. To model this you can write:

    >>> speed = C('speed')
    >>> speed
    C(speed)

    >>> distance = C('distance')
    >>> duration = C('duration')
    >>> g.get_properties_from(speed*(distance+duration))
    >>> for i in g.properties:
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}

For fines you have to know also:

    >>> fine = C('fine')
    >>> monthly_income =  C('monthly_income')
    >>> speed_limit =  C('speed_limit')
    >>> g.get_properties_from(speed*(distance + duration) + fine*(speed + monthly_income + speed_limit))
    >>> for i in g.properties:
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}


    