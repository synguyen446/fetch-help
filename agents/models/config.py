import os
from dotenv import find_dotenv, load_dotenv
from uagents_core.identity import Identity

load_dotenv(find_dotenv())


ADMIN_SEED = os.getenv("ADMIN_SEED_PHRASE")
BOB_SEED = os.getenv("BOB_SEED_PHRASE")
ROUTER_SEED = os.getenv("ROUTER_SEED_PHRASE")
PROJECT_OVERVIEW_SEED = os.getenv("PROJECT_OVERVIEW_SEED_PHRASE")
API_SPEC_SEED = os.getenv("API_SPEC_SEED_PHRASE")
ARCHITECTURE_SEED = os.getenv("ARCHITECTURE_SEED_PHRASE")
DATA_MODEL_SEED = os.getenv("DATA_MODEL_SEED_PHRASE")
DEVOPS_SEED = os.getenv("DEVOPS_SEED_PHRASE")
REQUIREMENT_SEED = os.getenv("REQUIREMENT_SEED_PHRASE")
TESTING_STRATEGY_SEED = os.getenv("TESTING_STRATEGY_SEED_PHRASE")
USER_STORIES_SEED = os.getenv("USER_STORIES_SEED_PHRASE")


ADMIN_ADDRESS = Identity.from_seed(seed=ADMIN_SEED, index=0).address
BOB_ADDRESS = Identity.from_seed(seed=BOB_SEED, index=0).address
PROJECT_OVERVIEW_ADDRESS = Identity.from_seed(seed=PROJECT_OVERVIEW_SEED, index=0).address
API_SPEC_ADDRESS = Identity.from_seed(seed=API_SPEC_SEED, index=0).address
ARCHITECTURE_ADDRESS = Identity.from_seed(seed=ARCHITECTURE_SEED, index=0).address
DATA_MODEL_ADDRESS = Identity.from_seed(seed=DATA_MODEL_SEED, index=0).address
DEVOPS_ADDRESS = Identity.from_seed(seed=DEVOPS_SEED, index=0).address
REQUIREMENT_ADDRESS = Identity.from_seed(seed=REQUIREMENT_SEED, index=0).address
TESTING_STRATEGY_ADDRESS = Identity.from_seed(seed=TESTING_STRATEGY_SEED, index=0).address
USER_STORIES_ADDRESS = Identity.from_seed(seed=USER_STORIES_SEED, index=0).address
