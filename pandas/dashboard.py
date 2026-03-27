import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data = {
    "Order_ID": range(1, 21),
    "Customer_Age": np.random.randint(18, 60, 20),
    "Gender": np.random.choice(["Male", "Female"], 20),
    "Purchase_Amount": np.random.randint(100, 1000, 20),
    "Category": np.random.choice(["Electronics", "Clothing", "Groceries"], 20),
    "Order_Date": pd.date_range(start="2025-01-01", periods=20, freq='D')
}

df = pd.DataFrame(data)

df["Month"] = df["Order_Date"].dt.month

plt.figure(figsize=(15, 10))


monthly_revenue = df.groupby("Month")["Purchase_Amount"].sum()

plt.subplot(2, 2, 1)
plt.plot(monthly_revenue.index, monthly_revenue.values, marker='o')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

gender_counts = df["Gender"].value_counts()

plt.subplot(2, 2, 2)
plt.bar(gender_counts.index, gender_counts.values)
plt.title("Customer Demographics (Gender)")
plt.xlabel("Gender")
plt.ylabel("Count")

plt.subplot(2, 2, 3)
plt.hist(df["Customer_Age"], bins=8)
plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
category_revenue = df.groupby("Category")["Purchase_Amount"].sum()

plt.subplot(2, 2, 4)
plt.bar(category_revenue.index, category_revenue.values)
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.suptitle("E-Commerce Customer Insights Dashboard", fontsize=16)
plt.subplots_adjust(top=0.92)
plt.show()