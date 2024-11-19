import csv
import matplotlib.pyplot as plt 

x =[]
y =[]
firstRun = False
with open('uci_datasets.csv', 'r') as csvfile:
    plots = csv.reader(csvfile)

    for row in plots:
        if firstRun != False:
            print(row[1])
            abbrievation = row[0].split()
            x.append(row[0])

            y.append(float(row[1]))
        else:
            firstRun = True
    
plt.bar(x,y, width=0.72, label = "stocks")
plt.colormaps['viridis']
plt.xticks(rotation=90)
plt.show()