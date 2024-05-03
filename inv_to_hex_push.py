#!/usr/bin/python

import sys

def string_to_reversed_hex(s):
    # Convert the string to hexadecimal
    hex_string = s.encode().hex()

    # Calculate the required padding
    padding_length = (4 - len(s) % 4) % 4
    padded_hex_string = hex_string + '00' * padding_length

    # Reverse the order of bytes
    reversed_hex = ''.join(reversed([padded_hex_string[i:i+2] for i in range(0, len(padded_hex_string), 2)]))

    return reversed_hex

def split_into_four_byte_groups(hex_str):
    # Split the hexadecimal string into 4-byte groups
    groups = [hex_str[i:i+8] for i in range(0, len(hex_str), 8)]

    return groups

def negate_hex_value(hex_value):
    # Convert hex to integer, negate it, and get the two's complement
    negated_int_value = (int(hex_value, 16) ^ 0xFFFFFFFF) + 1
    # Format back to hex
    negated_hex_value = hex(negated_int_value & 0xFFFFFFFF)
    return negated_hex_value

def generate_assembly_commands(groups):
    commands = []

    # Check if the first bytes of the first group are NULL bytes and handle accordingly
    first_group = groups[0]
    first_bytes_are_null = any(byte == '00' for byte in [first_group[i:i+2] for i in range(0, len(first_group), 2)])

    if first_bytes_are_null:
        # Remove leading '00' bytes
        while first_group.startswith('00'):
            first_group = first_group[2:]
        
        # If all bytes were '00', adjust the first group to a single '00'
        if not first_group:
            first_group = '00'
        
        # Calculate the negated value
        negated_value = negate_hex_value(first_group)
        commands.append(f"mov eax, {negated_value}")
        commands.append("neg eax")
        commands.append("push eax")
        groups = groups[1:]  # Remove the first group as it's handled differently
    else:
        commands.append(f"push 0x{first_group}")
        groups = groups[1:]  # Remove the first group as it's already handled

    # Handle the remaining groups
    for group in groups:
        commands.append(f"push 0x{group}")

    return commands

# Example of use
input_string = sys.argv[1]
result = string_to_reversed_hex(input_string)
print(f'Original string: {input_string}')
print(f'String in reversed hexadecimal: {result}')

groups = split_into_four_byte_groups(result)

print(f'4-byte groups: {groups}')
print()
print("Assembly commands:")
assembly_commands = generate_assembly_commands(groups)
for command in assembly_commands:
    print(command)

