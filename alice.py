from datetime import datetime, timezone
from uuid import uuid4
from uagents import Agent, Context, Protocol
from uagents_core.identity import Identity
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import (
   ChatAcknowledgement,
   ChatMessage,
   EndSessionContent,
   StartSessionContent,
   TextContent,
   chat_protocol_spec,
)
from models import *

import os
from dotenv import load_dotenv

load_dotenv()

alice = Agent(name="alice", seed=os.getenv("ALICE_SEED_PHRASE"), port=8001, endpoint=["http://localhost:8001/submit"])

# Initialize the chat protocol with the standard chat spec
chat_proto = Protocol(spec=chat_protocol_spec)

# Lets get Bob's address so we can send him messages
BOB_IDENTITY = Identity.from_seed(seed=str(os.getenv("BOB_SEED_PHRASE")), index=0)
BOB_ADDRESS = BOB_IDENTITY.address

# This is so Alice can regsiter for almanac contract. Almanac costs a little bit of money to register
# Don't worry, we're using test funds
fund_agent_if_low(str(alice.wallet.address()))

@alice.on_event("startup")
async def introduce_agent(ctx: Context):
    pass

# @alice.on_interval(period=5.0)
# async def ping_bob(ctx: Context):
#     await ctx.send(BOB_ADDRESS, Message(content="Hello this is Alice"))
#     ctx.logger.info("Sent message to Bob")

@alice.on_message(model=Message)
async def echo(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Got response: {msg.content}")


# Handle incoming chat messages
@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received message from {sender}")

    # Always send back an acknowledgement when a message is received
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    response = "sdlkjfdsjlf"

    # Process each content item inside the chat message
    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.now(tz=timezone.utc),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=response),
                EndSessionContent(type="end-session"),
            ],
        )
    )


# Handle acknowledgements for messages this agent has sent out
@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
   ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

alice.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    alice.run()
