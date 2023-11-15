from langchain.llms import GooglePalm
from secret_key import googlepalm_api_key
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os


os.environ["GOOGLE_API_KEY"] = googlepalm_api_key

llm = GooglePalm(temperature = 0)

instructor_embeddings = HuggingFaceInstructEmbeddings()
vectordb_file_path = "faiss_index"

def create_vectordb():
    loader = CSVLoader(file_path="output.csv", source_column="question")
    data = loader.load()
    vectordb = FAISS.from_documents(documents = data, embedding=instructor_embeddings)
    vectordb.save_local(vectordb_file_path)

def get_qa_chain():
    # Load the vector database from the local folder
    vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings)

    retriever = vectordb.as_retriever(score_threshold = 0.7)

    prompt_template = """Given the following context and a question, generate an answer based on this context only. In the answer try to provide as much text as possible from "response" section in the source document context without making much changes. If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt":PROMPT}
    )

    return chain


if __name__ == "__main__":
    # Creating a vectordb at once and saving it
    # create_vectordb()


    chain = get_qa_chain()

    print(chain("Can you gift wrap my product?"))
    

