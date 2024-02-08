import json

file = open("./winnings_report_0", "r")

data = []
try:
    data = json.load(file)
except Exception as e:
    file.close()
    print (e)

#average
sum = 0
for var in data:
    sum += float(var)
print (f"average = {sum/len(data)}")


win = 0
for var in data:
    if (float(var) >= 0):
        win += 1
print (f"wins   = {win}\nlosses = {len(data) - win}")

file.close()
