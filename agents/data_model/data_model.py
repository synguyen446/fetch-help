SYSTEM_PROMPT = """You are a Data Modeling specialist. Given a software idea, produce a complete database schema and entity-relationship document.

Focus areas:
- Entity identification (what are the core data objects?)
- Attribute definition with data types and constraints
- Relationships between entities (one-to-many, many-to-many, etc.)
- Primary keys, foreign keys, and indexes
- Database engine recommendation and rationale
- Data integrity rules and validation
- Soft deletes, audit trails, and timestamps

Instructions:
1. List all entities first, then define relationships.
2. Use standard SQL-style type names (VARCHAR, INTEGER, TIMESTAMP, etc.).
3. Mark primary keys (PK), foreign keys (FK), and unique constraints (UQ) explicitly.
4. Include an ER diagram in simple ASCII or table notation.
5. Return ONLY your document in this exact structure:

## Data Model

### Database Recommendation
[Engine choice and rationale]

### Entities

#### [EntityName]
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id     | UUID | PK          | Primary key |

### Relationships
- [EntityA] has many [EntityB] via [foreign_key]

### Entity-Relationship Diagram
```
[ASCII ER diagram]
```

### Indexes
- [table].[column] - [reason for index]

### Data Integrity Notes
[Soft deletes, audit fields, cascades, etc.]"""

from agents.models.config import DATA_MODEL_SEED
from agents.models.models import SharedAgentState
from uagents import Agent, Context
from agents.models.llm import Model

agent_data_model = Agent(
    name="agent_data_model",
    seed=DATA_MODEL_SEED,
    port=8007,
    mailbox=True,
    publish_agent_details=True,
)

model = Model(system=SYSTEM_PROMPT)

def data_model_workflow(state: SharedAgentState) -> SharedAgentState:
    """
    This is where the Data Model agent's specialized workflow lives.
    It should process state.query (the software idea) and write the data model document to state.result.
    """
    state.query = state.query.replace("@agent1qt0xg9jcgj29ux73zdfa6emmgrvj4zlct5qucplqvvtdezx2yrgejzr0uc0","")
    state.query = state.query.replace("agent_dm","")
    state.result = model.invoke(state.query)
    return state


@agent_data_model.on_message(SharedAgentState)
async def handle_message(ctx: Context, sender: str, state: SharedAgentState):
    ctx.logger.info(f"Received state from orchestrator: session={state.chat_session_id}, query={state.query!r}")
    state = data_model_workflow(state)
    await ctx.send(sender, state)


if __name__ == "__main__":
    agent_data_model.run()
