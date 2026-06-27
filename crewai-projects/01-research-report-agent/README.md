# CrewAI Research Report Agent

## Overview

This project demonstrates a small multi-agent research workflow using CrewAI.

It creates a research crew with two agents:

- First agent searches the web using SearXNG and gathers findings about a topic
- Second agent turns those findings into a structured Markdown report

The project is intentionally compact. It is useful for understanding how CrewAI organizes agents, tasks, configuration, and execution without adding too many custom abstractions.

**Note:** This is the main README for this project. However, CrewAI also generates a README in the `research_team` folder. That README is more focused on the code and structure of the research crew itself.

## Project Workflow

The workflow runs in a simple sequence.

1. User provides the research topic and current year
2. CrewAI loads the agent and task definitions from the YAML files.
3. CrewAI creates a crew using the agents and tasks defined in `crew.py`.
4. The researcher agent runs the research task and uses the SearXNG tool.
5. The reporting analyst agent receives the result and source URLs as context.
6. The reporting analyst writes the final Markdown report with sources.
7. The report is saved as `report.md`

## Use Case

Research tasks often involve two separate activities:

1. Gathering useful information
2. Turning that information into a readable report

This project shows how that process can be modeled as a small team of AI agents. Each agent has a clear role, goal, and backstory, while the tasks define what each agent should produce.

In this project, the researcher agent uses a tool instead of relying only on the model's internal knowledge. This is closer to real-world agent workflows, where agents call external systems such as search engines, databases, APIs, and internal knowledge bases.

<!-- It is not a production research platform yet. It is a focused learning project that demonstrates the core CrewAI pattern before adding tools, web search, persistence, evaluation, or human review. -->

<!-- ## Project Structure

