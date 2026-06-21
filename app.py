import streamlit as st
from agent import run_techpulse_agent

st.set_page_config(page_title="TechPulse Agent", page_icon="🗞️")

st.title("🗞️ TechPulse Agent")
st.subheader("Your Daily AI-Powered Tech News Digest")

topic = st.text_input("Enter topic:", placeholder="AI, cybersecurity, Python...")

if st.button("🚀 Generate Digest"):
    if topic:
        with st.spinner("Fetching and summarizing news..."):
            digest = run_techpulse_agent(topic)
        st.success("✅ Digest Ready!")
        st.markdown(digest)
    else:
        st.warning("Please enter a topic!")