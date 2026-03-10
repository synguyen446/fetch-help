import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../models"))

from config import BOB_SEED
from uagents import Agent, Context, Model

bob = Agent(
    name="bob",
    seed=BOB_SEED,
    port=8002,
    mailbox=True,
    publish_agent_details=True,
)

class Message(Model):
    text: str

# -------------------------------------------------------
# YOUR CODE GOES HERE
# This handler is called whenever bob receives a message.
# -------------------------------------------------------
@bob.on_message(Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received from {sender}: {msg.text}")

if __name__ == "__main__":
    bob.run()
