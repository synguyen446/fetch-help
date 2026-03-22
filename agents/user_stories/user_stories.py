SYSTEM_PROMPT = """You are a Product Manager and User Story specialist. Given a software idea, produce a complete product backlog.

Focus areas:
- 2-4 distinct user personas with goals and pain points
- Epics that map to major feature areas
- User stories: "As a [persona], I want [goal] so that [reason]"
- Acceptance criteria for each story
- Priority label: Must Have / Should Have / Could Have

Instructions:
1. Create personas before writing stories - stories must reference a defined persona.
2. Write 3-5 stories per epic minimum.
3. Each story must have at least 2 acceptance criteria.
4. Mark priority clearly.
5. Return ONLY your document in this exact structure:

## User Stories & Product Backlog

### User Personas
#### [Persona Name]
- Role: [job or context]
- Goal: [what they want to achieve]
- Pain Point: [current frustration]

### Epics & User Stories

#### Epic 1: [Epic Name]
**US-001** [Priority: Must Have]
As a [persona], I want [goal] so that [reason].
Acceptance Criteria:
- [ ] [criterion]
- [ ] [criterion]"""

from agents.models.config import USER_STORIES_SEED
from agents.models.models import SharedAgentState
from uagents import Agent, Context
from agents.models.llm import Model

agent_user_stories = Agent(
    name="agent_user_stories",
    seed=USER_STORIES_SEED,
    port=8011,
    mailbox=True,
    publish_agent_details=True,
)

model = Model(system=SYSTEM_PROMPT)

def user_stories_workflow(state: SharedAgentState) -> SharedAgentState:
    """
    This is where the User Stories agent's specialized workflow lives.
    It should process state.query (the software idea) and write the user stories document to state.result.
    """
    state.query = state.query.replace("@agent1qt0xg9jcgj29ux73zdfa6emmgrvj4zlct5qucplqvvtdezx2yrgejzr0uc0","")
    state.query = state.query.replace("agent_ustory","")
    state.result = model.invoke(state.query)
    return state


@agent_user_stories.on_message(SharedAgentState)
async def handle_message(ctx: Context, sender: str, state: SharedAgentState):
    ctx.logger.info(f"Received state from orchestrator: session={state.chat_session_id}, query={state.query!r}")
    state = user_stories_workflow(state)
    await ctx.send(sender, state)


if __name__ == "__main__":
    agent_user_stories.run()
