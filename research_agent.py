"""
Global Health Research Agent
=============================
An agentic AI system that autonomously researches infectious disease
topics with a focus on economic and policy dimensions in low- and
middle-income countries.

Built for Dr. Stefano Bertozzi's research group at UC Berkeley.

HOW IT'S AGENTIC:
  Unlike a simple chatbot or Google search, this agent:
  1. Receives a high-level research goal (country + disease + focus area)
  2. Autonomously decides what to search for — no human picks the queries
  3. Reads results and evaluates what's useful vs. what's missing
  4. Decides to search again from different angles to fill gaps
  5. Determines on its own when it has enough information to stop
  6. Produces a structured research brief WITH identified knowledge gaps

  The human presses "go" once. Everything between that and the final
  output is the agent making its own decisions.

USAGE:
  1. pip install anthropic
  2. export ANTHROPIC_API_KEY="your-key-here"
  3. python research_agent.py

REQUIREMENTS:
  - Python 3.9+
  - anthropic Python SDK (pip install anthropic)
  - An Anthropic API key with web search access
"""

import anthropic
import json
import sys
import os
from datetime import datetime



MODEL = "claude-sonnet-4-20250514"
MAX_AGENT_TURNS = 15  

SYSTEM_PROMPT = """You are a global health research agent specializing in infectious disease 
economics and policy, particularly in low- and middle-income countries (LMICs).

You have access to a web search tool. Your job is to AUTONOMOUSLY research a given topic 
by making multiple searches from different angles until you have enough information to 
produce a comprehensive research brief.

## Your Research Process (you decide each step autonomously):

1. START by searching for the most important/recent information on the topic
2. EVALUATE what you found — what's solid? What's missing?
3. SEARCH AGAIN from a different angle to fill gaps (e.g., if you found epidemiological 
   data but no economic analysis, search for economic impact next)
4. REPEAT steps 2-3 until you have sufficient coverage across these dimensions:
   - Current epidemiological situation
   - Economic impact and costs
   - Existing policies and interventions
   - Recent developments or changes
   - Key stakeholders and organizations involved
5. When you have enough information, produce your final research brief

## Output Format (use this EXACTLY when you're ready):

---BEGIN RESEARCH BRIEF---

# [Topic Title]
**Country/Region:** [country]
**Disease:** [disease]  
**Focus:** [economic/policy/epidemiological]
**Date Compiled:** [today's date]

## Executive Summary
[2-3 paragraph overview of key findings]

## Key Findings
[Organized by theme — present the most important discoveries from your research]

## Economic Dimensions
[Costs, funding, economic burden, financial mechanisms — whatever is relevant]

## Policy Landscape
[Current policies, recent changes, key decisions, political dynamics]

## Recent Developments
[What's new or changing — within the last 1-2 years ideally]

## Knowledge Gaps & Areas Needing Clarification
[CRITICAL SECTION — Be specific about:]
- What information you searched for but couldn't find
- Where sources contradicted each other
- Topics where data is outdated or insufficient
- Questions that would require primary research or expert consultation
- Areas where the evidence base is thin

## Key Sources
[List the most important sources you found]

---END RESEARCH BRIEF---

IMPORTANT RULES:
- Make at least 3-4 searches before producing your brief
- Each search should target a DIFFERENT angle of the topic
- Be honest about what you couldn't find — the Knowledge Gaps section is the most 
  valuable part for a researcher
- Focus on LMICs and global health perspectives
- Prioritize recent information (last 2-3 years)
- Do NOT fabricate information — if you can't find it, say so in Knowledge Gaps
"""


def create_client():
    """Initialize the Anthropic client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n" + "=" * 60)
        print("  ERROR: ANTHROPIC_API_KEY not set")
        print("=" * 60)
        print("\n  To set your API key:\n")
        print("  On Mac/Linux:")
        print('    export ANTHROPIC_API_KEY="your-key-here"')
        print("\n  On Windows:")
        print('    set ANTHROPIC_API_KEY=your-key-here')
        print("\n  Get a key at: https://console.anthropic.com/")
        print()
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def get_user_input():
    """Collect research parameters from the user."""
    print("\n" + "=" * 60)
    print("  GLOBAL HEALTH RESEARCH AGENT")
    print("  Autonomous AI-Powered Research Assistant")
    print("=" * 60)

    print("\n  This agent will autonomously research a global health")
    print("  topic and produce a structured brief with knowledge gaps.\n")

    print("-" * 40)
    country = input("  Country or region to research:\n  > ").strip()
    if not country:
        country = "Sub-Saharan Africa"
        print(f"  (defaulting to: {country})")

    print()
    disease = input("  Disease or health topic:\n  > ").strip()
    if not disease:
        disease = "Malaria"
        print(f"  (defaulting to: {disease})")

    print("\n  Research focus area:")
    print("    1. Economic impact & costs")
    print("    2. Policy & governance")
    print("    3. Epidemiology & burden")
    print("    4. Interventions & programs")
    print("    5. All of the above")
    focus_choice = input("  > Choose (1-5): ").strip()

    focus_map = {
        "1": "economic impact, costs, financing, and economic burden",
        "2": "policy landscape, governance, regulations, and political dynamics",
        "3": "epidemiological burden, prevalence, incidence, and mortality trends",
        "4": "interventions, programs, treatment strategies, and their effectiveness",
        "5": "comprehensive overview including economic, policy, epidemiological, and intervention dimensions",
    }
    focus = focus_map.get(focus_choice, focus_map["5"])

    print()
    additional = input(
        "  Any specific questions or context? (Enter to skip):\n  > "
    ).strip()

    return country, disease, focus, additional


def run_agent(client, country, disease, focus, additional_context=""):
    """
    Run the agentic research loop.

    This is the core "agentic" part: the AI runs in a loop, autonomously
    deciding what to search for, evaluating results, and determining when
    it has enough information to produce its final output.
    """

    user_message = f"""Please research the following topic autonomously:

