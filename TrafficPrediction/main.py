from pymongo import MongoClient
import matplotlib.pyplot as plt

client = MongoClient('localhost', 27017)
db = client['DataProject']
vehicules = db['vehicules']

vehicules_stamped = db['vehicules_stamped']


rows = vehicules_stamped.aggregate( [
                #{"$match": { "num_arete" : 93 }},
                {"$addFields": {
                    "h": {
                        "$arrayElemAt": [ 
                                    {"$split": [ "$date", " " ] },
                                    1 ]
                    }
                }},
                {"$group": {
                    "_id": {"date" : "$h", "arete" : "$num_arete"},
                    "count": {"$sum": "$nb_vehicules"}
                    }
                },
                {"$sort" : {"_id.date" :1}}
            ])
fig, (mx, sx) = plt.subplots(2) 
m = {}
s= {}
for i in rows:
    date_ar = i["_id"]["date"].split('h')
    minute = int(date_ar[0]) * 60 + int(date_ar[1][:-1])
    if i["_id"]["date"][0] == "0" : 
        if not minute in m : m[minute] = i["count"]
        else : m[minute] += i["count"]
    else:
        if not minute in s : s[minute] = i["count"]
        else : s[minute] += i["count"]


mx.scatter(m.keys(),m.values())
sx.scatter(s.keys(),s.values())


fig.suptitle("Mesured number of vehicule per minute for morning an evening period")
fig.add_axes(mx)
fig.add_axes(sx)
fig.show()
#print(m)
#print(s)
input()
