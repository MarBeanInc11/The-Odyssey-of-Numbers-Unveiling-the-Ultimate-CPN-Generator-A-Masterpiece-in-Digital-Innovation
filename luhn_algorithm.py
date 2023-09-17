from typing import Union


def calculate_luhn_check_digit(number: Union[int, str]) -> int:
    """
    Calculates the Luhn check digit for a given number.
    
    Args:
        number (Union[int, str]): The number for which to calculate the check digit.
        
    Returns:
        int: The calculated check digit.
    """
    sum_of_digits = 0

    # Convert the number to a string and reverse it
    reversed_digits = reversed(str(number))

    # Enumerate through the reversed digits
    for idx, digit in enumerate(reversed_digits):
        n = int(digit)

        # Double every second digit starting from the right
        if idx % 2 == 1:
            n *= 2

            # Subtract 9 if the doubled value is greater than 9
            if n > 9:
                n -= 9

        sum_of_digits += n

    # Calculate the Luhn check digit
    check_digit = (10 - (sum_of_digits % 10)) % 10

    return check_digit
