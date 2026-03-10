from agents.models.config import ALICE_SEED
from uagents import Agent, Context, Model

alice = Agent(
    name="alice",
    seed=ALICE_SEED,
    port=8001,
    mailbox=True,
    publish_agent_details=True,
)

class Message(Model):
    text: str

# -------------------------------------------------------
# YOUR CODE GOES HERE
# This handler is called whenever alice receives a message.
# -------------------------------------------------------
@alice.on_message(Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received from {sender}: {msg.text}")

if __name__ == "__main__":
    alice.run()
