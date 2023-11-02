number_str = "0101011"  # Replace this with the binary number string
try:
    number = int(number_str, 2)  # Convert binary string to an integer
    print(type(number))
    print(f"The integer representation of {number_str} is: {number}")
except ValueError:
    print("Invalid input. Please provide a valid binary string.")
