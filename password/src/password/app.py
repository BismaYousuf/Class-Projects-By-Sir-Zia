import re
import random
import string

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Criteria checks
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Make your password at least 8 characters long.")
    
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Include at least one uppercase letter.")
    
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include at least one lowercase letter.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include at least one digit (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")
    
    # Scoring results
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"
    
    return strength, feedback

def suggest_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))

def main():
    password = input("Enter your password: ")
    strength, feedback = check_password_strength(password)
    print(f"Password Strength: {strength}")
    
    if strength == "Weak":
        print("Suggestions to improve your password:")
        for tip in feedback:
            print(f"- {tip}")
        print(f"Suggested Strong Password: {suggest_strong_password()}")
    elif strength == "Strong":
        print("Great job! Your password is strong.")
    
if __name__ == "__main__":
    main()
