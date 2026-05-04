import json

f_name = "limits_database/All_Limits.txt"

with open(f_name, "r") as f:
    limits = json.load( f)

for limit in limits:
    print(limit)
    print(limits[limit]["YSlice"]["2000"]["4000"])
