import random
import math
cache = []
# Generate traffic data for an edge
def generate():
    global cache
    if len(cache) == 0:

        m_a = 1503.43402
        m_b = -556561.2208
        m_max = m_a*60*12+m_b

        e_a = -1507.393614
        e_b = 1862163.515
        e_max = e_a*60*12+e_b
        morning = [int(round(10*(m_a*60*i+m_b)/m_max)) if 10*(m_a*60*i+m_b)/m_max >= 0 else 0 for i in range(0,12) ]
        evening = [int(round(10*(e_a*60*i+e_b)/e_max)) if 10*(e_a*60*i+e_b)/e_max >=0 else 0 for i in range(12,24)]

        cache=morning+evening
    # Predicted weight array from project given data
    # traffic = [0, 0, 0, 0, 0, 0, 0, 2, 4, 6, 8, 10, 10, 9, 8, 7, 5, 4, 3, 2, 1, 0, 0, 0]

    # Base weighted array from offical french stats
    # traffic = [1, 1, 1, 1, 1, 1, 1, 2, 7, 8, 3, 2, 1, 1, 1, 2, 3, 5, 7, 5, 1, 1, 1, 1, 1]

    # Return array of slowth coeficient [0-10]
    return cache