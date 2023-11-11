def decimal_to_binary(number, num_bits):
    if number >= 0:
        # For non-negative numbers, convert to binary as usual
        binary_representation = bin(number)[2:]
    else:
        # For negative numbers, convert to binary using two's complement
        binary_representation = bin(2**num_bits + number)[2:]

    # Calculate the number of padding zeros needed
    padding_zeros = num_bits - len(binary_representation)

    # Add the necessary padding zeros to achieve the desired number of bits
    binary_with_padding = '0' * padding_zeros + binary_representation

    return binary_with_padding

# Example usage:
positive_example = decimal_to_binary(42, 32)
negative_example = decimal_to_binary(-42, 32)

def binary_to_decimal(number_str):
    if len(number_str) > 0 and number_str[0] == '1':
        # If the most significant bit is 1, indicating a negative number
        num_bits = len(number_str)
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in number_str[1:])
        decimal_value = -int(inverted_bits, 2) - 1
    else:
        # If the most significant bit is 0, indicating a non-negative number
        decimal_value = int(number_str, 2)

    return decimal_value

# Example usage:

print(f"Positive example: {positive_example}")
print(f"Negative example: {negative_example}")
print(binary_to_decimal(negative_example))


def decimal_to_binary(number, num_bits):
    # Convert the decimal number to binary
    binary_representation = bin(number)[2:]  # Remove '0b' prefix

    # Calculate the number of padding zeros needed
    padding_zeros = num_bits - len(binary_representation)

    # Add the necessary padding zeros to achieve the desired number of bits
    binary_with_padding = '0' * padding_zeros + binary_representation

    return binary_with_padding

def binary_to_decimal(number_str):
    if (len(number_str) > 30 and number_str[30:32] == "b1"):
        number_str = number_str[0:29] + "01"
    # print(number_str)
    number = int(number_str, 2)
    # print(number)
    return number