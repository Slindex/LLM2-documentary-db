from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Se comenta todo lo de llama para tenerlo cuando sea integrado
#import os
#from dotenv import load_dotenv

# Importing langchai and llama2 related functions
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
#from llama_cpp import Llama 
from langchain.llms import CTransformers
from langchain.llms import Replicate

# Where the llama2 folder lives
model_path = "c:/Users/SEBASTIAN/Downloads/llama-2-7b-chat.ggmlv3.q4_0.bin"

#llm = Llama(model_path)

#callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


# loading the model using langchain LlamaCpp class
llm = CTransformers(
        model="c:/Users/SEBASTIAN/Downloads/llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        max_new_tokens=512,  # type: ignore
        temperature=0.01,  # type: ignore
    )

"""
llm = Replicate(
        streaming = True,
        model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
        callbacks=[StreamingStdOutCallbackHandler()],
        input = {"temperature": 0.01, "max_length" :500,"top_p":1},
        replicate_api_token="r8_dkOTjc4YFQB6w1NwpqvL5w19zKxZysF2vWUF1",
        )
"""

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
    
"""
#De aqui en adelante hay dragones 🐲
"""

def AI_GGML(request):
    
    """
    llm = Replicate(
        streaming = True,
        model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
        callbacks=[StreamingStdOutCallbackHandler()],
        input = {"temperature": 0.01, "max_length" :500,"top_p":1},
        replicate_api_token="r8_dkOTjc4YFQB6w1NwpqvL5w19zKxZysF2vWUF1",
        )
    """
    llm = CTransformers(
        model="c:/Users/SEBASTIAN/Downloads/llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        max_new_tokens=512,  # type: ignore
        temperature=0.001,  # type: ignore
    )
    
    queries = Userquery.objects.all().order_by('id')[:5]
    
    query = request.GET['query']
    
    model_out = llm(query, 
        max_tokens=512, 
        echo=True)

    print(model_out)
    output = model_out
    
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


