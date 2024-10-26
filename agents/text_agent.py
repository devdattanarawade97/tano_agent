

import os
import cohere
from dotenv import load_dotenv
from swarm import Swarm, Agent
import openai

load_dotenv()

co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))


def get_cohere_chat(prompt):
        """
        Sends a chat request to the Cohere API using the specified model and prompt.

        Args:
            prompt (str): The input text message or prompt for the chat request.

        Returns:
            The response object from the Cohere API containing the chat completion.
        """
        response = co.chat(
        model="command-r-plus-08-2024",
        messages=orompt,
        connectors=[{"id":"web-search"}]
    
      
    )   
        print(f'cohere response : {response}')
        return response


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



text_agent = Agent(
    name="Text Agent",
    instructions="""You are an helpful agent . if you dont know answer transfer conversation to Real Info Agent for more information""",
   functions=[transfer_to_real_info_agent],
)




