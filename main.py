"""
RBAC Chatbot - Role-Based Access Control Chatbot with Vector Database Integration
Simple, clean ChatGPT-style interface
"""

import streamlit as st
import time
from utils import authenticate, get_all_roles
from langgraph_workflow import get_workflow

# Page configuration
st.set_page_config(
    page_title="RBAC Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ChatGPT-style interface
def apply_custom_css():
    st.markdown("""
    <style>
    /* Global Styling */
    .main {
        background-color: #f0f2f6;
        padding: 0;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    
    /* Login Container */
    .login-container {
        background: white;
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 2rem auto;
        max-width: 400px;
        text-align: center;
    }
    
    .login-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 2rem;
    }
    
    /* Chat Container */
    .chat-container {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        padding: 1rem;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Welcome Header */
    .welcome-header {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* Chat Messages */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin: 1rem 0;
    }
    
    .user-bubble {
        background-color: #d4f4dd;
        color: #1f2937;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        max-width: 70%;
        font-weight: 500;
        line-height: 1.5;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .assistant-message {
        display: flex;
        justify-content: flex-start;
        margin: 1rem 0;
    }
    
    .assistant-bubble {
        background-color: #eeeeee;
        color: #1f2937;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        max-width: 70%;
        line-height: 1.5;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Input Area */
    .input-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-top: 1rem;
        position: sticky;
        bottom: 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: #10b981;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #059669;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    /* Text Input */
    .stTextInput input {
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        border: 2px solid #e5e7eb;
        border-radius: 10px;
    }
    
    /* Loading Spinner */
    .loading-message {
        background-color: #eeeeee;
        color: #1f2937;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        max-width: 70%;
        line-height: 1.5;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        font-style: italic;
        opacity: 0.8;
    }
    
    /* Logout Button */
    .logout-btn {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    /* Hide default Streamlit elements and reduce top padding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none;}
    .stApp > div:first-child {margin-top: 0 !important;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    
    /* Hide empty text input elements */
    .stTextInput[data-testid="stTextInput-RootElement"]:has(input[value=""]) {
        display: none !important;
    }
    
    /* Target specific empty divs */
    .stApp > div > div > div:empty {
        display: none !important;
    }
    
    /* Hide any standalone empty containers */
    .element-container:empty {
        display: none !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

def render_login_page():
    """Render the login page"""
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Login to RBAC Chatbot</div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        role = st.selectbox("Role", get_all_roles())
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            login_button = st.form_submit_button("Login", use_container_width=True)
    
    # Demo credentials info
    with st.expander("📋 Demo Credentials"):
        st.markdown("""
        **Quick Login Options:**
        - Username: `alice` | Password: `123` | Role: HR
        - Username: `bob` | Password: `123` | Role: Finance  
        - Username: `charlie` | Password: `123` | Role: Engineering
        - Username: `diana` | Password: `123` | Role: Marketing
        - Username: `eve` | Password: `123` | Role: Employee
        - Username: `frank` | Password: `123` | Role: C-Level
        """)
    
    if login_button:
        if username and password and role:
            user_info = authenticate(username, password, role)
            if user_info:
                # Store user session
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_name = user_info["name"]
                st.session_state.role = user_info["role"]
                st.session_state.messages = []
                st.rerun()
            else:
                st.error("❌ Invalid credentials or user does not exist. Please check your username, password, and role.")
        else:
            st.error("❌ Please fill in all fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat_message(message, is_user=True):
    """Render a chat message bubble"""
    if is_user:
        st.markdown(f'''
        <div class="user-message">
            <div class="user-bubble">
                {message}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="assistant-message">
            <div class="assistant-bubble">
                {message}
            </div>
        </div>
        ''', unsafe_allow_html=True)

def render_loading_message():
    """Show loading message while processing"""
    st.markdown(f'''
    <div class="assistant-message">
        <div class="loading-message">
            🔍 Searching knowledge base and generating response...
        </div>
    </div>
    ''', unsafe_allow_html=True)

def get_rag_response(query, role, user_name):
    """Get response from RAG system"""
    try:
        workflow = get_workflow()
        
        # Get user ID (simplified for demo)
        user_id_map = {
            "alice": 1, "bob": 2, "charlie": 10, "diana": 4, "eve": 5, "frank": 6
        }
        user_id = user_id_map.get(st.session_state.username, 1)
        
        # Process query through workflow
        result = workflow.process_query(
            user_role=role,
            user_id=user_id,
            user_name=user_name,
            query=query
        )
        
        return result.get('response', f"I received your query '{query}' as a {role}. Let me help you with that based on our knowledge base.")
        
    except Exception as e:
        st.error(f"Error processing query: {str(e)}")
        return f"I received your query '{query}' as a {role}. I'm currently experiencing some technical difficulties, but I'm here to help you."

def render_chat_interface():
    """Render the main chat interface"""
    # Logout button
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🚪 Logout", key="logout"):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    # Welcome header
    st.markdown(f'''
    <div class="welcome-header">
        🧠 Welcome, {st.session_state.user_name} ({st.session_state.role})
    </div>
    ''', unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.messages:
            render_chat_message(message["content"], message["role"] == "user")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Message", 
                placeholder="Type your message here...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.form_submit_button("Send", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process message when submitted
    if send_button and user_input.strip():
        # Add user message to session state
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Show loading message temporarily
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            render_loading_message()
        
        # Get response from RAG system
        response = get_rag_response(
            query=user_input,
            role=st.session_state.role,
            user_name=st.session_state.user_name
        )
        
        # Clear loading message
        loading_placeholder.empty()
        
        # Add assistant response to session state
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response
        })
        
        # Rerun to update the interface with new messages
        st.rerun()

def main():
    """Main application"""
    apply_custom_css()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Route to appropriate page
    if not st.session_state.logged_in:
        render_login_page()
    else:
        render_chat_interface()

if __name__ == "__main__":
    main()
# streamlit run main.py --server.address 127.0.0.1 --server.port 5000