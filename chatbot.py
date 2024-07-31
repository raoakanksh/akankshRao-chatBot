import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI


OPEN_AI_API_KEY = "sk-None-zTFWUh5XqjaKAfTDIJB2T3BlbkFJb4zRRNid2TWup5PxGLrG"
# Upload files
st.header("My First Chatbot")

with st.sidebar:
    st.title("Your documents")
    file = st.file_uploader("Upload a PDF file and start asking questions", type="pdf")

# Extract the text
if file is not None:
    pdf_reader = PdfReader(file)  # Read the file
    text = ""
    # For all the pages in pdf_reader, extract that text and put it into the text variable
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Break into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=300,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Generating embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)

    # Creating vector store - FAISS
    vector_store = FAISS.from_texts(chunks, embeddings)

    #get user question
    user_input = st.text_input("Enter your question")

    #do similarity search
    if user_input:
        #Do a comparison between vector store and the user question to return the same results
        match = vector_store.similarity_search(user_input)

        #define the llm
        llm = ChatOpenAI(
            openai_api_key = OPEN_AI_API_KEY,
            temperature = 0,
            max_tokens = 1000,
            model_name = "gpt-3.5-turbo"
        )

        #output results
        #chain -> take question, get relevant document, pass it to the llm, generate the output
        chain = load_qa_chain(llm, chain_type = "stuff")
        output = chain.run(input_documents = match, question = user_input)
        st.write(output)

