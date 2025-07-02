"""
Utility functions for RBAC Chatbot
"""

# Dummy user database
USER_DATABASE = {
    "alice@company.com": {"password": "password123", "role": "HR", "name": "Alice Johnson"},
    "bob@company.com": {"password": "password123", "role": "Finance", "name": "Bob Smith"},
    "charlie@company.com": {"password": "password123", "role": "Engineering", "name": "Charlie Brown"},
    "diana@company.com": {"password": "password123", "role": "Marketing", "name": "Diana Wilson"},
    "eve@company.com": {"password": "password123", "role": "Employee", "name": "Eve Davis"},
    "frank@company.com": {"password": "password123", "role": "C-Level", "name": "Frank Miller"},
    
    # Simple username versions
    "alice": {"password": "123", "role": "HR", "name": "Alice Johnson"},
    "bob": {"password": "123", "role": "Finance", "name": "Bob Smith"},
    "charlie": {"password": "123", "role": "Engineering", "name": "Charlie Brown"},
    "diana": {"password": "123", "role": "Marketing", "name": "Diana Wilson"},
    "eve": {"password": "123", "role": "Employee", "name": "Eve Davis"},
    "frank": {"password": "123", "role": "C-Level", "name": "Frank Miller"},
}

def authenticate(username, password, role=None):
    """
    Authenticate user credentials with optional role validation
    Returns: dict with user info if valid, None if invalid
    """
    if username in USER_DATABASE:
        user_data = USER_DATABASE[username]
        if user_data["password"] == password:
            # If role is specified, validate it matches
            if role and user_data["role"] != role:
                return None
            return user_data
    return None

def get_all_roles():
    """Get list of all available roles"""
    return ["HR", "Finance", "Engineering", "Marketing", "Employee", "C-Level"]