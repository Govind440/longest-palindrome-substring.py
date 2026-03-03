# Data_Type:
# 1. int
# 2. float
# 3. str
# 4. bool
# 5. list
# 6. tuple
# 7. set
# 8. dict
# 9. Sequence Types: list, tuple, range
# 10. Mapping Type: dict
# 11. Boolean Type: bool
# 12. Binary Types: bytes, bytearray, memoryview
# 1. int: Integer type, represents whole numbers without a fractional part.

# 1. int 
a = 10
print(type(a))  # Output: <class 'int'>
# 2. float: Floating-point type, represents real numbers with a
# fractional part.
b = 3.14
print(type(b))  # Output: <class 'float'>
# 3. str: String type, represents a sequence of characters.
c = "Hello, World!"
print(type(c))  # Output: <class 'str'>
d = ""
print(type(d))  # Output: <class 'str'>
# 4. bool: Boolean type, represents one of two values: True or
# False.
e = ""
print(bool(e))  # Output: False
f = "Hello"
print(bool(f))  # Output: True
g = 0
print(bool(g))  # Output: False
h = 1
print(bool(h))  # Output: True
i = 2
print(bool(i))  # Output: True
# 5. list: List type, represents an ordered collection of items
# that can be of different types.
j = [1, 2, 3, "four", 5.0]
print(bool(j))  # Output: True
k = []
print(bool(k))  # Output: False
# 6. tuple: Tuple type, represents an ordered collection of items
# that can be of different types, but is immutable (cannot be
# changed after creation).
tuple1 = (1, 2, 3, "four", 5.0)  
print(bool(tuple1))  # Output: True
m = (1, 2,)
print(bool(m))  # Output: True
n = ()
print(bool(n))  # Output: False
# 7. set: Set type, represents an unordered collection of unique
# items.
o = {1, 2, 3, "four", 5.0}
print(bool(o))  # Output: True
p = set()
print(bool(p))  # Output: False
# 8. dict: Dictionary type, represents a collection of key-value
# pairs.
q = {"name": "Alice", "age": 30, "city": "New York"}
print(bool(q))  # Output: True
r = {}
print(bool(r))  # Output: False
# 9. Sequence Types: list, tuple, range
s = [1, 2, 3]   
print(bool(s))  # Output: True
t = (1, 2, 3)
print(bool(t))  # Output: True
u = range(5)
print(bool(u))  # Output: True
# 10. Mapping Type: dict
v = {"key1": "value1", "key2": "value2"}
print(bool(v))  # Output: True
w = {}
print(bool(w))  # Output: False
# 11. Boolean Type: bool