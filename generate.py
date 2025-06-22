# # # import os
# # # from langchain_core.prompts import PromptTemplate
# # # from langchain_core.output_parsers import JsonOutputParser
# # # from langchain_core.exceptions import OutputParserException
# # # from langchain_groq import ChatGroq
# # # from dotenv import load_dotenv
# # # import streamlit as st

# # # groq_api_key = st.secrets["GROQ_API_KEY"]

# # # # Load environment variables
# # # load_dotenv()

# # # # Initialize Groq LLM
# # # llm = ChatGroq(temperature=0.7, groq_api_key=groq_api_key,
# # #                 model_name="llama3-70b-8192")

# # # # Define the output parser
# # # json_parser = JsonOutputParser()

# # # # Define the prompt template
# # # prompt_template = PromptTemplate(
# # #     input_variables=["text"],
# # #    template="""
# # # Based on the following text, generate 5 multiple-choice questions (MCQs) with 4 options each. 
# # # Ensure that one option is correct and the others are plausible but incorrect.
# # # Also provide a short explanation for the correct answer.
# # # Format the output as a JSON array with the structure:
# # # [
# # #     {{
# # #         "question": "...",
# # #         "choices": ["a) ...", "b) ...", "c) ...", "d) ..."],
# # #         "answer": "b) Correct option text",
# # #         "explanation": "Short explanation of the correct answer."
# # #     }},
# # #     ...
# # # ]
# # # Text: {text}
# # # """

# # # )

# # # def generate_mcqs(text):
# # #     chain = prompt_template | llm | json_parser
# # #     try:
# # #         result = chain.invoke({"text": text})
# # #         return result
# # #     except OutputParserException as e:
# # #         st.error(f"Error parsing output: {e}")
# # #         return None
# # import os
# # from langchain_core.prompts import PromptTemplate
# # from langchain_core.output_parsers import JsonOutputParser
# # from langchain_core.exceptions import OutputParserException
# # from langchain_groq import ChatGroq
# # from dotenv import load_dotenv
# # import streamlit as st

# # # Load secrets
# # groq_api_key = st.secrets["GROQ_API_KEY"]

# # # Load environment variables from .env if needed
# # load_dotenv()

# # # Initialize Groq Chat model
# # llm = ChatGroq(
# #     temperature=0.7,
# #     groq_api_key=groq_api_key,
# #     model_name="llama3-70b-8192"  # updated model name
# # )

# # # Define output parser for JSON response
# # json_parser = JsonOutputParser()

# # # Define prompt template
# # prompt_template = PromptTemplate(
# #     input_variables=["text"],
# #     template="""
# # Based on the following text, generate 5 multiple-choice questions (MCQs) with 4 options each. 
# # Ensure that one option is correct and the others are plausible but incorrect.
# # Also provide a short explanation for the correct answer.
# # Format the output as a JSON array with the structure:
# # [
# #     {{
# #         "question": "...",
# #         "choices": ["a) ...", "b) ...", "c) ...", "d) ..."],
# #         "answer": "b) Correct option text",
# #         "explanation": "Short explanation of the correct answer."
# #     }},
# #     ...
# # ]
# # Text: {text}
# # """
# # )

# # # MCQ generation function
# # def generate_mcqs(text):
# #     chain = prompt_template | llm | json_parser
# #     try:
# #         result = chain.invoke({"text": text})
# #         return result
# #     except OutputParserException as e:
# #         st.error(f"❌ Error parsing output: {e}")
# #         return None
# import os
# import json
# import streamlit as st
# from langchain_core.prompts import PromptTemplate
# from langchain_core.exceptions import OutputParserException
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv

# groq_api_key = st.secrets["GROQ_API_KEY"]
# load_dotenv()

# # Initialize Groq LLM
# llm = ChatGroq(
#     temperature=0.7,
#     groq_api_key=groq_api_key,
#     model_name="llama3-70b-8192"
# )

# # Define the prompt
# prompt_template = PromptTemplate(
#     input_variables=["text"],
#     template="""
# Based on the following text, generate 5 multiple-choice questions (MCQs) with 4 options each. 
# Ensure that one option is correct and the others are plausible but incorrect.
# Also provide a short explanation for the correct answer.
# Format the output as a **JSON array only** with the structure:
# [
#     {{
#         "question": "...",
#         "choices": ["a) ...", "b) ...", "c) ...", "d) ..."],
#         "answer": "b) Correct option text",
#         "explanation": "Short explanation of the correct answer."
#     }},
#     ...
# ]
# Text: {text}
# """
# )

# def extract_json(text):
#     try:
#         start = text.index("[")
#         end = text.rindex("]") + 1
#         json_text = text[start:end]
#         return json.loads(json_text)
#     except Exception as e:
#         st.error(f"⚠️ Failed to extract valid JSON: {e}")
#         return None

# def generate_mcqs(text):
#     chain = prompt_template | llm
#     try:
#         output = chain.invoke({"text": text})
#         return extract_json(output.content if hasattr(output, "content") else output)
#     except Exception as e:
#         st.error(f"❌ Error generating MCQs: {e}")
#         return None
import os
import re
import json
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

groq_api_key = st.secrets["GROQ_API_KEY"]
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    temperature=0.7,
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192"
)

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="""
Based on the following text, generate 10 multiple-choice questions (MCQs) with 4 options each. 
Ensure that one option is correct and the others are plausible but incorrect.
Also provide a short explanation for the correct answer.
Format the output as a JSON array ONLY:
[
    {{
        "question": "...",
        "choices": ["a) ...", "b) ...", "c) ...", "d) ..."],
        "answer": "b) Correct option text",
        "explanation": "Short explanation of the correct answer."
    }},
    ...
]
Text: {text}
"""
)

# Robust JSON extractor using regex
def extract_json(text):
    try:
        match = re.search(r'\[\s*{.*?}\s*]', text, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON array found.")
        json_text = match.group(0)
        return json.loads(json_text)
    except Exception as e:
        st.error(f"⚠️ Failed to extract valid JSON: {e}")
        return None

# Main MCQ generation function
def generate_mcqs(text):
    chain = prompt_template | llm
    try:
        output = chain.invoke({"text": text})
        return extract_json(output.content if hasattr(output, "content") else output)
    except Exception as e:
        st.error(f"❌ Error generating MCQs: {e}")
        return None
