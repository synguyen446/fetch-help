import os
from dotenv import load_dotenv
from uagents import Agent
import chat_protocol

load_dotenv()

alice = Agent(
    name="alice",
    seed="soiufisdfkjsjflksdowo24792834",
    port=8001,
    mailbox=True,
    publish_agent_details=True,
)

# -------------------------------------------------------
# YOUR CODE GOES HERE
# This function is called whenever alice receives a message.
# `text` is the incoming message content as a string.
# Return your response as a string.
# -------------------------------------------------------
async def get_response(text: str) -> str:
    return f"Hi! You said: {text}"

# Wire up your response function and register the chat protocol
chat_protocol.get_response = get_response
alice.include(chat_protocol.chat_proto, publish_manifest=True)

if __name__ == "__main__":
    alice.run()