**Country/Region:** {country}
**Disease/Health Topic:** {disease}
**Research Focus:** {focus}
**Date:** {datetime.now().strftime('%B %d, %Y')}
"""
    if additional_context:
        user_message += f"\n**Additional Context/Questions:** {additional_context}\n"

    user_message += """
Begin your autonomous research now. Make multiple searches from different angles, 
evaluate what you find, identify gaps, and produce a comprehensive research brief 
when you have sufficient information. Remember: at least 3-4 searches from different 
angles before synthesizing."""

    print("\n" + "=" * 60)
    print("  AGENT STARTING AUTONOMOUS RESEARCH")
    print("=" * 60)
    print(f"\n  Topic:  {disease} in {country}")
    print(f"  Focus:  {focus}")
    print(f"\n  The agent will now autonomously:")
    print(f"    - Decide what to search for")
    print(f"    - Evaluate results and identify gaps")
    print(f"    - Search again from different angles")
    print(f"    - Synthesize findings into a research brief")
    print(f"\n  No human input needed until completion.\n")
    print("-" * 60)

    messages = [{"role": "user", "content": user_message}]

    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 20}]

    turn_count = 0
    search_count = 0
    final_output = ""

   
    while turn_count < MAX_AGENT_TURNS:
        turn_count += 1

        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=8096,
                system=SYSTEM_PROMPT,
                tools=tools,
                messages=messages,
            )
        except anthropic.APIError as e:
            print(f"\n  ERROR: API call failed - {e}")
            break

        assistant_content = response.content
        full_text = ""

        for block in assistant_content:
            if block.type == "text":
                full_text += block.text
            elif block.type == "server_tool_use":
                if block.name == "web_search":
                    search_count += 1
                    query = block.input.get("query", "unknown")
                    print(f"  [Search #{search_count}] \"{query}\"")

        for line in full_text.split("\n"):
            line = line.strip()
            if (
                line
                and not line.startswith("#")
                and not line.startswith("**")
                and not line.startswith("---")
                and not line.startswith("-")
                and not line.startswith("[")
                and len(line) > 20
            ):
                preview = line[:120] + "..." if len(line) > 120 else line
                print(f"  [Thinking] {preview}")
                break 

        messages.append({"role": "assistant", "content": assistant_content})

        if "---END RESEARCH BRIEF---" in full_text:
            start = full_text.find("---BEGIN RESEARCH BRIEF---")
            end = full_text.find("---END RESEARCH BRIEF---") + len(
                "---END RESEARCH BRIEF---"
            )
            if start != -1:
                final_output = full_text[start:end]
            else:
                final_output = full_text
            print(f"\n  Agent completed after {search_count} autonomous searches.")
            break

        if response.stop_reason == "end_turn":
            if full_text.strip():
                final_output = full_text
                print(f"\n  Agent finished after {search_count} searches.")
            break

    else:
        print(f"\n  Agent reached safety limit ({MAX_AGENT_TURNS} turns).")
        for msg in reversed(messages):
            if isinstance(msg.get("content"), list):
                for block_data in msg["content"]:
                    if hasattr(block_data, "text") and block_data.text:
                        final_output = block_data.text
                        break
            if final_output:
                break

    return final_output, search_count, turn_count


def save_output(brief, country, disease):
    """Save the research brief to a markdown file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_country = country.replace(" ", "_").replace("/", "-").lower()
    safe_disease = disease.replace(" ", "_").replace("/", "-").lower()
    filename = f"research_brief_{safe_country}_{safe_disease}_{timestamp}.md"

    with open(filename, "w") as f:
        f.write(brief)

    return filename


def main():
    """Main entry point."""
    client = create_client()

    country, disease, focus, additional = get_user_input()

    brief, searches, turns = run_agent(client, country, disease, focus, additional)

    if not brief:
        print("\n  Agent did not produce output. Try again.\n")
        return

    print("\n" + "=" * 60)
    print("  RESEARCH BRIEF")
    print("=" * 60)
    print(brief)

    filename = save_output(brief, country, disease)
    print("\n" + "=" * 60)
    print(f"  Saved to: {filename}")
    print(f"  Stats:    {searches} searches, {turns} reasoning turns")
    print("=" * 60)

    print()
    again = input("  Research another topic? (y/n): ").strip().lower()
    if again == "y":
        main()
    else:
        print("\n  Done. Happy researching!\n")


if __name__ == "__main__":
    main()
