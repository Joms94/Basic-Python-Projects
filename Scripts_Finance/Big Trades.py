import pandas as pd
import matplotlib.pyplot as plt

trades = pd.read_csv("D:\Personal\Education\Programming\Test files\ge_transactions.csv", header=0, index_col=0, squeeze=False).to_dict()
ge_frame = pd.DataFrame(trades)
chart_headers = ["Item", "Actual Profit"]
ge_profits = ge_frame[chart_headers]
sorted_profits = ge_profits.sort_values(by=["Actual Profit"], ascending=False)
cleaned_profits = sorted_profits.dropna()
cleaned_profits["Actual Profit"] = cleaned_profits["Actual Profit"].str.replace(r",", "")
print(cleaned_profits)

plt.pie(cleaned_profits[chart_headers].head(10), labels="Actual Profit", autopct="%1.1f%%")
plt.title("Profits")
plt.axis("equal")
plt.show()
