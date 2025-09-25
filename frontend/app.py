import streamlit as st
import requests
import time

# Page configuration
st.set_page_config(
    page_title="Nanobot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for greenish theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .course-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #F8FFF8;
        border: 1px solid #90EE90;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(46, 139, 87, 0.1);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    .user-message {
        background-color: #2E8B57;
        color: white;
        margin-left: auto;
    }
    .bot-message {
        background-color: #F0FFF0;
        color: #2D2D2D;
        border: 1px solid #90EE90;
        margin-right: auto;
    }
    .normal-button {
        background-color: #2E8B57 !important;
        color: white !important;
        border: 1px solid #2E8B57 !important;
        border-radius: 5px !important;
    }
    .normal-button:hover {
        background-color: #3CB371 !important;
        border-color: #3CB371 !important;
    }
    .secondary-button {
        background-color: #F8FFF8 !important;
        color: #2E8B57 !important;
        border: 1px solid #2E8B57 !important;
        border-radius: 5px !important;
    }
</style>
""", unsafe_allow_html=True)

# Backend configuration
BACKEND_URL = "http://127.0.0.1:8000"

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'current_course' not in st.session_state:
    st.session_state.current_course = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}
if 'show_docs' not in st.session_state:
    st.session_state.show_docs = False

def test_backend_connection():
    """Test if backend is reachable"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def ask_question(question):
    """Send question to backend"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/ask",
            params={"question": question},
            timeout=30
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}", "success": False}

def home_page():
    """Display the home page with course selection"""
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="main-header">🤖 Nanobot</div>', unsafe_allow_html=True)
        st.markdown("### Interactive Learning Platform")
    
    # Minimal information with expandable docs
    if not st.session_state.show_docs:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📚 View Documentation", use_container_width=True):
                st.session_state.show_docs = True
                st.rerun()
    
    # Documentation section (hidden by default)
    if st.session_state.show_docs:
        with st.expander("📚 Documentation", expanded=True):
            st.markdown("""
            ### How It Works:
            
            **Learn any technology through intelligent conversations** with AI tutors trained on official documentation.
            
            **🚀 Getting Started:**
            1. Select a course from available technologies
            2. Chat with the AI tutor specialized in that technology
            3. Get accurate answers based on official documentation
            4. Learn at your own pace with instant feedback
            
            **📚 Current Features:**
            - Flask documentation chatbot
            - Real-time question answering
            - Conversation history
            - Clean, intuitive interface
            
            *More courses coming soon!*
            """)
            
            if st.button("❌ Close Documentation", use_container_width=True):
                st.session_state.show_docs = False
                st.rerun()
    
    st.markdown("---")
    
    # Course selection
    st.subheader("🎯 Available Courses")
    
    courses = [
        {
            "id": "flask",
            "name": "Flask Documentation",
            "description": "Learn Flask web framework with our AI tutor trained on official Flask documentation.",
            "icon": "🚀",
            "status": "active"
        }
    ]
    
    for course in courses:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="course-card">
                    <h3>{course['icon']} {course['name']}</h3>
                    <p>{course['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if course['status'] == 'active':
                    if st.button("Start Learning", key=course['id'], use_container_width=True):
                        st.session_state.current_course = course['id']
                        st.session_state.page = 'chat'
                        st.rerun()
                else:
                    st.button("Coming Soon", key=course['id'], disabled=True, use_container_width=True)

def chat_interface():
    """Display the chat interface"""
    # Header
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown('<div class="main-header">💬 Flask Learning</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("← Back to Courses", use_container_width=True):
            st.session_state.page = 'home'
            st.session_state.current_course = None
            st.rerun()
    
    st.info("💡 Ask me anything about Flask! I'm trained on official Flask documentation.")
    
    # Initialize chat history
    course_id = st.session_state.current_course
    if course_id not in st.session_state.chat_history:
        st.session_state.chat_history[course_id] = []
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history[course_id]:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>AI Tutor:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    question = st.chat_input("Ask your question about Flask...")
    
    if question:
        # Add user message to chat history
        st.session_state.chat_history[course_id].append({
            'role': 'user',
            'content': question
        })
        
        # Display user message immediately
        with chat_container:
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {question}
            </div>
            """, unsafe_allow_html=True)
        
        # Get AI response
        with st.spinner("🤔 Thinking..."):
            response = ask_question(question)
        
        # Display AI response
        if response.get('success'):
            answer = response['answer']
            st.session_state.chat_history[course_id].append({
                'role': 'assistant',
                'content': answer
            })
            
            with chat_container:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>AI Tutor:</strong> {answer}
                </div>
                """, unsafe_allow_html=True)
        else:
            error_msg = response.get('error', 'Unknown error occurred')
            st.error(f"❌ Error: {error_msg}")
        
        # Auto-scroll to bottom
        st.rerun()
    
    # Chat controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.chat_history[course_id] = []
            st.rerun()
    
    with col2:
        if st.button("💡 Example Question", use_container_width=True):
            st.info("Try asking: 'What is Flask and how do I create a basic app?'")

def main():
    """Main application logic"""
    
    # Sidebar - Minimal version
    with st.sidebar:
        st.title("🤖 Nanobot")
        st.markdown("---")
        
        # Only show essential info
        st.subheader("Quick Info")
        st.markdown("""
        **Current Course:**
        - Flask Documentation
        
        **Status:** Active
        """)
        
        st.markdown("---")
        
        # Simple controls
        if st.button("🔄 Restart Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.button("📚 Toggle Docs", use_container_width=True):
            st.session_state.show_docs = not st.session_state.show_docs
            st.rerun()
    
    # Main content area
    if st.session_state.page == 'home' or st.session_state.current_course is None:
        home_page()
    else:
        chat_interface()

if __name__ == "__main__":
    main()