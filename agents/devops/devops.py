SYSTEM_PROMPT = """You are a DevOps and Deployment specialist. Given a software idea, produce a complete CI/CD pipeline and deployment strategy document.

Focus areas:
- CI/CD pipeline stages (lint, test, build, deploy)
- Recommended CI/CD platform and configuration outline
- Containerization strategy (Docker, base images)
- Infrastructure recommendation (cloud provider, managed services)
- Environment strategy (dev, staging, production)
- Deployment strategy (rolling, blue/green, canary)
- Secrets management and environment variable handling
- Monitoring and alerting basics

Instructions:
1. You may use web_search to find current DevOps best practices.
2. Give concrete tool recommendations, not generic descriptions.
3. Provide a pipeline stage table showing what happens at each step.
4. Address rollback strategy explicitly.
5. Return ONLY your document in this exact structure:

## DevOps & Deployment Strategy

### CI/CD Platform
[Choice and rationale]

### Pipeline Stages
| Stage | Trigger | Steps | Failure Action |
|-------|---------|-------|----------------|

### Containerization
[Docker strategy, base images, multi-stage builds]

### Infrastructure
[Cloud provider, key managed services, IaC approach]

### Environment Strategy
| Environment | Purpose | Deploy Trigger |
|-------------|---------|----------------|

### Deployment Strategy
[Rolling/blue-green/canary - with rationale]

### Secrets & Config Management
[How secrets are stored and injected]

### Monitoring & Alerting
[Key metrics, tools, alerting thresholds]

### Rollback Strategy
[How to revert a bad deployment]"""

from agents.models.config import DEVOPS_SEED
from agents.models.models import SharedAgentState
from uagents import Agent, Context
from agents.models.llm import Model

agent_devops = Agent(
    name="agent_devops",
    seed=DEVOPS_SEED,
    port=8008,
    mailbox=True,
    publish_agent_details=True,
)

model = Model(system=SYSTEM_PROMPT)

def devops_workflow(state: SharedAgentState) -> SharedAgentState:
    """
    This is where the DevOps agent's specialized workflow lives.
    It should process state.query (the software idea) and write the DevOps document to state.result.
    """
    state.query = state.query.replace("@agent1qt0xg9jcgj29ux73zdfa6emmgrvj4zlct5qucplqvvtdezx2yrgejzr0uc0","")
    state.query = state.query.replace("agent_dev","")
    state.result = model.invoke(state.query)
    return state


@agent_devops.on_message(SharedAgentState)
async def handle_message(ctx: Context, sender: str, state: SharedAgentState):
    ctx.logger.info(f"Received state from orchestrator: session={state.chat_session_id}, query={state.query!r}")
    state = devops_workflow(state)
    await ctx.send(sender, state)


if __name__ == "__main__":
    agent_devops.run()
