import numpy as np

sales = np.array([
    [200,220,250,270,300,320,310,330,350,370,390,420],
    [150,160,170,165,180,190,200,210,205,220,230,240],
    [300,310,305,320,330,340,360,370,380,390,410,430],
    [120,130,140,150,160,155,150,145,140,135,130,125],
    [220,230,240,260,270,290,300,320,340,360,380,400]
])

products = ["A","B","C","D","E"]

product_total = np.sum(sales,axis=1)
monthly_total = np.sum(sales,axis=0)

print("Total yearly sales per product:",product_total)
print("Monthly sales:",monthly_total)

best_product = np.argmax(product_total)
print("Best selling product:",products[best_product])

best_month = np.argmax(monthly_total)
print("Best sales month:",best_month+1)

print("Mean sales:",np.mean(sales,axis=1))
print("Std deviation:",np.std(sales,axis=1))

monthly_growth = np.diff(monthly_total)
growth_percent = (monthly_growth/monthly_total[:-1])*100
print("Growth %:",growth_percent)

top3 = np.argsort(monthly_total)[-3:]
print("Top 3 sales months:",top3+1)

avg_growth = np.mean(growth_percent)
prediction = monthly_total[-1]*(1+avg_growth/100)
print("Predicted next month sales:",prediction)