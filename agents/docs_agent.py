import os
from swarm import Swarm, Agent
import  openai
from dotenv import load_dotenv
import cohere

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


co = cohere.Client(os.getenv("COHERE_API_KEY"))

from agents.text_agent import get_cohere_chat

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




# base agent
docs_agent = Agent(
    name="Docs Agent",
    instructions="You are a helpful agent. Answer user questions based on the provided information. If you don't find the answer, consult the real info agent before responding.",
    functions=[transfer_to_real_info_agent ],
)

