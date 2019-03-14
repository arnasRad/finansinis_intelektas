import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

csv_data = pd.read_csv('tick_data_EURUSD-2016-02.csv')
csv_data['Date'] = pd.to_datetime(csv_data['Date'], format="%Y%m%d %H:%M:%S.%f")
csv_data = csv_data.set_index('Date')

print("Sample data:")
print(csv_data.head(10))

plt.plot(csv_data.head(200))
plt.xticks(rotation=90)
plt.legend(['Open', 'Close'])
plt.xlabel('Laikas')
plt.ylabel('Kaina')
plt.grid()
plt.show()
# plt.close()
