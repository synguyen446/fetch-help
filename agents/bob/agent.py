from agents.models.config import BOB_SEED
from agents.models.models import AgentState
from uagents import Agent, Context

bob = Agent(
    name="bob",
    seed=BOB_SEED,
    port=8002,
    mailbox=True,
    publish_agent_details=True,
)

# -------------------------------------------------------
# YOUR CODE GOES HERE
# This handler is called whenever bob receives a message.
# -------------------------------------------------------
@bob.on_message(AgentState)
async def handle_message(ctx: Context, sender: str, msg: AgentState):
    ctx.logger.info(f"[{msg.session_id}] from {msg.user_sender_address}: {msg.query}")

if __name__ == "__main__":
    bob.run()
