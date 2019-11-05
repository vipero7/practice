import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
import algo
import mysql.connector


dbconfig = {'host': '127.0.0.1',
            'database': 'travel_feed',
            'user': 'root',
            'password': '7787',
            }
conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()
#
cursor.execute("""select id, pilgrims, pilgrims_like, foodie, foodie_like, adventure, adventure_like, waterbody, waterbody_like, natureseeing, natureseeing_like ,ancient, ancient_like from userprofiles""")
d = cursor.fetchall()
data = np.array(d)
# print(data)
id= data[:,0]
# print(type(id));
X = data

# print(X);

# data = pd.read_csv('data.csv')
# X = data.to_numpy()
# X = X.astype('int32')
print(X);


# normalizing data data using numpy method.
normalizedData  = X / np.linalg.norm(X);

print(normalizedData);

# print(normalized);
# print(np.linalg.norm(X));

final_clusters = algo.find_clusters(normalizedData)
cluster = algo.elbow_method(normalizedData, final_clusters)
print(cluster)
k = final_clusters[cluster]
print(k)

cursor.execute("""truncate table user_clusters""")
conn.commit()
v = 0
for c in k:
    v = v+1
    cursor.execute("""insert into user_clusters
            (userprofile_id, cluster)
            values
            (%s, %s)""", (v,k[c]))
    conn.commit()
cursor.close()
conn.close()