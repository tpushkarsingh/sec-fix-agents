# run_bot.py  ── minimal CrewAI POC (GPT‑3.5, two agents)

import argparse, os
from pathlib import Path
from dotenv import load_dotenv
from pr_agent import pr_agent, open_pull_request
from crewai import Agent, Task, Crew, Process
import tempfile, subprocess
load_dotenv()

# ------------------- 3.  CLI arg for repo -----------
default_repo = os.getenv("REPO_TO_SCAN")
parser = argparse.ArgumentParser()
parser.add_argument(
    "--repo",
    default=default_repo,
    help="GitHub repo to scan",
)
args = parser.parse_args()
REPO_URL = args.repo
# ------------------- 4.  Define agents --------------
scanner = Agent(
    role="Security Scanner",
    goal="List vulnerable dependencies in the given repository.",
    backstory="I specialise in running Snyk CLI and parsing its JSON output.",
    verbose=True,
)

fixer = Agent(
    role="Dependency Fixer",
    goal="Suggest safe upgrades for each vulnerability.",
    backstory="I patch package files and ensure builds still pass.",
    verbose=True,
)

# ------------------- 5.  Tasks ----------------------
task_scan = Task(
    description=f"Scan the repo at {REPO_URL} for vulnerable dependencies.",
    expected_output="A list of vulnerabilities found in the codebase, including dependency names and severity.",
    agent=scanner,
    tool_args=lambda _: {"repo_dir": repo_dir}
)

task_fix = Task(
    description=(
        "Suggest secure fixes for each issue reported by the scanner."
    ),
    expected_output=(
        "Return a JSON array. Each item must have keys "
        "groupId, artifactId, and new (the new version).\n"
        "Output *only* the JSON—no markdown, no extra text."
    ),
    agent=fixer,
    tool_args=lambda _: {"repo_dir": repo_dir}
)

# run_bot.py
# ... (previous code)

task_pr = Task(
    description=(
        f"Open a pull-request on the repository located at '{REPO_URL}' " # <-- **CRITICAL CHANGE HERE**
        "with the dependency upgrades provided as input. "
        "You must use the open_pull_request tool, ensuring you pass the correct repository URL."
    ),
    expected_output="The GitHub PR URL.",
    agent=pr_agent,
    # When using context, the previous task's output is automatically made available
    # to the agent and the description.
    # The agent will then figure out how to call the tool with the right inputs from the context.
    context=[task_fix], # This ensures the output of task_fix is available as context
    tools=[open_pull_request] # The agent knows this tool is available
)





# ------------------- 6.  Crew run -------------------
crew = Crew(
    agents=[scanner, fixer, pr_agent],
    tasks=[task_scan, task_fix, task_pr],
    process=Process.sequential,
    verbose=True
)


if __name__ == "__main__":
    crew.kickoff()