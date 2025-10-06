import streamlit as st
import requests
import time

# Page configuration
st.set_page_config(
    page_title="Nanobot AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Clean, professional CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .chat-message {
        padding: 1.25rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    .user-message {
        background-color: #f3f4f6;
        border-left: 4px solid #3b82f6;
    }
    .bot-message {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 4px solid #10b981;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .message-header {
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .input-container {
        background-color: #f9fafb;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
    .stButton button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: background-color 0.2s;
    }
    .stButton button:hover {
        background-color: #2563eb;
    }
    .tech-pill {
        display: inline-block;
        background-color: #e0e7ff;
        color: #3730a3;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.1rem;
    }
    .clear-btn {
        background-color: #6b7280 !important;
    }
    .clear-btn:hover {
        background-color: #4b5563 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_url" not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

# Header
st.markdown('<h1 class="main-title">🤖 Nanobot AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent documentation assistant for Python web frameworks</p>', unsafe_allow_html=True)

# Tech stack pills
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="tech-pill">Flask</span>
        <span class="tech-pill">FastAPI</span>
        <span class="tech-pill">Streamlit</span>
        <span class="tech-pill">Python</span>
        <span class="tech-pill">AI</span>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-header">👤 You</div>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="message-header">🤖 Nanobot</div>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# Input section
st.markdown("### 💬 Ask a question")

with st.form("chat_form", clear_on_submit=True):
    query = st.text_area(
        " ",
        placeholder="Example: How do I create a basic Flask app? Or: What's the difference between FastAPI and Flask?",
        height=80,
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        submitted = st.form_submit_button("🚀 Send Message", use_container_width=True)
    with col2:
        clear_chat = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)

if clear_chat:
    st.session_state.messages = []
    st.rerun()

if submitted and query:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Create a placeholder for the response
    with st.spinner("🤖 Nanobot is thinking..."):
        try:
            # Make API call to backend
            response = requests.post(
                f"{st.session_state.api_url}/chat", 
                json={"query": query}, 
                timeout=30
            )
            
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = "Sorry, I encountered an error while processing your request. Please try again."
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
        except requests.exceptions.ConnectionError:
            error_msg = "⚠️ Cannot connect to the backend server. Please make sure it's running on localhost:8000"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        except requests.exceptions.Timeout:
            error_msg = "⏰ Request timed out. Please try again."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        except Exception as e:
            error_msg = f"❌ An unexpected error occurred: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    st.rerun()

# Sidebar for settings
with st.sidebar:
    st.title("Settings")
    
    st.markdown("### Configuration")
    api_url = st.text_input(
        "Backend API URL",
        value=st.session_state.api_url,
        help="URL where your FastAPI backend is running"
    )
    st.session_state.api_url = api_url
    
    st.markdown("---")
    st.markdown("### About")
    st.write("""
    **Nanobot AI** helps you find answers about:
    - Flask documentation
    - FastAPI features
    - Streamlit components
    - Python web development
    """)
    
    st.markdown("### Examples")
    st.caption("Try asking:")
    st.code("How do I handle POST requests in Flask?")
    st.code("What are FastAPI dependencies?")
    st.code("How to create interactive plots in Streamlit?")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>"
    "Built with ❤️ using Streamlit & FastAPI • Nanobot AI • Suyash"
    "</div>",
    unsafe_allow_html=True
)