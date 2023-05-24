import streamlit as st
from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import openai
import os
import tempfile

openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    st.title('AI Cover Letter Generator')

    st.subheader('Upload Resume')
    resume = st.file_uploader('Choose a resume file', type=['pdf'])
    if resume is not None:
        # Save UploadedFile to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(resume.read())
        # Use PyPDFLoader to load the resume
        loader = PyPDFLoader(fp.name)
        resume_pages = loader.load_and_split()
    else:
        st.warning('Please upload a resume.')

    st.subheader('Job Description URL')
    job_url = st.text_input('Input the URL here')
    if job_url:
        # Use WebBaseLoader to load the job description
        loader = WebBaseLoader(job_url)
        job_description_pages = loader.load_and_split()
    else:
        st.warning('Please enter a job URL.')

    st.subheader('Company Name')
    company_name = st.text_input('Input the company name here')
    
    st.subheader('Recent Company News')
    company_news = st.text_area('Input the recent company news here')

    if st.button('Generate Cover Letter'):
        # Generate embeddings from the resume, job description, and news
        embeddings = OpenAIEmbeddings()
        resume_embeddings = embeddings.create_embedding(resume_pages)
        job_description_embeddings = embeddings.create_embedding(job_description_pages)
        news_embeddings = embeddings.create_embedding(company_news)

        # Use the embeddings to generate a cover letter
        chat = ChatOpenAI()
        context = RetrievalQA([resume_embeddings, job_description_embeddings, news_embeddings])
        prompt = f"I am applying for a job at {company_name}."
        cover_letter = chat.generate(context, prompt)
        
        # Display the cover letter
        st.markdown(cover_letter)

if __name__ == "__main__":
    main()