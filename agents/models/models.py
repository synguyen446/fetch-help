from uagents import Model


class AgentState(Model):
    session_id: str
    query: str
    user_sender_address: str
