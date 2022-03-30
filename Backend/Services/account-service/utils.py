import random
import secrets


def generate_ten_digit_ids(): return random.randint(10000000000, 99999999999)

# plaintext password generator to be returned to orchestrator


def generate_password(): return str(secrets.token_hex(4))


def get_id_and_passwords(n):
    id_and_passwords = []

    for _ in range(n):
        id_and_passwords.append({
            'Id': str(generate_ten_digit_ids()),
            'Password': generate_password()
        })
    return id_and_passwords


def error_message(message):
    return dict(error=message)

def validate_country(country):
    l_country = country.split()
    if len(l_country) > 0:
        for idx, word in enumerate(l_country):
            if word.lower() in ['of', 'the', 'former', 'part']:
                l_country[idx] = word.lower()
            else:
                l_country[idx] = word.capitalize()
            f_county = ' '.join(l_country)
        country = f_county
    return country
