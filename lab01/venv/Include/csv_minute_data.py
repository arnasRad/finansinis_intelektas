import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


csv_data = pd.read_csv('minute_data_EURUSD-2016.csv')
d_format = "%Y.%m.%d %H:%M"
csv_data['DateTime'] = csv_data['Date'] + ' ' + csv_data['Time']
csv_data['DateTime'] = pd.to_datetime(csv_data['DateTime'], format=d_format)
csv_data = csv_data.drop(['Date', 'Time'], 1)
csv_data = csv_data.set_index('DateTime')

print("Sample data:")
print(csv_data.head(10))

plt.plot(csv_data.head(100))
plt.xticks(rotation=90)
plt.legend(['Open', 'Low', 'High', 'Close'])
plt.xlabel('Laikas')
plt.ylabel('Kaina')
plt.grid()
plt.show()
# plt.close()