"""
   @copyright: 2018 by Pauli Rikula <pauli.rikula@gmail.com>
   @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""

from category_equations import from_operator




def get_component_graph():
    """
    With these tools

    >>> g  = get_component_graph()

    one can represent the need of something with the operator '*' in the following way:
    To measure speed you have to get interval and distance. To model this you can write:

    >>> speed = g.C('speed')
    >>> speed
    {"name": "Speed", "value_name": "speed"}

    >>> distance = g.C('distance')
    >>> duration = g.C('duration')
    >>> (speed*(distance+duration)).evaluate()
    {"name": "Distance", "value_name": "distance"}
    {"name": "Duration", "value_name": "duration"}
    {"name": "Speed", "components": {"Distance", "Duration"} , "value_name": "speed"}

    For fines you have to know also:
    >>> fine = g.C('fine')
    >>> monthly_income =  g.C('monthly_income')
    >>> speed_limit =  g.C('speed_limit')
    >>> (speed*(distance + duration) + fines*(speed + monthly_income + speed_limit)).evaluate()
    {"name": "Distance", "value_name": "distance"}
    {"name": "Duration", "value_name": "duration"}
    {"name": "Fine", "components": ["MonthlyIncome", "Speed", "SpeedLimit"], "value_name": "fine"}
    {"name": "Speed", "components": ["Distance", "Duration"] , "value_name": "speed"}
    {"name": "SpeedLimit", "value_name": "speed_limit"}
    """
    
   



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    Is, Os, Cs, evaluate = get_set_adding_tools()