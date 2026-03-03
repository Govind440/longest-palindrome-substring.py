# 1. Arithmetic Operators
# addition, subtraction, multiplication, division, modulus,
# exponentiation, floor division
# 1. Addition
a = 10
b = 5
result = a + b
print(result)
# 2. Subtraction
result = a - b
print(result)
# 3. Multiplication
result = a * b
print(result)
if __name__ == "__main__":
    # 4. Division
    result = a / b
    print(result)
    # 5. Modulus
    result = a % b
    print(result)
    # 6. Exponentiation
    result = a ** b
    print(result)
    # 7. Floor Division
    result = a // b
    print(result)
    
    # 2. Comparison Operators
    # equal to, not equal to, greater than, less than,
    # greater than or equal to, less than or equal to
    # 1. Equal to
    result = a == b
    print(result)
    # 2. Not equal to
    result = a != b
    print(result)
    # 3. Greater than
    result = a > b
    print(result)
    # 4. Less than
    result = a < b
    print(result)
    # 5. Greater than or equal to
    result = a >= b
    print(result)
    # 6. Less than or equal to
    result = a <= b
    print(result)
    # 3. Logical Operators
    # and, or, not
    x = True
    y = False
    # 1. And
    result = x and y
    print(result)
    # 2. Or
    result = x or y
    print(result)
    # 3. Not
    result = not x
    print(result)
    
    # 4. Assignment Operators
    # =, +=, -=, *=, /=, %=, **=, //=
    # 1. Assignment
    c = 10
    print(c)
    # 2. Add and assign
    c += 5
    print(c)
    # 3. Subtract and assign
    c -= 3
    print(c)
    # 4. Multiply and assign
    c *= 2
    print(c)
    # 5. Divide and assign
    print(c)
    c /= 4
    print(c)
    # 6. Modulus and assign
    c %= 3
    print(c)
    # 7. Exponentiation and assign
    c **= 2
    print(c)
    # 8. Floor division and assign
    c //= 2
    c %= 4
    print(c)
    
    # 5. Bitwise Operators
    # and, or, xor, not, left shift, right shift
    m = 5  # 0101 in binary
    n = 3  # 0011 in binary
    # 1. Bitwise AND
    result = m & n
    print(result)
    # 2. Bitwise OR
    result = m | n
    print(result)
    m = 5
    n = 3
    # 3. Bitwise XOR
    result = m ^ n
    print(result)
    print(m)
    # 4. Bitwise NOT
    result = ~m
    print(result)
    # 5. Left shift
    result = m << 1
    print(result)
    # 6. Right shift
    result = m >> 1
    print(result)
    
    # 6. Identity Operators
    # is, is not
    p = [1, 2, 3]
    q = [1, 2, 3]
    # 1. Identity
    result = p is q
    print(result)
    # 2. Not identity
    result = p is not q
    print(result)
    # 7. Membership Operators
    # in, not in
    s = "Hello, World!"
    # 1. Membership
    result = "Hello" in s
    print(result)
    # 2. Not membership
    result = "Python" not in s
    print(result)
    