```text
01-crewai-research-report-agent/
|
├── knowledge/
│   └── user_preference.txt
│
├── src/
│   └── research_team/
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       ├── tools/
│       │   ├── __init__.py
│       │   └── custom_tool.py
│       ├── __init__.py
│       ├── crew.py
│       └── main.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
``` -->

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [CrewAI](https://docs.crewai.com/)
- [An OpenAI API key (or another model provider supported by CrewAI)](https://platform.openai.com/account/api-keys)
- [Docker Desktop/Docker](https://docs.docker.com/engine/install/)
- [jq](https://jqlang.org/download/)


## Setup

1. Clone the repository.

    ```bash
    git clone https://github.com/joseeden/llm-engineering-sandbox
    cd project-llm-engineering-sandbox/crewai-projects/01-research-report-agent/research_team
    ```

2. Copy the environment file.

    ```bash
    cp .env.example .env
    ```

3. Configure environment variables.

    Open `.env` and set your API key.

    **NOTE:** Never commit real API keys to source control.

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

    **Note:** `crewai` has been added in the `pyproject.toml` file, so it will be installed into the virtual environment created by `uv`.

    Alternatively, you can also use the CrewAI CLI from the project directory:

    ```bash
    crewai install
    ```

5. Verify installation.

    ```bash
    crewai --version
    ```

**UPDATE:** `uv sync` only installs the dependencies into the project's virtual environment. It does not automatically put CLI commands like `crewai` into the shell's PATH. 

To run `crewai` commands, you can either:

1. Use the `uv run` command to run the CLI commands.

    ```bash
    uv run crewai --version
    ```

    Output:

    ```bash
    crewai, version 0.203.2
    ```

    This means anytime you want to run a `crewai` command, you will need to prefix it with `uv run`.

    You can also verify if CrewAI was installed correctly by running:

    ```bash
    uv run crewai --version
    ```

    Output:

    ```bash
    Name: crewai
    Version: 0.203.2
    ```

2. Activate the virtual environment created by `uv`.

    ```bash
    source .venv/bin/activate
    ```

    After activation, you can run `crewai` commands directly without the `uv run` prefix.

    ```bash
    crewai --version
    ```

## Setup - SearXNG

To enable the researcher agent to search the web, it needs to use a search tool. There are different ways to implement a search tool, but for this project, we will use SearXNG, an open-source metasearch engine which we can run locally in Docker.

1. Install Docker Desktop.

    Linux/Mac: Install Docker Engine from the official Docker installation page:

    ```text
    https://docs.docker.com/engine/install/
    ```

    Windows: Download Docker Desktop from the official Docker installation page:

    ```text
    https://docs.docker.com/desktop/setup/install/windows-install/
    ```

    Run `Docker Desktop Installer.exe`, keep the WSL 2 backend selected when prompted, finish the wizard, and start Docker Desktop.

    After Docker Desktop starts, verify Docker from a terminal:

    ```bash
    docker --version
    docker run hello-world
    ```

2. Create a local directory for the SearxNG configuration.

    **EDIT:** If you are using this repository, the `searxng/` directory with the example config file is already included. You can skip this step if that's the case.

    Windows/PowerShell: 

    ```powershell
    New-Item -ItemType Directory -Force -Path searxng
    ```

    MacOS, Linux, Git Bash, or WSL:

    ```bash
    mkdir -p searxng
    ```

3. Copy the SearxNG config from the example file in this repository.

    Windows/PowerShell:

    ```powershell
    Copy-Item searxng/settings.yml.example searxng/settings.yml
    ```

    MacOS, Linux, Git Bash, or WSL:

    ```bash
    cp searxng/settings.yml.example searxng/settings.yml
    ```

    The `searxng/settings.yml.example` file is safe to commit. The copied `searxng/settings.yml` file is for your local machine and is ignored by Git.

4. Generate a local SearxNG secret.

    SearxNG uses `server.secret_key` for cryptographic internals. You do not get this key from SearxNG or from an external service. Generate a random value locally and keep it in your uncommitted `.env` file.

    PowerShell:

    ```powershell
    -join ((48..57 + 65..90 + 97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
    ```

    MacOS, Linux, Git Bash, or WSL:

    ```bash
    openssl rand -hex 32
    ```

    Add the generated value to `.env`:

    ```env
    SEARXNG_SECRET=your_generated_secret_here
    SEARXNG_URL=http://localhost:8080
    ```

    Docker passes this value into the SearxNG container with `--env-file .env`. SearxNG maps `SEARXNG_SECRET` to `server.secret_key`.

5. Review `searxng/settings.yml`.

    SearxNG's JSON output must be enabled before the Python client can call `format=json`.

    ```yaml
    use_default_settings: true

    server:
      bind_address: "0.0.0.0"
      port: 8080

    search:
      formats:
        - html
        - json
    ```

6. Start SearXNG.

    **Note:** You need to run this command in the same directory as the `.env` file so Docker can read the `SEARXNG_SECRET` value.
    
    ```bash
    docker run --name searxng-local \
      -d \
      -p 8080:8080 \
      --env-file .env \
      -v "$(pwd)/searxng:/etc/searxng" \
      searxng/searxng:latest
    ```

    On Windows PowerShell, use:

    ```powershell
    docker run --name searxng-local -d -p 8080:8080 --env-file .env -v "${PWD}/searxng:/etc/searxng" searxng/searxng:latest
    ```

7. Verify SearXNG container is running.

    ```bash
    docker ps

    ## Or you can use:
    ## sudo docker ps
    ```

    Output:

    ```bash
    CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                     NAMES
    f2079af7a7af   searxng/searxng:latest  "/usr/local/searxng/…"   39 seconds ago   Up 38 seconds   0.0.0.0:8080->8080/tcp    searxng-local
    ```

8. Confirm SearxNG is running.

    Open this URL in your browser:

    ```text
    http://localhost:8080
    ```

    <div class='img-center'>

    ![](../../images/Screenshot2026-06-18005310.png)

    </div>

9. Test the JSON API using cURL.

    ```bash
    curl -s "http://localhost:8080/search?q=openai&format=json" | jq
    ```

    Output:

    ```json
    {
      "query": "openai",
      "results": [
        {
          "title": "OpenAI",
          "url": "https://openai.com/",
          "content": "OpenAI is an AI research and deployment company. Our mission is to ensure that artificial general intelligence benefits all of humanity."
        },
        ...
      ]
    }
    ```

10. Other useful Docker commands:

    ```bash
    docker stop searxng-local
    docker start searxng-local
    docker logs searxng-local
    ```


## Create the Project 

Inside the directory, run the following command to create the project:

```bash
## "research-team" is crew name I chose here.
## You can choose any name you like.
crewai create crew research-team
```

Choose the provider to use:

```bash
Select a provider to set up:
1. openai
2. anthropic
3. gemini
4. nvidia_nim
5. groq
6. huggingface
7. ollama
...
```

For this project, I used OpenAI, so I would select option 1.

Next, choose the model:

```bash
Select a model to use for Openai:
1. gpt-4
2. gpt-4.1
3. gpt-4.1-mini-2025-04-14
4. gpt-4.1-nano-2025-04-14
5. gpt-4o
6. gpt-4o-mini
7. o1-mini
8. o1-preview
q. Quit
```

For reference, I've created this ranking of OpenAI models based on their capabilities and cost-effectiveness:

| Model        | Cost     | Quality          | Recommendation             |
| ------------ | -------- | ---------------- | -------------------------- |
| gpt-4.1      | $$$      | Excellent        | Best overall               |
| gpt-4.1-mini | $        | Very good        | **Best value**             |
| gpt-4o       | $$       | Very good        | Good alternative           |
| gpt-4o-mini  | $        | Good             | Cheapest I'd recommend     |
| gpt-4.1-nano | Very low | Limited          | Too weak for research      |
| o1-mini      | $$$      | Strong reasoning | Overkill for most research |
| o1-preview   | $$$$     | Strong reasoning | Expensive, older           |
| gpt-4        | $$$      | Older            | No reason to choose today  |

After selecting the model, CrewAI will prompt you to enter your API key. 

```bash
Enter your OPENAI API key (press Enter to skip):  
```

:::info 

The API key is not stored in the project. It is stored into an `.env` file. This is a security measure to prevent accidental exposure of sensitive information in source control or logs.

:::

Finally, CrewAI will create the project structure and install dependencies.

```bash
research_team
|
├── README.md
├── pyproject.toml
├── tests
│
├── knowledge
│   └── user_preference.txt
│
├── src
│   └── research_team
│       │
│       ├── __init__.py
│       ├── crew.py
│       ├── main.py
│       │
│       ├── config
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       │
│       └── tools
│           ├── __init__.py
│           └── custom_tool.py
```

## Agents

The agents are defined in `src/research_team/config/agents.yaml`.

```bash
research_team
│
├── src
│   └── research_team
│       │
│       ├── config
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       │
│       ├── __init__.py
│       ├── crew.py
│       ├── main.py
```

A crew is is simply a collection of agents. Each agent has a role, goal, and backstory. The agents are defined in YAML to make it easy to change their roles and goals without editing the Python orchestration code.

The `src/research_team` folder contains the files that enable the crew to run:

| File          | Purpose                                                                                                                             |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `agents.yaml` | <ul><li>Defines agent roles, goals, and backstories.</li><li>Lets you update agent behavior without changing Python code.</li></ul> |
| `tasks.yaml`  | <ul><li>Defines the tasks performed by agents.</li><li>Lets you update task behavior without changing Python code.</li></ul>        |
| `crew.py`     | <ul><li>Defines the crew and connects agents.</li><li>Adds custom logic, tools, and agent-specific arguments.</li></ul>             |
| `main.py`     | <ul><li>Entry point for running the crew.</li><li>Adds custom inputs for agents and tasks.</li></ul>                                |

For this project, the crew has two agents:

| Agent               | Purpose                                                                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `researcher`        | <ul><li>Researches the assigned topic.</li><li>Finds and gathers relevant information from available sources.</li></ul> |
| `reporting_analyst` | <ul><li>Analyzes the research findings.</li><li>Expands the results into a detailed Markdown report.</li></ul>          |

As mentioned, the configuration for these agents is defined in `src/research_team/config/agents.yaml`.

```yaml
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    ....
  backstory: >
    ....

reporting_analyst:
  role: >
    {topic} Reporting Analyst
  goal: >
    ....
  backstory: >
    ....
```

If you want to add more agents, you can simply add them here and update the `crew.py` file to include them in the crew.

For example, adding the `research_assistant` and `research_editor` agents would look like this:

```yaml
researcher:
  ....

reporting_analyst:
  ....

research_assistant:
  role: >
    {topic} Research Assistant
  goal: >
    ....
  backstory: >
    ....

research_editor:
  role: >
    {topic} Editor
  goal: >
    ....  
  backstory: >
    ....    
```

The updated `crew.py` file would then include these new agents and their *tasks* in the crew definition.

```python
@CrewBase
class ResearchTeam():
    """ResearchTeam crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    .... 
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            ....
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            ....
        )

    @agent
    def research_task(self) -> Task:
        return Task(
            ....
        )

    @agent
    def reporting_task(self) -> Task:
        return Task(
            ....
        )
```



## Tasks

The tasks are the actions that the agents perform. They are basically the "jobs" that the agents are assigned to do. Each task has a name, description, and a function that defines what the agent should do when executing that task.

The important files for tasks are:

- `tasks.yaml` defines the tasks and their descriptions.
- `crew.py` defines the task functions that implement the logic for each task.

```yaml
research_task:
  description: >
    ....
  expected_output: >
    ....
  agent: researcher

reporting_task:
  description: >
    ....
  expected_output: >
    ....
  agent: reporting_analyst
```

As seen in the previous section, if you want to update the agents or tasks, you will also need to update the tasks in `crew.py`, in addition to updating the `tasks.yaml` file. 

## Outputs 

You can configure the agents and tasks to produce different outputs. 

For example, the `reporting_analyst` agent can be configured to produce a Markdown report, a PDF report, or even a presentation deck.

To do this, you would update the `expected_output` field in the `tasks.yaml` file for the `reporting_task`.

```yaml
reporting_task:
  description: >
    ....
  expected_output: >
    A detailed Markdown report with the research findings.
  agent: reporting_analyst
```

Additionally, you would also need to update the `reporting_task` function in `crew.py` to handle the different output formats.

```python
@task
def reporting_task(self) -> Task:
    return Task(
        config=self.tasks_config['reporting_task'], # type: ignore[index]
        output_file='report.md'
    )
```

## Additional: Sequential Processing 

The crew is designed to process tasks sequentially. This means tasks run one after another based on the order they are defined.

In this workflow, the `research_task` runs first and produces research findings. The `reporting_task` then uses those findings to generate the final Markdown report.

This behavior is configured in the `crew.py` file using `Process.sequential`:

```python
@CrewBase
class ResearchTeam():
    """ResearchTeam crew"""

    ....

    @crew
    def crew(self) -> Crew:
        """Creates the ResearchTeam crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical,
            # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
```

**Note on `@CrewBase` framework:**

When you use this framework, the execution order under `Process.sequential` is determined by the declaration order of the `@task` methods in the Python file.

See [Using Annotations in crew.py](https://docs.crewai.com/v1.14.7/en/learn/using-annotations)

This means that if the tasks are defined in this order:

```python
@CrewBase
class ResearchTeam():
    """ResearchTeam crew"""

    @task
    def research_task(self) -> Task:
        ....

    @task
    def reporting_task(self) -> Task:
        ....
```

Then the `research_task` will always run before the `reporting_task`, regardless of the order they are defined in the `tasks.yaml` file.

If they were defined in the opposite order:


```python
@CrewBase
class ResearchTeam():
    """ResearchTeam crew"""

    @task
    def reporting_task(self) -> Task:
        ....

    @task
    def research_task(self) -> Task:
        ....
```

Then the order will be reversed, and the `reporting_task` will run before the `research_task`.

In this case, the reversed order would not work for this workflow since the reporting task depends on the output of the research task.

## Tools 

CrewAI allows agents to use tools to enhance their capabilities. Tools can be used to perform specific functions, access external data, or integrate with other systems.

This project uses the `crewai[tools]` package, which provides tool support within CrewAI and includes a collection of pre-built tools that can be attached to agents.

:::info

The `crewai[tools]` package is already included in `pyproject.toml` and is installed automatically when you run `uv sync`. You do not need to install it separately.

For more details, please see [CrewAI Tools documentation.](https://docs.crewai.com/v1.14.7/en/tools/overview)

:::

For this workflow, the researcher agent uses a custom tool named `SearxNGSearchTool`.

The tool sends search requests to a local SearXNG container:

```text
GET {SEARXNG_URL}/search?q=...&format=json&categories=general
```

This allows the agent to retrieve live search results without relying on a paid search API or external search service.

**Note:** The reporting analyst does not use the search tool directly. It only receives the researcher's findings as task context and generates the final report from that information.

The custom tool is defined in:

```text
tools/custom_tool.py
```

It is attached to the researcher agent in the `crew.py` file: 

```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config["researcher"],
        tools=[SearxNGSearchTool()],
        verbose=True,
    )
```





## Run the Application

Run the crew from the project directory:

```bash
cd project-llm-engineering-sandbox/crewai-projects/01-research-report-agent/research_team

uv run crewai run
```

**Note:** If you activated the virtual environment created by `uv`, you can run the `crewai` command directly:

```bash
crewai run  
```

<!-- You can also run the Python entry point directly:

```bash
uv run run_crew
``` -->

It will prompt you to enter a research topic and current year:

```bash
Enter the research topic: 
```

After the workflow completes, the final report will be written to:

```text
report.md
```

Note that the report should be treated as a first draft. 

Review the claims, add citations where needed, and refine the structure before publishing or reusing it.

<div class='img-center'>

![](../../images/21062026-crewai-research-agent.gif)

</div>
