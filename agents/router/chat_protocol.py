from datetime import datetime, timezone
from uuid import uuid4

from uagents import Context, Protocol
from agents.models.config import (
    ADMIN_ADDRESS,
    BOB_ADDRESS,
    PROJECT_OVERVIEW_ADDRESS,
    API_SPEC_ADDRESS,
    ARCHITECTURE_ADDRESS,
    DATA_MODEL_ADDRESS,
    DEVOPS_ADDRESS,
    REQUIREMENT_ADDRESS,
    TESTING_STRATEGY_ADDRESS,
    USER_STORIES_ADDRESS,
)
from agents.models.models import SharedAgentState
from agents.services.state_service import state_service
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

    chat_session_id = str(ctx.session)
    state = state_service.get_state(chat_session_id)

    if state is None:
        state = SharedAgentState(
            chat_session_id=chat_session_id,
            query=text,
            user_sender_address=sender,
        )
        state_service.set_state(chat_session_id, state)
    else:
        state.query = text


    response = None
    routed = False

    if "@dm1n" in text.lower():
        await ctx.send(ADMIN_ADDRESS, state)
        ctx.logger.info("Routing to Admin!")
        routed = True
    if "bob" in text.lower():
        await ctx.send(BOB_ADDRESS, state)
        ctx.logger.info("Routing to Bob!")
        routed = True
    if "agent_po" in text.lower():
        await ctx.send(PROJECT_OVERVIEW_ADDRESS, state)
        ctx.logger.info("Routing to PO!")
        routed = True
    if "agent_api" in text.lower():
        await ctx.send(API_SPEC_ADDRESS, state)
        ctx.logger.info("Routing to API Spec!")
        routed = True
    if "agent_arch" in text.lower():
        await ctx.send(ARCHITECTURE_ADDRESS, state)
        ctx.logger.info("Routing to Architecture!")
        routed = True
    if "agent_dm" in text.lower():
        await ctx.send(DATA_MODEL_ADDRESS, state)
        ctx.logger.info("Routing to Data Model!")
        routed = True
    if "agent_dev" in text.lower():
        await ctx.send(DEVOPS_ADDRESS, state)
        ctx.logger.info("Routing to DevOps!")
        routed = True
    if "agent_req" in text.lower():
        await ctx.send(REQUIREMENT_ADDRESS, state)
        ctx.logger.info("Routing to Requirement!")
        routed = True
    if "agent_test" in text.lower():
        await ctx.send(TESTING_STRATEGY_ADDRESS, state)
        ctx.logger.info("Routing to Testing Strategy!")
        routed = True
    if "agent_ustory" in text.lower():
        await ctx.send(USER_STORIES_ADDRESS, state)
        ctx.logger.info("Routing to User Stories!")
        routed = True

    if not routed:
        response = "Mention a specific agent (e.g., Admin, Bob, Project_Overview, API_Spec, Architecture, Data_Model, DevOps, Requirement, Testing_Strategy, User_Stories) in your message and I'll route it to them."

    if response:
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


def generate_orchestrator_response_from_state(state: SharedAgentState) -> str:
    return state.result
