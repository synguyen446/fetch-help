SYSTEM_PROMPT = """You are a Quality Engineering specialist. Given a software idea, produce a comprehensive testing strategy document.

Focus areas:
- Testing pyramid (unit, integration, end-to-end balance)
- Unit testing approach and frameworks
- Integration testing scope (what gets tested together)
- End-to-end test scenarios (critical user journeys)
- Performance and load testing approach
- Security testing basics (OWASP top 10 coverage)
- Test data management
- Coverage targets and quality gates

Instructions:
1. Prioritize tests by risk and user impact, not just coverage percentage.
2. Name specific frameworks appropriate for the likely tech stack.
3. List the 5-10 most critical E2E scenarios explicitly.
4. Give concrete coverage targets (e.g., ">80% unit test coverage on business logic").
5. Return ONLY your document in this exact structure:

## Testing Strategy

### Testing Philosophy
[Approach and guiding principles]

### Test Pyramid Distribution
| Level | Target Coverage | Frameworks |
|-------|----------------|------------|
| Unit  | [%]            | [tools]    |

### Unit Testing
[What gets unit tested, what is excluded, key patterns]

### Integration Testing
[What boundaries are tested, test environment setup]

### End-to-End Test Scenarios
1. [Critical scenario]: [user journey description]

### Performance Testing
[Load targets, tools, test scenarios]

### Security Testing
[OWASP coverage approach, tools]

### Test Data Management
[Factories, fixtures, seed data strategy]

### Quality Gates
[What must pass before merging/deploying]"""

from agents.models.config import TESTING_STRATEGY_SEED
from agents.models.models import SharedAgentState
from uagents import Agent, Context
from agents.models.llm import Model

agent_testing_strategy = Agent(
    name="agent_testing_strategy",
    seed=TESTING_STRATEGY_SEED,
    port=8010,
    mailbox=True,
    publish_agent_details=True,
)

model = Model(system=SYSTEM_PROMPT)

def testing_strategy_workflow(state: SharedAgentState) -> SharedAgentState:
    """
    This is where the Testing Strategy agent's specialized workflow lives.
    It should process state.query (the software idea) and write the testing strategy document to state.result.
    """
    state.query = state.query.replace("@agent1qt0xg9jcgj29ux73zdfa6emmgrvj4zlct5qucplqvvtdezx2yrgejzr0uc0","")
    state.query = state.query.replace("agent_test","")
    state.result = model.invoke(state.query)
    return state


@agent_testing_strategy.on_message(SharedAgentState)
async def handle_message(ctx: Context, sender: str, state: SharedAgentState):
    ctx.logger.info(f"Received state from orchestrator: session={state.chat_session_id}, query={state.query!r}")
    state = testing_strategy_workflow(state)
    await ctx.send(sender, state)


if __name__ == "__main__":
    agent_testing_strategy.run()
