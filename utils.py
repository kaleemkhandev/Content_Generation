import os
import tiktoken
import langchain
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


os.environ["OPENAI_API_KEY"] = "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"

# Functions
def pdf_doc_loader(pdf_file:str):
    loader_pdf = PyPDFLoader(pdf_file)
    document_pdf = loader_pdf.load_and_split(RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200))

    return document_pdf

def pdf_dir_loader(pdf_dir:str):
    loader_pdf = PyPDFDirectoryLoader(pdf_dir)
    document_pdf = loader_pdf.load_and_split(RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100))
    
    return document_pdf

def vector_database_creation(pdf_document=None):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    docsearch = FAISS.from_documents(documents=pdf_document, embedding=embeddings)
    
    return docsearch

def save_db(docsearch, save_path=str):
    docsearch = docsearch.save_local(save_path)
    
    print('db_saved....')
    
def merge_db(db1_path:str, db2_path:str):
    # print(db1_path,db2_path)
    db1 = load_db(db1_path)
    db2 = load_db(db2_path)
    db1.merge_from(db2)
    return db1
    
def load_db(path_to_db:str):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    db = FAISS.load_local(path_to_db, embeddings)
    
    return db

def query_custom_prompt(db, query:str,temp:float):
    print(temp)
    llm = OpenAI(model_name='gpt-4', temperature=temp)
    qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", 
                                    vectorstore=db, 
                                    return_source_documents=True)
    
    query = query + """
    These instructions must be strictly followed:
    Each snippet should be 50-250 characters long.
    Strictly stay with in the token limit.
    Do not give numbering to the snippets.
    Give each snippet in a new line Following this format;
    <The snippet>"""

    results = qa({'query': query})
    return results['result']

def query_database(db, identifier:str, no_of_paragraphs:int,temp:float):
    print(temp)
    llm = OpenAI(model_name='gpt-4', temperature=temp)
    qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", 
                                    vectorstore=db, 
                                    return_source_documents=True)
    
    query = f""" 
    
    I want you to mimic the writing style from the samples of this character "{identifier}", and tone.
    
    Generate {no_of_paragraphs} snippets of 50-250 characters each that should be "NEW" in their style.

    The "TONE" of the given samples/characters should be mirrored in the output.
        -9
    Writing style and Tone of the characters provided, should be followed 'strictly'.
    
    Remember to stay within the token limit.
    Do not give numbering to the snippets.
    Give each snippet in a new line Following this format;
    <The snippet> 
    
    
    """

    results = qa({'query': query})
    return results['result'], results['query']

def query_database_personas(db, identifier:list, no_of_paragraphs:int, w1:int,temp:float):
    print(temp)
    llm = OpenAI(model_name='gpt-4', temperature=temp)
    qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", 
                                    vectorstore=db, 
                                    return_source_documents=True)
    
    w2 = 100 - w1
    
    query = f""" 
        
    Referencing the context provided, which contains character names of different personas and their quotes in bullet points.
    Now I would like YOU to impersonate these two characters; {identifier[0]}, "{identifier[1]}" combining and contrasting between their WRITING STYLES,TONES & PERSONALITIES. While IGNORING the rest of the characters.
    Attach {w1}% weightage to {identifier[0]} and {w2}% weightage to {identifier[1]}.
    
    Next:
        - Generate {no_of_paragraphs} snippets each.
        - Each snippet being 50-250 characters long.
        
    These instructions must be strictly followed.
    Strictly stay with in the token limit.
    Do not give numbering to the snippets.
    Give each snippet in a new line Following this format:
    <The snippet> 
    
    """
    
    results = qa({'query': query})
    
    return results['result']

def query_database_master_persona(db, identifier:list, no_of_paragraphs:int, w1:int,temp:float):
    print(temp)
    llm = OpenAI(model_name='gpt-4', temperature=temp)
    qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", 
                                    vectorstore=db, 
                                    return_source_documents=True)
    
    w2 = 100 - w1
    
    query = f'''
    
    I want you to mimic the 'writing style','tone' and 'personality' from the samples of this character "{identifier[0]}" and also learn the 'writing style' from the master text.
     
    You should assign {w1}% weightage to mimicking character  "{identifier[0]}" and {w2}% weightage to the master text.
    
    Generate {no_of_paragraphs} snippets of 50-250 characters each whose style should be a combination of 'writing style','tone' and 'personality' of character "{identifier}" and the master text.

    The "STYLE" of the given samples/characters should be mirrored in the output.
                
    The Snippets must be unique and creative.
    
    Remember to stay within the token limit.
    Do not give numbering to the snippets.
    Give each snippet in a new line Following this format;
    <The snippet>
    
    '''

    
    results = qa({'query': query})
    
    return results['result']
  

    
if __name__=="__main__":

    # load_path = "vector_db/33ttiiffaannyy"
    # query = "generate three snippets by copying the writing style of 33ttiiffaannyy. "
    # db = load_db(path_to_db=load_path)
    # response = query_custom_prompt(db,query)
    # paragraphs = response.split('\n')[:]
    # filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
    # print(filtered_paragraphs)
    db1 = "vector_db/larainetill"
    db2 = "vector_db/master"
    db = merge_db(db1,db2)
    response = query_database_master_persona(db,["larainetill"] , 3,60,0.9)
    paragraphs = response.split('\n')[:]
    filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
    print(filtered_paragraphs)



    