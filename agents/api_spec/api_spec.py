SYSTEM_PROMPT = """You are an API Design specialist. Given a software idea, produce a REST API specification document.

Focus areas:
- RESTful resource design and URL structure
- HTTP methods and status codes
- Request and response body schemas (JSON)
- Authentication and authorization model
- Pagination, filtering, and sorting patterns
- Error response format
- Rate limiting and versioning strategy

Instructions:
1. You may use web_search to look up REST API best practices or similar API designs.
2. Design endpoints around resources, not actions (REST principles).
3. Include realistic example request/response bodies.
4. Be explicit about which endpoints require authentication.
5. Return ONLY your document in this exact structure:

## API Specification

### Authentication
[Auth method - JWT, OAuth, API key - and how to pass it]

### Base URL & Versioning
`/api/v1/`

### Error Format
```json
{ "error": { "code": "...", "message": "...", "details": {} } }
```

### Endpoints

#### [Resource Name]
**GET /api/v1/[resource]**
Description: [what this does]
Auth required: Yes/No
Query params: `[param]`: [type] - [description]
Response 200:
```json
[example]
```"""

from agents.models.config import API_SPEC_SEED
from agents.models.models import SharedAgentState
from uagents import Agent, Context
from agents.models.llm import Model

agent_api_spec = Agent(
    name="agent_api_spec",
    seed=API_SPEC_SEED,
    port=8005,
    mailbox=True,
    publish_agent_details=True,
)

model = Model(system=SYSTEM_PROMPT)

def api_spec_workflow(state: SharedAgentState) -> SharedAgentState:
    """
    This is where the Project Overview agent's specialized workflow lives.
    It should process state.query (the software idea) and write the project overview document to state.result.
    """
    # Placeholder implementation
    state.query = state.query.replace("@agent1qt0xg9jcgj29ux73zdfa6emmgrvj4zlct5qucplqvvtdezx2yrgejzr0uc0","")
    state.query = state.query.replace("agent_api","")
    state.result = model.invoke(state.query)
    return state



@agent_api_spec.on_message(SharedAgentState)
async def handle_message(ctx: Context, sender: str, state: SharedAgentState):
    ctx.logger.info(f"Received state from orchestrator: session={state.chat_session_id}, query={state.query!r}")
    state = api_spec_workflow(state)
    await ctx.send(sender, state)


if __name__ == "__main__":
    agent_api_spec.run()
