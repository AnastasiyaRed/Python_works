import re
from prettytable import PrettyTable
import matplotlib.pyplot as plt

my_file = open("test_data.log", "r").readlines()
hist = re.findall(r'((?<=\"hist\"\: \{).*?(?=},))',str(my_file))
data= (re.findall(r'(?<=\"data\"\: \[).*?(?=\])', str(hist)))
bins= re.findall(r'(?<=\"bins\"\: \[).*?(?=\])', str(hist))

#add parsing data[] to list_count
list_count=[]
for i in data:
    k=i.split(', ')
    for j in k:
        list_count.append(j)

#add parsing bins[] to list_sla
list_sla=[]
for i in bins:
    k=i.split(', ')
    for j in k:
        list_sla.append(j)

n=len(list_sla)

#count requests for every response time in list_sla
#1)unique response times to s from list_sla
response_times=[]
for i in list_sla:
    if i not in response_times:
        response_times.append(i)

#2)create dictionary 'response_time': 'count requests'...
d={}
for i in response_times:
    count=0
    for j in range(n):
        if i==list_sla[j]:
           count+=int(list_count[j])
    d[int(i)]=count

#summ of all requests
summ=0
for i in d:
    summ+=d[i]

print('HTTP codes')
table = PrettyTable([" ", "Count", "Percent"])
table.add_row(['302 - Found', summ, '100%'])
print (table)

#count percentiles using dictionary -d
table = PrettyTable([" ", "Count", "Percent", "Quantile"])
a = list(d.keys())
a.sort()

print('Response time distribution')
percentiles={}
for i in reversed(a):
    percent = round(d[i]*100/summ,3)
    amount=0
    for j in a:
       if (j<=i):
           amount+=d[j]
    percentile=round(amount*100/summ,3)
    percentiles[i]=percentile
    #print("%i\t\t%i\t\t%s\t\t%s" % (i/1000, d[i], percent, percentile))
    table.add_row([i/1000, d[i], percent, percentile])
print(table)

#count quantiles using dictionary -percentiles
print("Cumulative quantiles")
quantiles=[99, 98, 95, 90, 85, 80, 75, 50]

Quantile={}
V=percentiles.keys()
for q in quantiles:
    v=100
    response_time=0
    for p in V:
        if percentiles[p]>=q:
            if percentiles[p]<v:
                v=percentiles[p]
                response_time=int(p/1000)
                Quantile[q]=response_time
    #print("%i%%\t\t%i" % (q, response_time))



#print table Quantile
table = PrettyTable([" ", "Quantile"])
for i in reversed(sorted(Quantile.keys())):
    table.add_row(["%i%%" % i, Quantile[i]])
print (table)

#graph
x=list(Quantile.keys())
y=list(Quantile.values())

# bar()
fig = plt.figure()
plt.bar(x,y)
plt.title('Simple bar chart')
plt.grid(True)   # линии вспомогательной сетки
#plt.show()
