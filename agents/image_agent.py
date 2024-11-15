
import os
from swarm import Swarm, Agent
import  openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_client= openai


# Function to generate image using OpenAI API
def generate_image(prompt):
    """
    Generates an image using OpenAI's API

    Args:
        prompt: the text to generate an image from

    Returns:
        the URL of the generated image, or an error string if it fails
    """
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



# base agent
image_agent = Agent(
    name="Image Agent",
    instructions=f"You are an helpful AI agent that can generate images. use appropriate function for generating image. finally return generated image url",
    functions=[generate_image]
)