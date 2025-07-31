import streamlit as st
from utils import ask_llm, validate_input, COUNTRY_CODES
from prompts import GREETING_PROMPT, TECH_QUESTIONS_PROMPT, SYSTEM_CONTEXT
import os
import re

# --- Sidebar: Branding, Progress, Instructions ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.markdown("<h2 style='color:#4F8BF9;'>TalentScout</h2>", unsafe_allow_html=True)
    st.markdown("### Welcome to TalentScout!")
    total_steps = 8  # Updated to include the single tech question
    current_step = st.session_state.get('step', 0)
    st.progress(min(current_step, total_steps) / total_steps)
    st.markdown("#### Instructions")
    st.markdown("""
    - Answer each question step by step
    - Press Enter to submit
    - Your data is confidential
    """)

# --- Session State Initialization ---
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'candidate_data' not in st.session_state:
    st.session_state['candidate_data'] = {}
if 'step' not in st.session_state:
    st.session_state['step'] = 0
if 'current_field' not in st.session_state:
    st.session_state['current_field'] = None
if 'bot_message' not in st.session_state:
    st.session_state['bot_message'] = None
if 'input_key' not in st.session_state:
    st.session_state['input_key'] = 0
if 'country_code' not in st.session_state:
    st.session_state['country_code'] = '+91'  # Default to India
if 'conversation_complete' not in st.session_state:
    st.session_state['conversation_complete'] = False
if 'tech_question_asked' not in st.session_state:
    st.session_state['tech_question_asked'] = False

st.markdown("""
    <style>
    .stChatMessage.user {background: #e3f2fd; border-radius: 12px; padding: 10px; margin-bottom: 8px;}
    .stChatMessage.assistant {background: #f0f2f6; border-radius: 12px; padding: 10px; margin-bottom: 8px;}
    .st-emotion-cache-1kyxreq {padding-bottom: 0rem;}
    </style>
    """, unsafe_allow_html=True)

st.title('TalentScout – AI Hiring Assistant')

# --- Fields to Collect ---
FIELDS = [
    ('full_name', 'Full Name'),
    ('email', 'Email'),
    ('phone', 'Phone Number'),
    ('experience', 'Years of Experience'),
    ('position', 'Desired Position(s)'),
    ('location', 'Current Location'),
    ('tech_stack', 'Tech Stack (comma-separated)')
]

def get_bot_message():
    if st.session_state['step'] == 0:
        return ask_llm(GREETING_PROMPT, SYSTEM_CONTEXT)
    elif st.session_state['step'] <= len(FIELDS):
        field_name, field_display = FIELDS[st.session_state['step'] - 1]
        if field_name == 'phone':
            return f"Please select your country code and enter your {field_display.lower()}:"
        return f"Please provide your {field_display.lower()}:"
    elif st.session_state['step'] == len(FIELDS) + 1:
        # Generate single technical question
        tech_stack = st.session_state['candidate_data'].get('tech_stack', '')
        prompt = f"""Based on the candidate's tech stack: {tech_stack}
        
Generate ONE practical scenario-based technical question that tests their understanding.
Make it relevant to their tech stack and suitable for a hiring interview.
Return only the question, no formatting or headers."""
        return ask_llm(prompt, SYSTEM_CONTEXT)
    else:
        st.session_state['conversation_complete'] = True
        email = st.session_state['candidate_data'].get('email', '')
        phone = st.session_state['candidate_data'].get('phone', '')
        return f"Thanks for your interest and time. Our team will get back to you on your mail id {email} or phone {phone}."

def append_bot_message_once(bot_message):
    if not st.session_state['chat_history'] or st.session_state['chat_history'][-1]['role'] != 'bot' or st.session_state['chat_history'][-1]['content'] != bot_message:
        st.session_state['chat_history'].append({
            'role': 'bot',
            'content': bot_message
        })

