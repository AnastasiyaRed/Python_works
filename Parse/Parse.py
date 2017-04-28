import re

import matplotlib.pyplot as plt
from prettytable import PrettyTable

my_file = open("test_data.log", "r")
my_lines = my_file.readlines()
my_file.close()

def analizing(lines):
    hist = re.findall(r'((?<=\"hist\"\: \{).*?(?=},))', str(lines))
    data = re.findall(r'(?<=\"data\"\: \[).*?(?=\])', str(hist))
    bins = re.findall(r'(?<=\"bins\"\: \[).*?(?=\])', str(hist))

    list_requests = [k for j in (i.split(', ') for i in data) for k in j]
    list_sla = [k for j in (i.split(', ') for i in bins) for k in j]

    n = len(list_requests)

    # create dictionary 'response_time': 'count requests'.
    d = {}
    for i in range(n):
        if list_sla[i] in d:
            d[int(list_sla[i])] += int(list_requests[i])
        else:
            d[int(list_sla[i])] = int(list_requests[i])

    # sum of all requests
    summ = 0
    for i in d:
        summ += d[i]

    # print table HTTP codes
    print('HTTP codes')
    table = PrettyTable([" ", "Count", "Percent"])
    table.add_row(['302 - Found', summ, '100%'])
    print(table)

    # count percentiles using dictionary -d
    table = PrettyTable([" ", "Count", "Percent", "Quantile"])
    a = list(d.keys())
    a.sort()

    print('Response time distribution')
    percentiles = {}
    for i in reversed(a):
        percent = round(d[i] * 100 / summ, 3)
        amount = 0
        for j in a:
            if j <= i:
                amount += d[j]
        percentile = round(amount * 100 / summ, 3)
        percentiles[i] = percentile
        # print("%i\t\t%i\t\t%s\t\t%s" % (i/1000, d[i], percent, percentile))
        table.add_row([i / 1000, d[i], percent, percentile])
    print(table)

    # count quantiles using dictionary -percentiles
    print("Cumulative quantiles")
    quantiles = [99, 98, 95, 90, 85, 80, 75, 50]

    Quantile = {}
    V = percentiles.keys()
    for q in quantiles:
        v = 100
        response_time = 0
        for p in V:
            if percentiles[p] >= q:
                if percentiles[p] < v:
                    v = percentiles[p]
                    response_time = int(p / 1000)
                    Quantile[q] = response_time
                    # print("%i%%\t\t%i" % (q, response_time))

    # print table Quantile
    table = PrettyTable([" ", "Quantile"])
    for i in reversed(sorted(Quantile.keys())):
        table.add_row(["%i%%" % i, Quantile[i]])
    print(table)

    # graph
    x = list(Quantile.keys())
    y = list(Quantile.values())

    # bar()
    fig = plt.figure()
    plt.bar(x, y)
    plt.title('Simple bar chart')
    plt.grid(True)  # линии вспомогательной сетки
    # plt.show()

if __name__ == "__main__":
   # print ('This program is being run by itself')
    analizing(my_lines)
else:
	print ('I am being imported from another module')