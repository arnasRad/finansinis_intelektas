import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

dates = pd.date_range('20190214', periods=6)
numbers = np.matrix([[101, 103], [105.5, 75], [102, 80.3], [100, 85], [110, 98], [109.6, 125.7]])
df = pd.DataFrame(numbers, index=dates, columns=['A', 'B'])

print(df)

print("\n# 1.")
print(df.loc['2019-02-18'])

print("\n# 2.")
print(df.loc[datetime.datetime(2019, 2, 18)])

print("\n# 3.")
print(df.tail(2).iloc[0])

print("\n# 4.")
print(df.head(2)['B'])

print("\n# 5.")
df = df.sort_values(by=['B'], ascending=False)
print(df)

print("\n# 6.")
print(df.max()['A'])

print("\n# 7.")
max_value = df.max()['A']
df.loc[df.idxmax(0)['A']]['A'] = max_value * 2
print(df)

print("\n# 8.")
print(df[df.A > 105])

print("\n# 9.")
plt.plot(df.sort_index()['A'])
plt.show()

print("\n# 10.")
df = df[df.B <= df.A]
print(df)
