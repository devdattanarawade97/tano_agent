from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from swarm import Swarm, Agent
import openai
import os
from dotenv import load_dotenv
from typing import List, Optional, Dict
import io
import requests

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

# Initialize Swarm client
client = Swarm(client=openai.Client())
openai_client= openai
# Define the text agent
def transfer_to_text_agent():
    return text_agent

def transfer_to_image_agent():
    return image_agent

text_agent = Agent(
    name="Text Agent",
    instructions="""You are a helpful agent,
    If the user wants to generate or create image, 
    transfer the conversation to Image Agent.""",
    functions=[transfer_to_image_agent],
)

# Function to generate image using OpenAI API
def generate_image(prompt):
    try:
        # Call OpenAI's API to create an image
      
        response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        )

        image_url = response.data[0].url
        print(f'image url : {image_url}')
        return image_url  # Return the image URL directly
    except Exception as e:
        return f"Error generating image: {str(e)}"

image_agent = Agent(
    name="Image Agent",
    instructions="You are an AI that can generate images. use function for generating image",
    functions=[generate_image]
)

@app.post("/text-query")
async def swarm_endpoint(
    user_message: str,
):
    try:
        # Start with the text agent
        agent = text_agent
        messages = [{"role": "user", "content": user_message}]

        # Keep track of the current agent
        current_agent = agent

        while True:
            response = client.run(
                agent=agent,
                messages=messages,
            )

            # Check if the agent wants to transfer
            if response.messages[-1]["content"] == 'image_agent':
                agent = image_agent
            elif response.messages[-1]["content"] == 'text_agent':
                agent = text_agent
            else:
                break  # No transfer, break the loop

            # If the agent has changed, update the current agent and add the transfer message
            if agent != current_agent:
                current_agent = agent
                messages.append(response.messages[-1])

        # Check if the response is an image URL
        content = response.messages[-1]["content"]
        if content.startswith("http"):
            # Fetch the image content from the URL
            image_content = requests.get(content).content

            # Return the image as a streaming response
            return StreamingResponse(
                io.BytesIO(image_content),
                media_type="image/png",  # Adjust media type if necessary
                headers={
                    "Content-Disposition": "attachment; filename=\"generated_image.png\""
                }
            )
        else:
            return {"response": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))