# Generate traffic data for an edge
import random
def generate():
    #return array of slowth coeficient [1-10]
    traffic = [1, 1, 1, 1, 1, 1, 1, 2, 7, 8, 3, 2, 1, 1, 1, 2, 3, 5, 7, 5, 1, 1, 1, 1, 1]

    for weight in traffic:
        if(random.randrange(1,1000) < 28):
            weight += 1

    return traffic