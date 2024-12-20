

import os
import cohere
from dotenv import load_dotenv
from swarm import Swarm, Agent
import openai
import google.generativeai as genai
# load env 
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


co = cohere.Client(os.getenv("COHERE_API_KEY"))


def get_cohere_chat(prompt):
        """
        Sends a chat request to the Cohere API using the specified model and prompt.

        Args:
            prompt (str): The input text message or prompt for the chat request.

        Returns:
            The response object from the Cohere API containing the chat completion.
        """
        try:
            response = co.chat(
                model="command-r-plus-08-2024",
                message= prompt,  # Correct format for messages
                connectors=[{"id":"web-search"}]
            )
            # print(f'cohere response : {response}')
            return response
        except Exception as e:
            print(f'error in cohere : {e}')


real_info_agent = Agent(
    name="Real Info Agent",
    instructions="""You are an helpful AI agent . use functions for answering user question""",
    functions=[get_cohere_chat],
)


def transfer_to_real_info_agent():
    """
    Transfers the conversation to the Real Info Agent.

    Returns:
        The Real Info Agent
    """
    return real_info_agent


def get_gemini_chat(prompt):
        """
        Sends a chat request to the Gemini API using the specified model and prompt.

        Args:
            prompt (str): The input text message or prompt for the chat request.

        Returns:
            The response object from the Gemini API containing the chat completion.
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        # print('gemini response : ',response)
        return response

def transfer_to_gemini_agent():
    """
    Transfers the conversation to the Gemini Agent.

    Returns:
        The Gemini Agent
    """
    return gemini_agent

gemini_agent = Agent(
    name="Gemini Agent",
    instructions="""You are an helpful agent . if you dont know answer transfer conversation to Real Info Agent for more information""",
    functions=[transfer_to_real_info_agent , get_gemini_chat],
)

# base agent
text_agent = Agent(
    name="Text Agent",
    instructions="""You are an helpful agent .if user specify he want answer from 'gemini' then transfer conversation to Gemini Agent. if you dont know answer or user mentions 'cohere'then transfer conversation to Real Info Agent for more information.""",
    functions=[transfer_to_real_info_agent , transfer_to_gemini_agent],
)




