import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="AI Research List Generator",
    page_icon="📋",
    layout="centered"
)

# ------------------ LOAD API KEY FROM STREAMLIT SECRETS ------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("GOOGLE_API_KEY not found in Streamlit Secrets.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# ------------------ MAIN UI ------------------
st.title("📋 AI Research List Generator")
st.markdown(
    "Generate well-researched lists from a specific **website source** using **Gemini AI**."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    topic = st.text_input(
        "🔍 Topic",
        placeholder="e.g. Machine Learning tools"
    )

with col2:
    source = st.text_input(
        "🌐 Source Website",
        placeholder="e.g. wikipedia.org"
    )

number = st.slider(
    "📌 Number of items",
    min_value=1,
    max_value=10,
    value=5
)

# ------------------ PROMPT ------------------
template = """
Do a proper research from {source} website and list down {number} {topic}.

Instructions:
1. Do a thorough research
2. Only list items (no description)
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["number", "topic", "source"]
)

# ------------------ MODEL ------------------
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

chain = prompt | gemini_model

# ------------------ ACTION ------------------
if st.button("🚀 Generate List"):
    if not topic or not source:
        st.warning("Please fill all fields.")
    else:
        with st.spinner("Researching... 🔎"):
            response = chain.invoke({
                "number": number,
                "topic": topic,
                "source": source
            })

        st.success("✅ Done!")
        st.markdown("### 📄 Generated List")
        st.markdown(response.content)


