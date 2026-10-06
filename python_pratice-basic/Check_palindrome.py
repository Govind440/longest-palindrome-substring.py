# check palindrome or not


# def is_palindrome(n):
# num = n
# result = 0
# while num > 0:
# digit = num % 10
# result = result * 10 + digit
# num = num // 10
# return n == result

text = input("Enter a number or string: ")

if text == text[::-1]:
    print("Palindrome")
else:
    print("Not a Palindrome")
