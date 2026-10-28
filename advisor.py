import streamlit as st

from rag.rag_engine import ask_health_advisor

st.title("🤖 AI Health Advisor")

st.markdown("""
### Example Questions

• How can I reduce diabetes risk?

• What preventive screenings are recommended?

• How does smoking affect diabetes?

• What wellness programs are available?

• What services are recommended for high-risk members?
""")

question = st.text_input(
    "Ask a healthcare question"
)

if st.button("Ask Advisor"):

    if question:

        with st.spinner("Thinking..."):

            answer = ask_health_advisor(
                question
            )

        st.markdown(answer)