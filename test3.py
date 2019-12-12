import numpy as np
from decimal import Decimal

"""
a = np.array([1,0],dtype=np.uint8)
b = np.array([0],dtype=np.uint8)
c = np.array([],dtype=np.uint8)

if a != c:
    d = np.bitwise_xor(a,b)
else:
    d = np.array([6])

print(d)
"""

"""
a = 3
a = float(a)
print(np.reciprocal(a))
"""

num1 = Decimal('0.1')
num2 = Decimal('0.5')
print(num1 + num2)

a = 0.24347177319074853
b = 4.107252298263535
aa = str(a)
bb = str(b)
da = Decimal(aa)
db = Decimal(bb)
print(da * db)
print(Decimal(1.00/2.00))