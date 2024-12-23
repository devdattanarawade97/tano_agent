from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from swarm import Swarm, Agent
import openai
import os
from dotenv import load_dotenv
from typing import List, Optional, Dict
import io
import requests
from agents.text_agent import text_agent
from agents.image_agent import image_agent
from agents.docs_agent import docs_agent
from schema.text_query_schema import TextQueryRequest
from schema.docs_query_schema import DocsQueryRequest
from fastapi.middleware.cors import CORSMiddleware
from schema.image_query_schema import ImageQueryRequest
# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; customize as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Swarm client
client = Swarm(client=openai.Client())



@app.post("/text-query")
async def text_agent_endpoint(
    request: TextQueryRequest,
):
    """
    Handles a text query from the user and returns a response from the text agent.

    Args:
        user_message (str): The message from the user.

    Returns:
        response (str): The response from the text agent.

    Raises:
        HTTPException: If there is an error with the request.
    """
    
    try:
        user_message = request.user_message
        # Start with the text agent
        agent = text_agent
        messages = [{"role": "user", "content": user_message}]
        

        response = client.run(
                    agent=agent,
                    messages=messages,
                )

        print(f"{response.messages[-1]['sender']}: {response.messages[-1]['content']}")
        content = response.messages[-1]["content"]
        return {"content": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/image-query")
async def image_agent_endpoint(
    request: ImageQueryRequest,
):
    """
    Handles an image query from the user and returns a response from the image agent.

    Args:
        user_message (str): The message from the user.

    Returns:
        response (str): The response from the image agent.

    Raises:
        HTTPException: If there is an error with the request.
    """
    try:


        agent = image_agent
        messages = [
            {"role": "user", "content": request.user_message},
        ]

        response = client.run(
                agent=agent,
                messages=messages,
            )

        content = response.messages[-1]["content"]
        if "Error generating image" in content:
            raise HTTPException(
                status_code=500, detail=f"Error generating image: {content}"
            )

        print(f"{response.messages[-1]['sender']}: {response}")

        return {"response": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.post("/docs-query")
async def docs_agent_endpoint(
    request: DocsQueryRequest,
):
   
    """
    Handles a document query from the user and returns a response from the docs agent.

    Args:
        request (DocsQueryRequest): The request containing the user query and relevant documents.

    Returns:
        dict: A dictionary containing the response content from the docs agent.

    Raises:
        HTTPException: If there is an error generating the response or handling the request.
    """

    try:
        
        # print(f'relevant docs : {request.relevant_docs}')
        agent = docs_agent
        messages = [
            {"role": "user", "content": request.user_query+request.relevant_docs},
        ]

        response = client.run(
                agent=agent,
                messages=messages,
            )
        
        # print(f'response : {response}')
        
        content = response.messages[-1]["content"]
        if "Error generating response" in content:
            raise HTTPException(
                status_code=500, detail=f"Error generating docs response: {content}"
            )


        print(f"{response.messages[-1]['sender']}: {response}")

        return {"content": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))