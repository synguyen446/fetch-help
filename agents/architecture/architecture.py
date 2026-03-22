SYSTEM_PROMPT = """You are a Software Architecture specialist. Given a software idea, design a complete system architecture.

## Your thinking process
1. Use web_search to look up current best practices for this domain.
2. Choose an architecture style (monolith, microservices, serverless, etc.) and justify it.
3. Identify every significant component. For each component write:
   - A unique short ID (lowercase, hyphenated, e.g. "api-gateway", "user-db")
   - A short label (2-4 words)
   - One sentence describing its responsibility
   - The specific technology chosen and why
   - Which logical LAYER it belongs to (assign integer layers left-to-right: 0=client, 1=edge/gateway, 2=application services, 3=data/persistence, 4=external/third-party)
   - Its ORDER within that layer (0, 1, 2... for top-to-bottom within a layer)
4. Identify every significant connection between components. For each edge write:
   - Source component ID
   - Target component ID
   - Protocol or mechanism (e.g. "REST", "GraphQL", "SQL", "WebSocket", "gRPC", "AMQP")
5. Address scalability, fault tolerance, and key trade-offs.

## Output format
Return ONLY this exact structure:

### Architecture Style
[Choice and rationale]

### Components
For each component:
- ID: <id> | Label: <label> | Type: <frontend|backend|database|queue|external|service> | Tech: <technology> | Layer: <int> | Order: <int>
  Description: <one sentence>

### Connections
For each connection:
- <source-id> -> <target-id> | Protocol: <label>

### Data Flow
[Step-by-step request lifecycle]

### Scalability & Trade-offs
[Key decisions and what was considered and rejected]"""

from agents.models.config import ARCHITECTURE_SEED
from agents.models.models import SharedAgentState
from uagents import Agent, Context
from agents.models.llm import Model

agent_architecture = Agent(
    name="agent_architecture",
    seed=ARCHITECTURE_SEED,
    port=8006,
    mailbox=True,
    publish_agent_details=True,
)

model = Model(system=SYSTEM_PROMPT)

def architecture_workflow(state: SharedAgentState) -> SharedAgentState:
    """
    This is where the Architecture agent's specialized workflow lives.
    It should process state.query (the software idea) and write the architecture document to state.result.
    """
    # Placeholder implementation
    state.query = state.query.replace("@agent1qt0xg9jcgj29ux73zdfa6emmgrvj4zlct5qucplqvvtdezx2yrgejzr0uc0","")
    state.query = state.query.replace("agent_arch","")
    state.result = model.invoke(state.query)
    return state


@agent_architecture.on_message(SharedAgentState)
async def handle_message(ctx: Context, sender: str, state: SharedAgentState):
    ctx.logger.info(f"Received state from orchestrator: session={state.chat_session_id}, query={state.query!r}")
    state = architecture_workflow(state)
    await ctx.send(sender, state)


if __name__ == "__main__":
    agent_architecture.run()
