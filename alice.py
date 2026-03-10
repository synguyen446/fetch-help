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

alice.include(chat_protocol.chat_proto, publish_manifest=True)

if __name__ == "__main__":
    alice.run()
