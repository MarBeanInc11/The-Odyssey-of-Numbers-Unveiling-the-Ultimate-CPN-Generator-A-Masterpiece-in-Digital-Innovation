import json
import logging
import secrets
from time import sleep

import requests

from constants import MAX_CPN_NUMBER, MIN_CPN_NUMBER
from luhn_algorithm import calculate_luhn_check_digit
from utils import is_valid_number

# Initialize logging
logging.basicConfig(filename='logs/cpn_generator.log', level=logging.INFO)


class CPNGenerator:

    def __init__(self):
        self.generated_cpn_numbers = set()

    def generate_random_cpn_number(self) -> int:
        cpn_number = secrets.SystemRandom().randint(MIN_CPN_NUMBER,
                                                    MAX_CPN_NUMBER)
        check_digit = calculate_luhn_check_digit(cpn_number)
        return cpn_number if check_digit == 0 else self.generate_random_cpn_number(
        )

    def generate_unique_random_cpn_number(self) -> int:
        cpn_number = self.generate_random_cpn_number()
        while cpn_number in self.generated_cpn_numbers:
            cpn_number = self.generate_random_cpn_number()
        self.generated_cpn_numbers.add(cpn_number)
        return cpn_number


def log_message(message: str, level: str = "info"):
    logging.log(getattr(logging, level.upper()), message)


def display_progress_bar(iteration, total, bar_length=50):
    progress = float(iteration) / float(total)
    arrow = '=' * int(round(progress * bar_length) - 1)
    spaces = ' ' * (bar_length - len(arrow))
    print(f'Progress: [{arrow + spaces}] {int(progress * 100)}%')


def audit_generated_cpn(cpn: int):
    with open('logs/audit_log.json', 'a') as f:
        json.dump({'generated_cpn': cpn}, f)
        f.write(",\n")


def notify_api_about_new_cpn(cpn: int):
    api_endpoint = "https://example.com/api/new_cpn"
    response = requests.post(api_endpoint, json={"cpn": cpn})
    if response.status_code == 200:
        log_message("Successfully notified the API.")
    else:
        log_message(
            f"Failed to notify the API. Status Code: {response.status_code}",
            level="error")


if __name__ == "__main__":
    cpn_gen = CPNGenerator()
    num_of_cpns_to_generate = 10  # You can change this number

    for i in range(1, num_of_cpns_to_generate + 1):
        try:
            cpn_number = cpn_gen.generate_unique_random_cpn_number()
            log_message(f"Generated CPN Number: {cpn_number}")

            is_valid = is_valid_number(cpn_number, calculate_luhn_check_digit)
            if is_valid:
                log_message("The CPN number is valid.")
                audit_generated_cpn(cpn_number)
                notify_api_about_new_cpn(cpn_number)
            else:
                log_message("The CPN number is not valid.", level="error")

            display_progress_bar(i, num_of_cpns_to_generate)
            sleep(0.1)  # Simulate some delay
        except Exception as e:
            log_message(str(e), level="error")
