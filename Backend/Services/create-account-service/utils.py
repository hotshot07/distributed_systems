import random
import secrets 

generate_ten_digit_ids  = lambda: random.randint(10000000000, 99999999999)

#plaintext password generator to be returned to orchestrator 
generate_password = lambda : str(secrets.token_hex(4))


def get_id_and_passwords(n):
    id_and_passwords = []
    
    for _ in range(n):
        id_and_passwords.append({
            'Id': str(generate_ten_digit_ids()),
            'Password': generate_password()
        })
    return id_and_passwords