def handle_user_input():
    # Extra safeguard: block all input if conversation is complete
    if st.session_state.get('conversation_complete', False):
        # Clear any pending input fields
        for k in list(st.session_state.keys()):
            if k.startswith('user_input_'):
                st.session_state[k] = ''
        return

    user_input = st.session_state.get(f'user_input_{st.session_state["input_key"]}', '')
    
    # Handle greeting step
    if st.session_state['step'] == 0:
        st.session_state['chat_history'].append({'role': 'user', 'content': user_input})
        st.session_state['step'] = 1
        st.session_state['bot_message'] = get_bot_message()
        append_bot_message_once(st.session_state['bot_message'])
        st.session_state['input_key'] += 1
        return

    # Handle field collection steps
    if st.session_state['step'] > 0 and st.session_state['step'] <= len(FIELDS):
        field_name, _ = FIELDS[st.session_state['step'] - 1]
        
        if field_name == 'phone':
            country_code = st.session_state['country_code']
            full_phone = f"{country_code}{user_input}"
            st.session_state['chat_history'].append({'role': 'user', 'content': f"{country_code} {user_input}"})
            is_valid, error_msg = validate_input('phone', full_phone, country_code=country_code)
            if is_valid:
                st.session_state['candidate_data']['phone'] = full_phone
                st.session_state['step'] += 1
                st.session_state['bot_message'] = get_bot_message()
            else:
                st.session_state['bot_message'] = f"Invalid input: {error_msg}. Please try again."
        else:
            st.session_state['chat_history'].append({'role': 'user', 'content': user_input})
            
            if field_name == 'email':
                is_valid, error_msg = validate_input('email', user_input)
            else:
                is_valid, error_msg = validate_input(field_name, user_input)
            
            if is_valid:
                st.session_state['candidate_data'][field_name] = user_input
                st.session_state['step'] += 1
                st.session_state['bot_message'] = get_bot_message()
            else:
                st.session_state['bot_message'] = f"Invalid input: {error_msg}. Please try again."
        
        append_bot_message_once(st.session_state['bot_message'])
        st.session_state['input_key'] += 1
        return

    # Handle technical question step
    if st.session_state['step'] == len(FIELDS) + 1:
        st.session_state['chat_history'].append({'role': 'user', 'content': user_input})
        st.session_state['step'] += 1
        st.session_state['bot_message'] = get_bot_message()  # This will trigger completion message
        append_bot_message_once(st.session_state['bot_message'])
        st.session_state['input_key'] += 1
        return

if st.session_state['bot_message'] is None and not st.session_state['chat_history']:
    st.session_state['bot_message'] = get_bot_message()
    append_bot_message_once(st.session_state['bot_message'])

# --- Chat UI with chat bubbles and avatars ---
user_avatar = "https://cdn-icons-png.flaticon.com/512/1946/1946429.png"
bot_avatar = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"

st.write('---')
st.subheader('Chat with TalentScout')

for message in st.session_state['chat_history']:
    if message['role'] == 'bot':
        with st.chat_message("assistant", avatar=bot_avatar):
            st.markdown(message['content'])
    else:
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(message['content'])

# --- Input Rendering ---
if not st.session_state.get('conversation_complete', False):
    # Greeting step
    if st.session_state['step'] == 0:
        st.text_input(
            "Your response:",
            key=f"user_input_{st.session_state['input_key']}",
            on_change=handle_user_input,
            placeholder="Type your message and press Enter..."
        )
    # Candidate info phase
    elif st.session_state['step'] > 0 and st.session_state['step'] <= len(FIELDS):
        field_name, field_display = FIELDS[st.session_state['step'] - 1]
        if field_name == 'phone':
            col1, col2 = st.columns([1, 3])
            with col1:
                st.selectbox(
                    'Country Code',
                    options=[c['dial_code'] for c in COUNTRY_CODES],
                    format_func=lambda x: f"{x} ({[c['name'] for c in COUNTRY_CODES if c['dial_code']==x][0]})",
                    key='country_code',
                )
            with col2:
                st.text_input(
                    "Phone Number (without country code)",
                    key=f"user_input_{st.session_state['input_key']}",
                    on_change=handle_user_input,
                    placeholder="Enter your phone number and press Enter..."
                )
        else:
            st.text_input(
                "Your response:",
                key=f"user_input_{st.session_state['input_key']}",
                on_change=handle_user_input,
                placeholder="Type your message and press Enter..."
            )
    # Technical question phase
    elif st.session_state['step'] == len(FIELDS) + 1:
        st.text_input(
            "Your answer (press Enter to submit, or type 'skip' to skip):",
            key=f"user_input_{st.session_state['input_key']}",
            on_change=handle_user_input,
            placeholder="Type your answer or 'skip'..."
        )
else:
    # End message
    email = st.session_state['candidate_data'].get('email', '')
    phone = st.session_state['candidate_data'].get('phone', '')
    st.success(f"✅ Screening complete! Thanks for your interest and time. Our team will get back to you soon at {email} or {phone}. You may close this window.")