import random

# Generate traffic data for an edge
def generate():
    
    # Base weighted array
    traffic = [1, 1, 1, 1, 1, 1, 1, 2, 7, 8, 3, 2, 1, 1, 1, 2, 3, 5, 7, 5, 1, 1, 1, 1, 1]
    
    # Random weight corresponding to crash probability
    for weight in traffic:
        if(random.randrange(1,1000) < 28):
            weight += 1
    
    # Return array of slowth coeficient [1-10]
    return traffic