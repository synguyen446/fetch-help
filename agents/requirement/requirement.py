SYSTEM_PROMPT = """You are a Requirements Engineering specialist. Given a software idea, produce a complete requirements document.

Focus areas:
- Functional requirements (what the system must DO)
- Non-functional requirements (performance, security, scalability, accessibility)
- Constraints (technical, regulatory, budget, time)
- Assumptions made about the product
- Out-of-scope items (what is explicitly NOT included)

Instructions:
1. Number all requirements: FR-001 for functional, NFR-001 for non-functional.
2. Write each requirement as a testable statement.
3. Group functional requirements by domain/feature area.
4. Be specific on non-functional numbers where possible (e.g., "p99 latency < 200ms").
5. Return ONLY your document in this exact structure:

## Requirements Document

### Functional Requirements
#### [Feature Area 1]
- FR-001: [requirement]

### Non-Functional Requirements
- NFR-001: [requirement]

### Constraints
- [constraint]

### Assumptions
- [assumption]

### Out of Scope
- [item]"""

from agents.models.config import REQUIREMENT_SEED
from agents.models.models import SharedAgentState
from uagents import Agent, Context
from agents.models.llm import Model

agent_requirement = Agent(
    name="agent_requirement",
    seed=REQUIREMENT_SEED,
    port=8009,
    mailbox=True,
    publish_agent_details=True,
)

model = Model(system=SYSTEM_PROMPT)

def requirement_workflow(state: SharedAgentState) -> SharedAgentState:
    """
    This is where the Requirement agent's specialized workflow lives.
    It should process state.query (the software idea) and write the requirements document to state.result.
    """
    state.query = state.query.replace("@agent1qt0xg9jcgj29ux73zdfa6emmgrvj4zlct5qucplqvvtdezx2yrgejzr0uc0","")
    state.query = state.query.replace("agent_req","")
    state.result = model.invoke(state.query)
    return state


@agent_requirement.on_message(SharedAgentState)
async def handle_message(ctx: Context, sender: str, state: SharedAgentState):
    ctx.logger.info(f"Received state from orchestrator: session={state.chat_session_id}, query={state.query!r}")
    state = requirement_workflow(state)
    await ctx.send(sender, state)


if __name__ == "__main__":
    agent_requirement.run()
