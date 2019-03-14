import numpy as np
import random

a = np.random.randint(low=1, high=10, size=10)
b = np.random.randint(low=1, high=10, size=10)
print("\n# 1. Sumuojam du vektorius")
print(a)
print(b)
array_sum = np.add(a, b)
print(array_sum)
print(np.sum(np.add(a, b)))

print("\n# 2. Anuliuojam teigiamus elementus")
a = np.random.randint(low=-10, high=10, size=10)
print(a)
a[a > 0] = 0
print(a)

print("\n# 3. Išmetam elementus, didesnius už 6")
a = np.random.randint(low=-10, high=10, size=10)
print(a)
a = a[a <= 6]
print(a)

print("\n# 4. Randam vienodus šalia esančius elementus")
a = np.random.randint(low=-10, high=10, size=10)
print(a)
print(np.where(a[1:] == a[:-1]))

print("\n# 5. randam elementus, kur a didesnis už b")
a = np.random.randint(low=-10, high=10, size=10)
b = np.random.randint(low=-10, high=10, size=10)
print(a)
print(b)
print(a[a > b])
print(np.where(a > b))

print("\n# 6. pastumiam elementus, kartojam paskutinį")
a = np.random.randint(low=-10, high=10, size=10)
print(a)
a[:-1] = a[1:]
print(a)

print("\n# 7. keičiam elementų tvarką")
a = np.random.randint(low=-10, high=10, size=10)
print(a)
a = np.flip(a)
print(a)

print("\n# 8. užnulinam kas antrą elementą")
a = np.random.randint(low=-10, high=10, size=10)
print(a)
a[::2] = 0
print(a)

print("\n# 9. randam matricos eilučių vidurkius")
a = np.random.randint(low=-10, high=10, size=(10, 10))
print(a)
print(a.mean(1))

print("\n% 10. gaunam matricos diagonalinius elementus")
a = np.random.randint(low=-10, high=10, size=(10, 10))
print(a)
print(a.flat[::(np.take(a.shape, 1)+1)])
print(a.flat[9::(np.take(a.shape, 1)-1)])
