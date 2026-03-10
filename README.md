# fetch-help

A multi-agent system using the Fetch.ai framework with an orchestrator that routes messages to specialized agents (Alice and Bob).

## Setup

### 1. Configure environment

```bash
cp .env.example .env
```

Open `.env` and set a unique seed phrase for each agent. Seed phrases should be random strings with no spaces (tip: just mash your keyboard):

```
ALICE_SEED_PHRASE=your_random_seed_here
BOB_SEED_PHRASE=your_random_seed_here
ORCHESTRATOR_SEED_PHRASE=your_random_seed_here
```

### 2. Create virtual environment and install dependencies

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the agents

Each agent runs in its own terminal:

```bash
make orchestrator
```

```bash
make alice
```

```bash
make bob
```

## Testing via Agent Inspector

1. Open the **Orchestrator Agent Inspector** in your browser
2. Click **Connect**
![img.png](img.png)
3. Select **Mailbox**
![img_1.png](img_1.png)
4. Click **Go to Agent Profile**
![img_2.png](img_2.png)
5. Click **Chat with Agent**
![img_3.png](img_3.png)

### Example messages to try

```
i want to speak to alice
```

```
i want to speak to bob
```

```
hi
```
![img_4.png](img_4.png)
