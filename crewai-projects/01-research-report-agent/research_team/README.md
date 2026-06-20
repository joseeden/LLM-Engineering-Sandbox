# ResearchTeam Crew

## Overview

This CrewAI project runs a small research report workflow.

It has two agents:

| Agent | Purpose |
| --- | --- |
| `researcher` | Searches the web with a local SearXNG tool and collects findings with source URLs. |
| `reporting_analyst` | Turns the research findings into a Markdown report. |

The researcher is the only agent with direct tool access. The reporting analyst receives the research output as context from the previous task.

## Workflow

1. `main.py` provides the topic and current year.
2. CrewAI loads the agents from `src/research_team/config/agents.yaml`.
3. CrewAI loads the tasks from `src/research_team/config/tasks.yaml`.
4. `research_task` runs first and uses the SearXNG search tool.
5. `reporting_task` runs second and writes `report.md`.

The task order is controlled by the `@task` method order in `src/research_team/crew.py` because the crew uses `Process.sequential`.

## Tools

The custom tool lives in:

```text
src/research_team/tools/custom_tool.py
```

`SearxNGSearchTool` calls the local SearXNG JSON endpoint:

```text
GET {SEARXNG_URL}/search?q=...&format=json&categories=general
```

The tool accepts:

- `query`
- `count`
- `time_range`

The tool returns a compact JSON list with result titles, URLs, and descriptions.

If SearXNG is not running, the tool returns a clear error message telling you to start the local container.

## Setup

1. Go to this folder.

    ```bash
    cd project-llm-engineering-sandbox/crewai-projects/01-research-report-agent/research_team
    ```

2. Copy the environment file.

    ```bash
    cp .env.example .env
    ```

3. Configure environment variables.

    ```env
    MODEL=gpt-4.1-mini-2025-04-14
    OPENAI_API_KEY=your_openai_key_here
    SEARXNG_URL=http://localhost:8080
    SEARXNG_SECRET=your_generated_searxng_secret_here
    ```

4. Install dependencies.

    ```bash
    uv sync
    ```

5. Verify CrewAI.

    ```bash
    uv run crewai --version
    ```

## Setup - SearXNG

SearXNG runs locally in Docker, so the project can search the web without a paid search API key.

1. Copy the SearXNG config.

    ```bash
    cp searxng/settings.yml.example searxng/settings.yml
    ```

2. Generate a local secret.

    ```bash
    openssl rand -hex 32
    ```

    Add it to `.env` as `SEARXNG_SECRET`.

3. Start SearXNG.

    ```bash
    docker run --name searxng-local \
      -d \
      -p 8080:8080 \
      --env-file .env \
      -v "$(pwd)/searxng:/etc/searxng" \
      searxng/searxng:latest
    ```

    Windows PowerShell:

    ```powershell
    docker run --name searxng-local -d -p 8080:8080 --env-file .env -v "${PWD}/searxng:/etc/searxng" searxng/searxng:latest
    ```

4. Test the JSON API.

    ```bash
    curl -s "http://localhost:8080/search?q=AI%20agents&format=json" | jq
    ```

Useful Docker commands:

```bash
docker ps
docker stop searxng-local
docker start searxng-local
docker logs searxng-local
```

## Run

Run the CrewAI workflow:

```bash
uv run crewai run
```

By default, the workflow researches `AI LLMs`. You can change the topic in:

```text
src/research_team/main.py
```

The final report is saved to:

```text
report.md
```
