import re
import math
import tkinter as tk
from hashlib import sha256

COMMON_PASSWORDS = {"123456", "password", "qwerty", "abc123", "letmein"}

def calculate_entropy(password):
    char_sets = [
        ("[a-z]", 26),  # Lowercase letters
        ("[A-Z]", 26),  # Uppercase letters
        ("[0-9]", 10),  # Digits
        ("[!@#$%^&*(),.?\":{}|<>]", 32),  # Special characters
    ]
    total_char_set_size = sum(size for pattern, size in char_sets if re.search(pattern, password))
    if total_char_set_size == 0:
        return 0
    entropy = len(password) * math.log2(total_char_set_size)
    return entropy


def check_patterns(password):
    if re.search(r"(.)\1{2,}", password):  # Repeated characters
        return "Avoid repeated characters (e.g., 'aaa')."
    if re.search(r"(123|abc|qwerty|asdf)", password.lower()):  # Sequential patterns
        return "Avoid common patterns (e.g., '123', 'qwerty')."
    return None


def is_common_password(password):
    hashed_password = sha256(password.encode()).hexdigest()
    return hashed_password in COMMON_PASSWORDS


def check_password_strength(password):

    entropy = calculate_entropy(password)
    

    if len(password) < 8:
        return "Weak: Password is too short.", "red"
    

    if is_common_password(password):
        return "Weak: This password is too common.", "red"
    
    pattern_feedback = check_patterns(password)
    if pattern_feedback:
        return f"Weak: {pattern_feedback}", "orange"
    
    if entropy < 40:
        return "Moderate: Increase complexity or length for better security.", "orange"
    elif entropy < 60:
        return "Strong: Your password is good.", "green"
    else:
        return "Very Strong: Your password is excellent!", "green"

def update_feedback(*args):
    password = password_var.get()
    feedback, color = check_password_strength(password)
    feedback_label.config(text=feedback, fg=color)


def main():
    global password_var, feedback_label

    root = tk.Tk()
    root.title("Sophisticated Password Strength Checker")

    tk.Label(root, text="Enter your password:").pack(pady=5)

    password_var = tk.StringVar()
    password_var.trace("w", update_feedback) 
    password_entry = tk.Entry(root, show="*", textvariable=password_var, width=30)
    password_entry.pack(pady=5)

    feedback_label = tk.Label(root, text="", font=("Helvetica", 12))
    feedback_label.pack(pady=10)

    root.geometry("800x200")
    root.mainloop()


if __name__ == "__main__":
    main()
