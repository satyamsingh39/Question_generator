# from langchain_community.document_loaders import PyPDFLoader
# from langchain_core.documents import Document
# from langchain.text_splitter import TokenTextSplitter
# from langchain_groq import ChatGroq
# from langchain.prompts import PromptTemplate
# from langchain.chains.summarize import load_summarize_chain
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# import os
# from dotenv import load_dotenv
# from src.prompt import *


# # OpenAI authentication
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# os.environ["GROQ_API_KEY"] = GROQ_API_KEY



# def file_processing(file_path):

#     # Load data from PDF
#     loader = PyPDFLoader(file_path)
#     data = loader.load()

#     question_gen = ''

#     for page in data:
#         question_gen += page.page_content

#     # Reduced chunk size for faster processing
#     splitter_ques_gen = TokenTextSplitter(
#         model_name = 'gpt-3.5-turbo',
#         chunk_size = 5000,  # Reduced from 10000
#         chunk_overlap = 100  # Reduced from 200
#     )

#     chunks_ques_gen = splitter_ques_gen.split_text(question_gen)

#     document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]

#     splitter_ans_gen = TokenTextSplitter(
#         model_name = 'gpt-3.5-turbo',
#         chunk_size = 800,  # Reduced from 1000
#         chunk_overlap = 50  # Reduced from 100
#     )


#     document_answer_gen = splitter_ans_gen.split_documents(
#         document_ques_gen
#     )

#     return document_ques_gen, document_answer_gen




# def llm_pipeline(file_path):

#     document_ques_gen, document_answer_gen = file_processing(file_path)

#     llm_ques_gen_pipeline = ChatGroq(
#         model="openai/gpt-oss-20b",
#         temperature=0.3,  # Lower temperature for faster, more focused responses
#     )

#     PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=["text"])

#     # Changed from "refine" to "stuff" for much faster processing
#     # "stuff" combines all chunks and makes one API call instead of sequential calls
#     ques_gen_chain = load_summarize_chain(
#         llm=llm_ques_gen_pipeline,
#         chain_type="stuff",  # Much faster than "refine"
#         verbose=True,
#         prompt=PROMPT_QUESTIONS
#     )

#     ques = ques_gen_chain.run(document_ques_gen)

#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     vector_store = FAISS.from_documents(document_answer_gen, embeddings)

#     llm_answer_gen = ChatGroq(
#         model="openai/gpt-oss-20b",
#         temperature=0.3,  # Lower temperature for faster responses
#     )

#     ques_list = ques.split("\n")
#     filtered_ques_list = [element for element in ques_list if element.endswith('?') or element.endswith('.')]

#     answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen, 
#                                                 chain_type="stuff", 
#                                                 retriever=vector_store.as_retriever())

#     return answer_generation_chain, filtered_ques_list

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import os
from dotenv import load_dotenv

from src.prompt import *


# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

os.environ["GROQ_API_KEY"] = GROQ_API_KEY


def file_processing(file_path):

    # Load data from PDF
    loader = PyPDFLoader(file_path)
    data = loader.load()

    question_gen = ""

    for page in data:
        question_gen += page.page_content

    # Split text for question generation
    splitter_ques_gen = TokenTextSplitter(
        model_name="gpt-3.5-turbo",
        chunk_size=5000,
        chunk_overlap=100
    )

    chunks_ques_gen = splitter_ques_gen.split_text(question_gen)

    document_ques_gen = [
        Document(page_content=t)
        for t in chunks_ques_gen
    ]

    # Split text for answer generation
    splitter_ans_gen = TokenTextSplitter(
        model_name="gpt-3.5-turbo",
        chunk_size=800,
        chunk_overlap=50
    )

    document_answer_gen = splitter_ans_gen.split_documents(
        document_ques_gen
    )

    return document_ques_gen, document_answer_gen


def llm_pipeline(file_path, question_type="Short Answer", difficulty="Medium"):

    document_ques_gen, document_answer_gen = file_processing(file_path)

    # Groq Llama model
    llm_ques_gen_pipeline = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.3
    )

    # Question generation prompt
    PROMPT_QUESTIONS = PromptTemplate(
        template=prompt_template,
        input_variables=["text", "question_type", "difficulty"]
    )

    # Prepare document text
    document_text = "\n\n".join(
        doc.page_content for doc in document_ques_gen
    )

    # Generate questions
    formatted_prompt = PROMPT_QUESTIONS.format(
        text=document_text,
        question_type=question_type,
        difficulty=difficulty
    )

    response = llm_ques_gen_pipeline.invoke(
        formatted_prompt
    )

    ques = response.content

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS vector store
    vector_store = FAISS.from_documents(
        document_answer_gen,
        embeddings
    )

    # Answer generation LLM
    llm_answer_gen = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.3
    )

    # Process generated questions
    ques_list = ques.split("\n")

    filtered_ques_list = [
        element.strip()
        for element in ques_list
        if element.strip().endswith("?")
        or element.strip().endswith(".")
    ]

    # Retriever
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    # Modern replacement for old RetrievalQA
    class AnswerGenerator:
        def __call__(self, question):
            return self.run(question)

        def run(self, question):
            docs = retriever.invoke(question)

            context = "\n\n".join(
                doc.page_content for doc in docs
            )

            answer_prompt = f"""
Answer the following question using ONLY the provided context.

Context:
{context}

Question:
{question}

Give a clear and concise answer.
"""

            result = llm_answer_gen.invoke(answer_prompt)

            return result.content

    answer_generation_chain = AnswerGenerator()

    # IMPORTANT:
    # Keep the original return structure:
    # (answer_generation_chain, filtered_ques_list)
    return answer_generation_chain, filtered_ques_list

