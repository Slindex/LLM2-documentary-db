import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
#from media import *

# Se comenta todo lo de llama para tenerlo cuando sea integrado
#import os
#from dotenv import load_dotenv

# Importing langchai and llama2 related functions
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
#from llama_cpp import Llama 
from langchain.llms import CTransformers
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.vectorstores import Pinecone
import pinecone
import torch
import transformers
from torch import cuda, bfloat16
from huggingface_hub import login

"""
device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

bnb_config = transformers.BitsAndBytesConfig(
     load_in_4bit=False, #Era True
     bnb_4bit_quant_type='nf4',
     bnb_4bit_use_double_quant=True,
     bnb_4bit_compute_dtype=bfloat16
     )

"""

# Constants
model_path = "E:/david/Documents/LLM2-db-documental/model"
idModel = "meta-llama/Llama-2-7b-chat-hf"
embeddingsModel = "sentence-transformers/all-MiniLM-L6-v2"
docum = "/media"
persist_directory = 'chroma/'
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '161b38d5-c986-4da9-ac94-d980a3fa0de7') #,'f5444e56-58db-42db-afd6-d4bd9b2cb40c')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter') #, 'asia-southeast1-gcp-free')
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
    )
index_name = "langchain-pinecone-llama2"

login(token='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')

os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'

#llm = Llama(model_path)

#callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


# loading the model using langchain LlamaCpp class
"""

llm = Replicate(
        streaming = True,
        model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
        callbacks=[StreamingStdOutCallbackHandler()],
        input = {"temperature": 0.01, "max_length" :500,"top_p":1},
        replicate_api_token="r8_dkOTjc4YFQB6w1NwpqvL5w19zKxZysF2vWUF1",
        )
"""

# Functions without a page
def createLlm():

    llm = CTransformers(
        model="E:/david/Documents/LLM2-db-documental/model/llama-2-7b-chat.ggmlv3.q5_1.bin",
        model_type="llama",
        max_new_tokens=4096,  # type: ignore
        temperature=0.01,  # type: ignore
    )

    return llm

def createEmbeddings(embeddingsModel):
    #Create embeddings here
    print("Loading sentence transformers model")
    embeddings = SentenceTransformerEmbeddings(
                                model_name=embeddingsModel,
                                model_kwargs={"device": "cpu"})
    print("Finished loading sentence transformers model")
    return embeddings

"""
# This function iterates on a list and then get the files
def dataProcessing(uploaded_files):
    text = []
    for file in uploaded_files:
      if os.path.isfile(file) and file.endswith(".txt"):
        loader = TextLoader(file)
        text.extend(loader.load())
      if os.path.isfile(file) and file.endswith(".pdf"):
        loader = PyPDFLoader(file)
        text.extend(loader.load())
      if os.path.isfile(file) and (file.endswith(".doc") or file.endswith(".docx")) :
        loader = Docx2txtLoader(file)
        text.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                              chunk_overlap=50,
                                              length_function=len,
                                              #is_separator_regex = False,
                                               separators=['\n\n', '.\n', ' ', '']
                                               )
    text_chunks = text_splitter.split_documents(text)

    os.remove(file)
    return text_chunks
"""
def dataProcessing(path):
    text = []
  
    loader = PyPDFLoader(f'{path}+*.pdf')
    text.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                  chunk_overlap=50,
                                                  length_function=len,
                                                  #is_separator_regex = False,
                                                  separators=['.\n\n', '.\n', '.', '\n\n', ',']
                                                  )
    text_chunks = text_splitter.split_documents(text)

    return text_chunks

def saveToDb(text_chunks, embeddings, persist_directory):
    
    # Para usar la base de datos con los embedigs ya guardados
    vector_store = Chroma.from_documents(documents=text_chunks,
                                        embedding=embeddings,
                                        persist_directory=persist_directory)
    return vector_store

def useDb(persist_directory, embeddings):
    vector_store = Chroma(persist_directory=persist_directory,
                      embedding_function=embeddings)
    return vector_store

def answer(query, llm, vector_store):
    print('aca entro a answer')
    chain = load_qa_chain(llm, chain_type="stuff")

    print('aca llego a chain')
    docs= vector_store.similarity_search(query, k=2)

    output = chain.run(input_documents=docs,
              question=query)
    
    return output



# Create your views here.
def frontpage (request):
    return render(request, 'core/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            
            return redirect('frontpage')
    else:
        form = SignUpForm()
        
    return render(request, 'core/signup.html', {'form': form})

@login_required
def chat(request):
    queries = Userquery.objects.all().order_by('-id')[:5]
    context = {
        'queries': queries
    }
    return render(request, 'core/chat.html',context)       


@login_required
def CargaDocumental(request):
    context ={}
    if request.method == "POST":
        uploaded_file= request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'core/CargaDocumental.html', context)       


def AI_GGML(request):
    
    # Carga del modelo con replicate
    """
    llm = Replicate(
        streaming = True,
        model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
        callbacks=[StreamingStdOutCallbackHandler()],
        input = {"temperature": 0.01, "max_length" :500,"top_p":1},
        replicate_api_token="r8_dkOTjc4YFQB6w1NwpqvL5w19zKxZysF2vWUF1",
        )
    
    llm = CTransformers(
        model="c:/Users/SEBASTIAN/Downloads/llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        gpu_layers=50,
        max_new_tokens=512,  # type: ignore
        temperature=0.001,  # type: ignore
    )
    
    answer = llm(query, 
        max_tokens=512, 
        echo=True)
    
    """

    query = request.GET['query']
    
    llm = createLlm()
    print("model loaded")
    embeddings = createEmbeddings(embeddingsModel)
    print("embeddings created")
    vector_store = Pinecone.from_existing_index(index_name, embeddings) #useDb(persist_directory, embeddings)
    print("Pinecone vector store loaded")
    output = answer(query, llm, vector_store)
    print("answer loaded")
    
    queries = Userquery.objects.all().order_by('id')[:5]
    
    #output = model_out
    
    #saving the query and output to database
    query_data = Userquery(
        query=query,
        reply=output
    )
    query_data.save() 
    context = {
        'queries':queries,
        'query':query,
        'output':output
    }
    
    return render(request, 'core/chat.html', context)


