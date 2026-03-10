from datetime import datetime, timezone
from uuid import uuid4

from uagents import Context, Protocol
from agents.models.config import ALICE_ADDRESS, BOB_ADDRESS
from agents.models.models import SharedAgentState
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

chat_proto = Protocol(spec=chat_protocol_spec)


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    text = " ".join(
        item.text for item in msg.content if isinstance(item, TextContent)
    )
    ctx.logger.info(f"Received: {text}")
    ctx.logger.info(ctx.session_history())

    state = SharedAgentState(
        chat_session_id=str(ctx.session),
        query=text,
        user_sender_address=sender,
    )

    if "alice" in text.lower():
        await ctx.send(ALICE_ADDRESS, state)
        response = "Routing to Alice!"
    elif "bob" in text.lower():
        await ctx.send(BOB_ADDRESS, state)
        response = "Routing to Bob!"
    else:
        response = "Mention Alice or Bob in your message and I'll route it to them."

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.now(tz=timezone.utc),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=response),
                EndSessionContent(type="end-session"),
            ],
        ),
    )


@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass


async def send_agent_result_back_to_user(ctx: Context, state: SharedAgentState) -> None:
    await ctx.send(
        state.user_sender_address,
        ChatMessage(
            timestamp=datetime.now(tz=timezone.utc),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=state.result),
                EndSessionContent(type="end-session"),
            ],
        ),
    )
