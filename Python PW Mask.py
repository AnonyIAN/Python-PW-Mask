import random
import string
import time
import getpass  # Used to handle hidden password input

def mask_email(email):
    """
    Enhance the security of the masked email by including symbols and numbers,
    showing only the first letter before the '@', and preserving the domain.
    """
    if '@' not in email:
        raise ValueError("Invalid email address.")
    user_part, domain_part = email.split('@')
    mask_length = max(4, len(user_part) - 1)
    mask = ''.join(random.choice(string.digits + "!@#$%^&*()_+") for _ in range(mask_length))
    masked_user = user_part[0] + mask
    masked_email = f"{masked_user}@{domain_part}"
    return masked_email

def generate_temp_password(length):
    """
    Generate a random password of specified length, containing letters, digits, and symbols.
    """
    if length < 14 or length > 25:
        raise ValueError("Password length must be between 14 and 25 characters.")
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def validate_password(password):
    """
    Validate the new password based on defined security policies.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must include at least one number."
    if not any(char.isupper() for char in password):
        return False, "Password must include at least one uppercase letter."
    return True, "Password is valid."

def ask_password_masking():
    """
    Ask user if they want to mask their new password.
    """
    response = input("Do you want to mask your password while typing? (Y/N): ").strip().upper()
    if response == 'Y':
        return True
    elif response == 'N':
        print("WARNING: Your password will be visible when you type it. Please ensure no one is around to see it.")
        confirm = input("Are you sure you want to proceed with visible password entry? (Y/N): ").strip().upper()
        return False if confirm == 'Y' else True  # If they are not sure, fallback to masking
    else:
        print("Invalid option, defaulting to masked input.")
        return True

def login():
    """
    Prompt for email input, generate a temporary password, and enforce password change on login.
    """
    email = input("Please enter your email address: ")
    try:
        masked_email = mask_email(email)
        temp_password = generate_temp_password(random.randint(14, 25))
        print(f"Login attempt with masked email: {masked_email}")
        print(f"Your temporary password is: {temp_password} (Expires in 5 minutes)")

        mask_password = ask_password_masking()
        if mask_password:
            new_password = getpass.getpass("Please enter your new password within 5 minutes: ")
        else:
            new_password = input("Please enter your new password within 5 minutes: ")

        session_start = time.time()

        if time.time() - session_start > 300:
            print("Session expired, please log in again.")
            return False

        # Validate and handle the new password
        valid, message = validate_password(new_password)
        if not valid:
            print(message)
            return False
        
        print("Password changed successfully. Please remember to set up 2FA.")
        return True
    except ValueError as e:
        print(e)
        return False

# Trigger the login function
login()
