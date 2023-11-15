import streamlit as st
from ecommerce_google_palm_chatbot import get_qa_chain, create_vectordb

st.title("E-Commerce QA Chatbot 🤖")

question = st.text_input("Question: ")

if question:
    chain = get_qa_chain()
    response = chain(question)

    st.header("Answer: ")
    st.write(response["result"])

