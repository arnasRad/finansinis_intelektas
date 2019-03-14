import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

csv_data = pd.read_csv('daily_data_EURUSD-2016.csv')
csv_data['Date'] = pd.to_datetime(csv_data['Date'], format="%b %d, %Y")
csv_data = csv_data.set_index('Date')
csv_data = csv_data.drop(['Change %'], 1)
df = csv_data.drop(['Low', 'High'], 1)

print("Sample data:")
print(df.head(10))

plt.plot(df.head(100))
plt.xticks(rotation=90)
plt.legend(['Close', 'Open'])
plt.xlabel('Laikas')
plt.ylabel('Kaina')
plt.grid()
plt.show()
# plt.close()
