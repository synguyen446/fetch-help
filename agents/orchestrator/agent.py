from agents.models.config import ORCHESTRATOR_SEED, ALICE_ADDRESS, BOB_ADDRESS
from uagents import Agent
from agents.orchestrator.chat_protocol import make_chat_protocol

orchestrator = Agent(
    name="orchestrator",
    seed=ORCHESTRATOR_SEED,
    port=8003,
    mailbox=True,
    publish_agent_details=True,
)

chat_proto = make_chat_protocol(ALICE_ADDRESS, BOB_ADDRESS)
orchestrator.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    orchestrator.run()
