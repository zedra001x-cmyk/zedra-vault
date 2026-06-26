import random
import string

def generate_password(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

def check_strength(password: str) -> dict:
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short (min 8 chars)")

    if len(password) >= 16:
        score += 1

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers")

    if any(c in "!@#$%^&*()" for c in password):
        score += 1
    else:
        feedback.append("Add special characters")

    levels = {6: "Strong", 5: "Strong", 4: "Medium", 3: "Weak", 2: "Weak", 1: "Very Weak", 0: "Very Weak"}
    return {
        "score": score,
        "level": levels[score],
        "feedback": feedback
    }
