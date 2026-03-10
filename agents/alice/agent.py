from agents.models.config import ALICE_SEED
from agents.models.models import AgentState
from uagents import Agent, Context

alice = Agent(
    name="alice",
    seed=ALICE_SEED,
    port=8001,
    mailbox=True,
    publish_agent_details=True,
)

# -------------------------------------------------------
# YOUR CODE GOES HERE
# This handler is called whenever alice receives a message.
# -------------------------------------------------------
@alice.on_message(AgentState)
async def handle_message(ctx: Context, sender: str, msg: AgentState):
    ctx.logger.info(f"[{msg.session_id}] from {msg.user_sender_address}: {msg.query}")

if __name__ == "__main__":
    alice.run()
