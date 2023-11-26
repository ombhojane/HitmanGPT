import streamlit as st
import openai
from rohit_data import data

# Define generate_prompt function
@st.cache_data  
def generate_prompt(query):
    return f"""{data}
Human: {query}

Rohit:"""

# OpenAI API key 
openai.api_key = st.secrets["openai_api_key"]

# Chatbot UI
st.header('Hitman Chatbot')
st.subheader('Powered by GPT-3.5 Turbo')

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []
    
user_input = st.text_input('You: ', 'Hi')

if user_input:
    output = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(user_input),
        temperature=0.8,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.3
    )
    
    response = output.choices[0].text.strip()
    
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)
    
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, len(st.session_state['past'])):    
        st.text_area('You:', value=st.session_state['past'][i], height=20, key=str(i)+"user")
        st.text_area('Rohit:', value=st.session_state['generated'][i], height=20, key=str(i)+"bot")
