import random

def generate_Tw(n):
    tw = []
    for i in range(0, n):
        start = random.randrange(30,1440, 30) 
        end = (start + random.randrange(60,180, 30)) % 1440
        tw.append({"start": start, "end": end})
    return tw
