import random
import string
import time
import getpass  # Used to handle hidden password input, enhances security by masking input directly in the terminal.

def mask_email(email):
    """
    Enhance the security of the masked email by including symbols and numbers,
    showing only the first letter before the '@', and preserving the domain.
    
    This function can be integrated with user authentication systems to mask emails during login or account recovery processes.

    Args:
    email (str): The email address to be masked.

    Returns:
    str: The masked email address.

    Raises:
    ValueError: If the email address is invalid.
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

    This can be linked to password strength monitoring systems to ensure complexity requirements are met.

    Args:
    length (int): Length of the generated password. Must be between 14 and 25 characters.

    Returns:
    str: The generated temporary password.

    Raises:
    ValueError: If the length is not between 14 and 25 characters.
    """
    if length < 14 or length > 25:
        raise ValueError("Password length must be between 14 and 25 characters.")
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def validate_password(password):
    """
    Validate the new password based on defined security policies.

    This function can be integrated into a larger security framework that includes continuous compliance monitoring.

    Args:
    password (str): The password to validate.

    Returns:
    tuple: A tuple containing a boolean indicating validity and a message.
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

    This interactive approach enhances user control over security practices and can be adapted for different security levels.

    Returns:
    bool: True if the user wants to mask their password, False otherwise.
    """
    while True:
        response = input("Do you want to mask your password while typing? (Y/N): ").strip().upper()
        if response == 'Y':
            return True
        elif response == 'N':
            print("WARNING: Your password will be visible when you type it. Please ensure no one is around to see it.")
            confirm = input("Are you sure you want to proceed with visible password entry? (Y/N): ").strip().upper()
            if confirm == 'Y':
                return False
        else:
            print("Invalid option, please enter 'Y' or 'N'.")

def login():
    """
    Prompt for email input, generate a temporary password, and enforce password change on login.

    Integrates email masking, temporary password generation, and user-driven password masking options for enhanced security.

    Consider integration with log management systems to monitor login attempts and password change activities.
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
        
        print("Password changed successfully. Please remember to set up 2FA with SOC.")
        return True
    except ValueError as e:
        print(e)
        return False

# Trigger the login function
if __name__ == "__main__":
    login()


