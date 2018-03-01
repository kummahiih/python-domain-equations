# python-domain-equations


@copyright: 2018 by Pauli Rikula <pauli.rikula@gmail.com>

@license: MIT <http://www.opensource.org/licenses/mit-license.php>


Represent and generate domain model classes from category equations.




    >>> g  = PropertyGraph()

    one can represent the need of something with the operator '*' in the following way:
    To measure speed you have to get interval and distance. To model this you can write:

    >>> speed = g.C('speed')
    >>> speed
    C(speed)

    >>> distance = g.C('distance')
    >>> duration = g.C('duration')
    >>> (speed*(distance+duration)).evaluate()
    >>> for i in g.properties:
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}

    For fines you have to know also:
    >>> fine = g.C('fine')
    >>> monthly_income =  g.C('monthly_income')
    >>> speed_limit =  g.C('speed_limit')
    >>> (speed*(distance + duration) + fine*(speed + monthly_income + speed_limit)).evaluate()
    >>> for i in g.properties:
    ...  print(i)
    {"naming": {"type": "Distance", "value": "distance"}}
    {"naming": {"type": "Duration", "value": "duration"}}
    {"naming": {"type": "Fine", "value": "fine"}, "properties": ["MonthlyIncome", "Speed", "SpeedLimit"]}
    {"naming": {"type": "MonthlyIncome", "value": "monthly_income"}}
    {"naming": {"type": "Speed", "value": "speed"}, "properties": ["Distance", "Duration"]}
    {"naming": {"type": "SpeedLimit", "value": "speed_limit"}}
    