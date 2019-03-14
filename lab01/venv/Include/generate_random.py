import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

N = 1000
index = pd.date_range('2000-1-1', periods=N, freq='B')
data = (np.random.random(N, 1)-0.5).cumsum(axis=0)
df = pd.DataFrame(data, index=index, columns=['price'])
print(df)
df.plot()
plt.show()
