import sqlite3
import bcrypt
import os
from datetime import datetime

DATABASE_FILE = "app_database.db"

def init_database():
    """Initialize the database with users and chat history tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create chat history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Create conversation sessions table for enhanced memory
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT NOT NULL,
            context_summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Insert dummy users if they don't exist
    create_dummy_users(cursor)
    
    conn.commit()
    conn.close()

def create_dummy_users(cursor):
    """Create dummy users for testing (3 users per role)"""
    dummy_users = [
        # HR Users
        ("Alice Johnson", "alice.johnson@company.com", "password123", "HR"),
        ("Bob Smith", "bob.smith@company.com", "password123", "HR"),
        ("Carol Wilson", "carol.wilson@company.com", "password123", "HR"),
        
        # Finance Users
        ("David Brown", "david.brown@company.com", "password123", "Finance"),
        ("Emma Davis", "emma.davis@company.com", "password123", "Finance"),
        ("Frank Miller", "frank.miller@company.com", "password123", "Finance"),
        
        # Employee Users
        ("Grace Lee", "grace.lee@company.com", "password123", "Employee"),
        ("Henry Taylor", "henry.taylor@company.com", "password123", "Employee"),
        ("Ivy Anderson", "ivy.anderson@company.com", "password123", "Employee"),
        
        # Engineering Users
        ("Jack Wilson", "jack.wilson@company.com", "password123", "Engineering"),
        ("Kate Martinez", "kate.martinez@company.com", "password123", "Engineering"),
        ("Liam Garcia", "liam.garcia@company.com", "password123", "Engineering"),
        
        # Marketing Users
        ("Mia Rodriguez", "mia.rodriguez@company.com", "password123", "Marketing"),
        ("Noah Thompson", "noah.thompson@company.com", "password123", "Marketing"),
        ("Olivia White", "olivia.white@company.com", "password123", "Marketing"),
        
        # C-Level Users
        ("Tony Sharma", "tony.sharma@company.com", "password123", "C-Level"),
        ("Sarah Johnson", "sarah.johnson@company.com", "password123", "C-Level"),
        ("Michael Chen", "michael.chen@company.com", "password123", "C-Level"),
    ]
    
    for name, email, password, role in dummy_users:
        try:
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone() is None:
                # Hash password
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    "INSERT OR IGNORE INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                    (name, email, password_hash, role)
                )
        except Exception as e:
            # Skip if user already exists or other error
            continue

def authenticate_user(email, password):
    """Authenticate user credentials"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, email, password_hash, role FROM users WHERE email = ?", (email,))
    user_data = cursor.fetchone()
    
    conn.close()
    
    if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[3]):
        return {
            'id': user_data[0],
            'name': user_data[1],
            'email': user_data[2],
            'role': user_data[4]
        }
    return None

def update_user_role(user_id, new_role):
    """Update user's role"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()

def save_chat_message(user_id, message, response):
    """Save chat message and response to database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO chat_history (user_id, message, response) VALUES (?, ?, ?)",
        (user_id, message, response)
    )
    
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=50):
    """Get chat history for a user"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT message, response, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    
    history = cursor.fetchall()
    conn.close()
    
    return list(reversed(history))  # Return in chronological order

def get_conversation_context(user_id, limit=10):
    """Get recent conversation context for memory"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT message, response FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    
    history = cursor.fetchall()
    conn.close()
    
    # Format for conversation context
    context = []
    for message, response in reversed(history):
        context.append(f"User: {message}")
        context.append(f"Assistant: {response}")
    
    return "\n".join(context)

def save_conversation_session(user_id, session_id, context_summary):
    """Save conversation session summary"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO conversation_sessions 
        (user_id, session_id, context_summary, updated_at) 
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    """, (user_id, session_id, context_summary))
    
    conn.commit()
    conn.close()

def get_conversation_session(user_id, session_id):
    """Get conversation session summary"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT context_summary FROM conversation_sessions WHERE user_id = ? AND session_id = ?",
        (user_id, session_id)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else ""
