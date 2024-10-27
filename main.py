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

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

# Initialize Swarm client
client = Swarm(client=openai.Client())






@app.post("/text-query")
async def text_agent_endpoint(
    user_message: str,
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
        # Start with the text agent
        agent = text_agent
        messages = [{"role": "user", "content": user_message}]
        

        response = client.run(
                    agent=agent,
                    messages=messages,
                )

        print(f"{response.messages[-1]['sender']}: {response.messages[-1]['content']}")
        content = response.messages[-1]["content"]
        return {"response": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/image-query")
async def image_agent_endpoint(
    user_message: str,
    file: UploadFile = File(...),
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
            {"role": "user", "content": user_message},
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