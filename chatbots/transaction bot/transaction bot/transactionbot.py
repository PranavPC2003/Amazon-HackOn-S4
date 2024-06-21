from pandasai.llm.local_llm import LocalLLM
import streamlit as st 
import pandas as pd 
from pandasai import SmartDataframe

# Initialize the model
model = LocalLLM(
    api_base="http://localhost:11434/v1",
    model="llama3"
)

# Set the title of the Streamlit app
st.title("Amazon Transaction Bot")

# Define the path to your CSV file here
file_path = "/Users/harshit/Downloads/transactionsf.csv"

# Read the CSV file
data = pd.read_csv(file_path)

# Display the first 3 rows of the dataframe
st.write(data.head(3))

# Initialize SmartDataframe with the data and model
df = SmartDataframe(data, config={"llm": model})

# Text area for user to input their prompt
prompt = st.text_area("Enter your prompt:")

# Button to generate the response
if st.button("Generate"):
    if prompt:
        with st.spinner("Generating response..."):
            # Display the chat response from SmartDataframe
            st.write(df.chat(prompt))
