from agents.models.config import ADMIN_SEED
from agents.models.models import SharedAgentState
from uagents import Agent, Context
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)


admin = Agent(
    name="admin",
    seed=ADMIN_SEED,
    port=8001,
    mailbox=True,
    publish_agent_details=True,
)

history = []


@admin.on_message(SharedAgentState)
async def handle_message(ctx: Context, sender: str, state: SharedAgentState):
    ctx.logger.info("Added history!")
    state.history = history
    history.append({'role':'user','content':state.query})
    await ctx.send(sender, state)


@admin.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    text = " ".join(
        item.text for item in msg.content if isinstance(item, TextContent)
    )
    ctx.logger.info(f"Received: {text[:100]}")
    if not text == "Mention a specific agent (e.g., Admin, Bob, Project_Overview, API_Spec, Architecture, Data_Model, DevOps, Requirement, Testing_Strategy, User_Stories) in your message and I'll route it to them.":
        history.append({'role':'user','content':text})


if __name__ == "__main__":
    admin.run()
