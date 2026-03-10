import os
from dotenv import load_dotenv
from uagents_core.identity import Identity

load_dotenv()

_ALICE_SEED = "soiufisdfkjsjflksdowo24792834"
_BOB_SEED = os.getenv("BOB_SEED_PHRASE")
_ORCHESTRATOR_SEED = os.getenv("ORCHESTRATOR_SEED_PHRASE")

ALICE_ADDRESS = Identity.from_seed(seed=_ALICE_SEED, index=0).address
BOB_ADDRESS = Identity.from_seed(seed=_BOB_SEED, index=0).address
