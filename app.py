import streamlit as st
import openai
import os
from datetime import datetime

# Configure OpenAI (use your API key)
# For demo, use: openai.api_key = st.secrets["OPENAI_API_KEY"]
# Or set environment variable: os.environ["OPENAI_API_KEY"] = "your-key"

# For Gemini users, replace with google.generativeai

st.set_page_config(page_title="AI Productivity Assistant", layout="wide")

st.title("🤖 AI Workplace Productivity Assistant")
st.caption("Smart Email · Meeting Summaries · Task Planning · Research · Chatbot")

# Sidebar for API key
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        openai.api_key = api_key
    st.markdown("---")
    st.markdown("⚠️ **Responsible AI Disclaimer**")
    st.info("AI may make mistakes. Verify critical information before acting.")

# Helper function for API calls
def call_ai(prompt, system_message="You are a helpful workplace assistant."):
    if not api_key:
        return "⚠️ Please enter your API key in the sidebar."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Tab layout for 5 features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📧 Email Generator", 
    "📝 Meeting Summarizer", 
    "📅 Task Planner", 
    "🔍 Research Assistant", 
    "💬 AI Chatbot"
])

# ---------- FEATURE 1: EMAIL GENERATOR ----------
with tab1:
    st.header("Smart Email Generator")
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_area("What's this email about?", placeholder="Request project update...")
        audience = st.selectbox("Audience", ["Client", "Manager", "Team Member", "Other"])
        tone = st.selectbox("Tone", ["Formal", "Informal", "Persuasive", "Friendly"])
    with col2:
        additional_context = st.text_area("Additional context (optional)", placeholder="Deadline, previous conversation...")
    
    if st.button("Generate Email", key="email_btn"):
        if topic:
            prompt = f"""Generate a {tone.lower()} email to a {audience.lower()}.
            Topic: {topic}
            Additional context: {additional_context}
            Include subject line, greeting, body, and closing."""
            response = call_ai(prompt)
            st.markdown("### 📧 Generated Email")
            st.markdown(response)
        else:
            st.warning("Please enter a topic.")

# ---------- FEATURE 2: MEETING SUMMARIZER ----------
with tab2:
    st.header("Meeting Notes Summarizer")
    notes = st.text_area("Paste your meeting notes or transcript", height=200)
    
    if st.button("Summarize Meeting", key="summary_btn"):
        if notes:
            prompt = f"""Summarize these meeting notes into:
            1. Key points (bullet list)
            2. Decisions made
            3. Action items (who does what)
            4. Deadlines mentioned
            
            Notes: {notes}"""
            response = call_ai(prompt)
            st.markdown("### 📝 Meeting Summary")
            st.markdown(response)
        else:
            st.warning("Please paste meeting notes.")

# ---------- FEATURE 3: TASK PLANNER ----------
with tab3:
    st.header("AI Task Planner / Scheduler")
    tasks = st.text_area("List your tasks (one per line)", 
                         placeholder="Finish project report\nCall client about contract\nResearch AI tools\nUpdate team on progress")
    
    priority = st.multiselect("Priority level", ["High urgency", "Medium urgency", "Low urgency"], default=["High urgency"])
    
    if st.button("Generate Plan", key="plan_btn"):
        if tasks:
            prompt = f"""Create a daily work plan from these tasks:
            Tasks: {tasks}
            Priority focus: {', '.join(priority)}
            
            Include:
            - Suggested order of tasks
            - Time blocks (morning/afternoon)
            - Productivity tips
            - Estimated effort per task"""
            response = call_ai(prompt)
            st.markdown("### 📅 Your AI-Generated Plan")
            st.markdown(response)
        else:
            st.warning("Please enter at least one task.")

# ---------- FEATURE 4: RESEARCH ASSISTANT ----------
with tab4:
    st.header("AI Research Assistant")
    query = st.text_area("What would you like to research?", 
                         placeholder="Summarize the key benefits of hybrid work models...")
    depth = st.select_slider("Research depth", options=["Quick summary", "Detailed analysis", "With examples"])
    
    if st.button("Research", key="research_btn"):
        if query:
            prompt = f"""Research the following topic: {query}
            Depth: {depth}
            
            Provide:
            1. Key insights (3-5 bullet points)
            2. Practical recommendations (2-3)
            3. Simplify complex concepts for quick understanding"""
            response = call_ai(prompt)
            st.markdown("### 🔍 Research Results")
            st.markdown(response)
        else:
            st.warning("Please enter a research query.")

# ---------- FEATURE 5: CHATBOT ----------
with tab5:
    st.header("AI Chatbot Assistant")
    st.caption("Ask me anything about workplace productivity, task management, or professional advice.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    user_input = st.chat_input("Ask your workplace assistant...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            response = call_ai(user_input, "You are a helpful, concise workplace AI assistant. Provide practical advice.")
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})