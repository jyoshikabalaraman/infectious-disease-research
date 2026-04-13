# Global Health Research Agent

An autonomous AI agent that researches infectious disease economics and policy in low- and middle-income countries. Give it a country, a disease, and a focus area — it handles the rest.

The agent decides what to search, evaluates results, identifies gaps, searches again from new angles, and produces a structured research brief. No human input between start and finish.

## Setup

**1. Install Python** (skip if you already have it)

Download from [python.org/downloads](https://www.python.org/downloads/). Check the "Add Python to PATH" box during install.

**2. Install the Anthropic SDK**

```bash
pip install anthropic
```

**3. Get an API key**

Sign up at [console.anthropic.com](https://console.anthropic.com), go to Settings → API Keys, and create one.

**4. Set your key**

Mac/Linux:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Windows (Command Prompt):
```bash
set ANTHROPIC_API_KEY=your-key-here
```

Windows (PowerShell):
```bash
$env:ANTHROPIC_API_KEY="your-key-here"
```

You need to do this each time you open a new terminal.

## Run

```bash
python research_agent.py
```

It'll ask for a country, disease, and focus area (economic, policy, epidemiology, or all). Then the agent takes over — you'll see it making searches and thinking in real time. Takes 1-3 minutes.

Output prints to the terminal and saves as a `.md` file in the same folder.

## Example

```
$ python research_agent.py

  Country or region: Nigeria
  Disease: Malaria
  Focus: 1 (Economic impact)

  [Search #1] "malaria economic burden Nigeria 2024"
  [Search #2] "Nigeria malaria financing Global Fund"
  [Search #3] "malaria treatment costs Nigeria households"
  [Search #4] "Nigeria national malaria policy budget"
  [Search #5] "artemisinin drug costs Nigeria"

  Agent completed after 5 autonomous searches.
  Saved to: research_brief_nigeria_malaria_20260412_143022.md
```

## What's in the Output

- **Executive Summary** — overview of findings
- **Key Findings** — organized by theme
- **Economic Dimensions** — costs, funding, burden
- **Policy Landscape** — current policies and governance
- **Recent Developments** — what's changed lately
- **Knowledge Gaps** — what the agent couldn't find, where sources conflicted, what needs deeper research
- **Key Sources** — links to sources used

## Troubleshooting

| Problem | Fix |
|---|---|
| `command not found: python` | Install Python (see step 1) |
| `No module named anthropic` | Run `pip install anthropic` |
| `ANTHROPIC_API_KEY not set` | Set your key (see step 4) |
| `API Error: 401` | Key is invalid — check it at console.anthropic.com |
| Agent seems stuck | Give it up to 3 min. `Ctrl+C` to stop if needed |

## License

MIT
