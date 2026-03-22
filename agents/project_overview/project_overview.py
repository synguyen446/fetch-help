SYSTEM_PROMPT = """You are a Project Overview specialist. Given a software idea, produce a compelling README-style project overview document.

Focus areas:
- A concise one-paragraph "what is this" description
- Problem statement: why this product needs to exist
- Target users and personas
- 4-6 key features (user-facing value, not implementation details)
- A creative but professional project name suggestion with brief rationale
- Positioning statement (how it differs from alternatives)

Instructions:
1. Read the idea carefully and identify the core value proposition.
2. Think about who the users are before listing features.
3. Keep language accessible - avoid jargon.
4. Return ONLY your document in this exact structure:

## Project Overview

### Project Name Suggestion
[Name] - [One sentence rationale]

### What Is This?
[1-2 paragraph description]

### Problem Statement
[Why this product is needed]

### Target Users
- [Persona 1]: [brief description]
- [Persona 2]: [brief description]

### Key Features
1. [Feature name]: [one sentence on the user value]

### Positioning
[How this differs from alternatives]"""

from agents.models.config import PROJECT_OVERVIEW_SEED
from agents.models.models import SharedAgentState
from uagents import Agent, Context
from agents.models.llm import Model

project_overview = Agent(
    name="agent_PO",
    seed=PROJECT_OVERVIEW_SEED,
    port=8004,
    mailbox=True,
    publish_agent_details=True,
)

model = Model(system=SYSTEM_PROMPT)

def project_overview_workflow(state: SharedAgentState) -> SharedAgentState:
    """
    This is where the Project Overview agent's specialized workflow lives.
    It should process state.query (the software idea) and write the project overview document to state.result.
    """
    # Placeholder implementation
    state.query = state.query.replace("@agent1qt0xg9jcgj29ux73zdfa6emmgrvj4zlct5qucplqvvtdezx2yrgejzr0uc0","")
    state.query = state.query.replace("project_overview","")
    state.result = model.invoke(state.query)
    return state



@project_overview.on_message(SharedAgentState)
async def handle_message(ctx: Context, sender: str, state: SharedAgentState):
    ctx.logger.info(f"Received state from orchestrator: session={state.chat_session_id}, query={state.query!r}")
    state = project_overview_workflow(state)
    await ctx.send(sender, state)


if __name__ == "__main__":
    project_overview.run()
