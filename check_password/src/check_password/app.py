import re
import random
import string
import streamlit as st

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
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")
    st.title("🔐 Password Strength Meter")
    st.write("Check how secure your password is and get suggestions to improve it.")
    
    password = st.text_input("Enter your password:", type="password")
    
    if st.button("Check Strength"):
        if password:
            strength, feedback = check_password_strength(password)
            st.subheader(f"Password Strength: {strength}")
            
            if strength == "Weak":
                st.warning("Your password is weak. Consider the following improvements:")
                for tip in feedback:
                    st.write(f"- {tip}")
                st.write("### Suggested Strong Password:")
                st.code(suggest_strong_password(), language='plaintext')
            elif strength == "Strong":
                st.success("Great job! Your password is strong.")
        else:
            st.error("Please enter a password.")
    
if __name__ == "__main__":
    main()
