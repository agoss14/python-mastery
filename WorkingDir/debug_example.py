# debug_example.py

# def calculate_factorial(n):
#     if n == 0:
#         return 1
#     return n * calculate_factorial(n - 1)

# def main():
#     number = 5  # You can change this number
#     result = calculate_factorial(number)
#     print(f"The factorial of {number} is {result}")

# if __name__ == "__main__":
#     main()

prices = {
'ACME' : 513.25,
'SPAM' : 42.1
}

prices['SPAM'] += 12.2

print(prices.get('SPAM'))