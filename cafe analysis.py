import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/dell/OneDrive/Documents/cafe_data/cafesales.csv")
ca = df.copy()


#converting data into numeric basically into nan

ca['Total Spent'] = pd.to_numeric(ca['Total Spent'], errors="coerce")
ca['Quantity'] = pd.to_numeric(ca['Quantity'], errors="coerce")
ca['Price Per Unit'] = pd.to_numeric(ca['Price Per Unit'], errors="coerce")

# cols = ["Quantity", "Price Per Unit", "Total Spent"]
# ca[cols] = ca[cols].apply(pd.to_numeric, errors="coerce")



# cleaning nan values from quantity,total spent and price per unit
ca["Quantity"] = ca["Quantity"].fillna(ca["Quantity"].mean())
ca["Price Per Unit"] = ca["Price Per Unit"].fillna(ca["Price Per Unit"].mean())
ca["Total Spent"] = ca["Total Spent"].fillna(ca['Quantity'] * ca["Price Per Unit"])
# print(pd.DataFrame(ca))

# cleaning date

ca['Transaction Date']=pd.to_datetime(ca["Transaction Date"], errors="coerce")
ca["Transaction Date"]=ca["Transaction Date"].fillna(ca["Transaction Date"].mode()[0])
ca["Transaction Date"]=ca["Transaction Date"].dt.strftime("%d-%m-%Y")
 

# cleaning items,payment method and location
cols = ["Location", "Payment Method", "Item"]
ca[cols] = ca[cols].replace(["UNKNOWN", "ERROR"], np.nan)
for i in cols:
    ca[i]=ca[i].fillna(ca[i].mode()[0])
# print(ca['Item'].head(60))
# ca.to_csv("C:/Users/dell/Desktop/cleaned_cafe_data1.csv", index=False) 




#visualization of data using matplot lib
plt.subplot(2,3,1)
plt.hist(ca["Quantity"])
plt.title("Quantity Distribution")
plt.xlabel("Quantity")
plt.ylabel("Frequency")


plt.subplot(2,3,2)
location_sales = ca.groupby("Location")["Total Spent"].sum()
plt.bar(location_sales.index, location_sales.values)
plt.title("Total Sales by Location")
plt.xlabel("Location")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)


plt.subplot(2,3,3)
payment_counts = ca["Payment Method"].value_counts()
plt.pie(payment_counts, labels=payment_counts.index, autopct="%1.1f%%")
plt.title("Payment Method Distribution")


plt.subplot(2,3,4)
plt.scatter(ca["Price Per Unit"], ca["Quantity"])
plt.title("Price vs Quantity")
plt.xlabel("Price Per Unit")
plt.ylabel("Quantity")


plt.subplot(2,3,5)
ca["Transaction Date"] = pd.to_datetime(ca["Transaction Date"], errors="coerce")

sales_by_date = ca.groupby("Transaction Date")["Total Spent"].sum()

plt.plot(sales_by_date.index, sales_by_date.values)
plt.title("Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)

plt.tight_layout()


plt.show()