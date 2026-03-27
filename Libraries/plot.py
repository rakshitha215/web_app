import matplotlib.pyplot as plt
years_experience = [10,15,30,22,19,12,17,25]
salary = [2500, 30000, 145000, 75000, 69000, 6000, 65000, 90000]

plt.figure(figsize=(8, 5))
plt.scatter(years_experience, salary)
plt.title("Years of Experience vs Salary")
plt.xlabel("Years of Experience")
plt.ylabel("Salary")
plt.grid(True)
plt.show()