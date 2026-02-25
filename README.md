# ProjectForge - AI-Powered Business Analysis Tool

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

**ProjectForge** is an enterprise-grade AI business analysis tool that transforms rough project ideas into comprehensive, multi-format business plans using a 5-agent CrewAI workflow.

## What It Does

Takes a simple project description like:
```
"A sample nutrition tracker app with photo-based meal logging"
```

And generates:
- **Business Requirements** (3 prioritized features with justifications)
- **Technical Architecture** (Database schemas, API endpoints, integrations)
- **Risk Assessment** (Security gaps, edge cases, data validation concerns)
- **Technical Synthesis** (1-page executive summary for non-technical stakeholders)
- **Project Roadmap** (Sprint breakdown, success metrics, timelines)

## Output Formats

- **Plain Text** (`.txt`) - Easy to read and share
- **HTML** (`.html`) - Interactive with collapsible sections and styled badges
- **PDF** (`.pdf`) - Professional documents for presentations

## Architecture

### Multi-Agent Workflow

ProjectForge uses a sequential 5-agent pipeline:

```
┌─────────────────┐
│ 1. Intake       │  Identifies 3 core features from user input
│    Specialist   │  
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Technical    │  Creates database schemas, API specs, integrations
│    Architect    │  
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Quality      │  Finds security risks, edge cases, validation gaps
│    Auditor      │  
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Technical    │  Condenses architect + QA outputs into 1-page summary
│    Synthesizer  │  (Prevents context bloat for PM agent)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Project      │  Creates executive summary, sprint plan, success metrics
│    Manager      │  
└─────────────────┘
```

### Project Structure

```
ProjectForge/
├── .env                          # API keys and configuration
├── main.py                       # CLI entry point
├── app.py                        # Streamlit web UI entry point
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── project_forge/                # Main package
│   ├── __init__.py
│   ├── core.py                   # Core workflow engine (shared by CLI & Web)
│   │
│   ├── agents/                   # Agent definitions
│   │   ├── __init__.py
│   │   └── team.py               # 5 agent factory function
│   │
│   ├── tasks/                    # Task definitions
│   │   ├── __init__.py
│   │   └── workflows.py          # 5 task creation with context passing
│   │
│   ├── utils/                    # Utility modules
│   │   ├── __init__.py
│   │   ├── exporters.py          # Markdown→HTML, file saving, PDF generation
│   │   └── task_extractors.py   # Safe output extraction by role (no magic numbers)
│   │
│   └── templates.py              # HTML/CSS template generator
│
└── output_YYYYMMDD_HHMMSS.*     # Generated reports (CLI mode)
```

## Quick Start

### Prerequisites

- **Python 3.11+**
- **macOS** (for PDF generation via WeasyPrint)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tnrss/ProjectForge.git
   cd ProjectForge
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # OR on Windows:
   # .venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install system dependencies (macOS only, for PDF generation)**
   ```bash
   brew install pango gdk-pixbuf libffi
   ```

5. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   GOOGLE_API_KEY=your_gemini_api_key_here
   LLM_MODEL=gemini/gemini-2.5-flash
   ```

### Usage

ProjectForge provides **two interfaces**: a command-line tool for developers and a web UI for teams.

#### Web UI (Recommended for Teams)

Launch the Streamlit web interface:
```bash
streamlit run app.py
```

This opens an interactive browser interface where you can:
- Enter project descriptions in a rich text area
- Configure LLM model and API key in the sidebar
- View agent outputs in expandable sections with real-time results
- Download TXT, HTML, and PDF outputs instantly

**Default URL:** http://localhost:8501

**Features:**
- Clean, professional interface with Font Awesome icons
- Dark mode optimized for readability
- Responsive design with proper overflow handling
- Session state management for persistent results
- Error handling with partial result recovery

**Note:** The web UI runs in automated mode (no human-in-the-loop feedback). For iterative agent feedback, use the CLI with interactive mode.

#### Command-Line Interface (CLI)

For automation, scripting, or local development:

**Interactive Mode:**
```bash
python main.py
```

**Iterative Mode with Human-in-the-Loop:**
```bash
python main.py
> [Enter project description]
> y  # Enable feedback between agents
```

**Pipe Input Mode:**
```bash
echo "Your project description here" | python main.py
```

**Example:**
```bash
python main.py
> A carbon tracking app with car trip logging and Google Login
```

Output files will be saved as:
- `output_20260223_154523.txt`
- `output_20260223_154523.html`
- `output_20260223_154523.pdf`

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | None | Yes |
| `LLM_MODEL` | LLM model identifier | `gemini/gemini-2.5-flash` | No |

### Supported LLM Models

```bash
# Google Gemini (default)
LLM_MODEL=gemini/gemini-2.5-flash

# OpenAI (if you have API key)
LLM_MODEL=openai/gpt-4

# Anthropic Claude
LLM_MODEL=anthropic/claude-3-opus
```

**Note:** Changing models requires updating the API key configuration in CrewAI.

## Enterprise Features

### 1. Partial Failure Recovery

If an API call fails mid-workflow (HTTP 429 rate limit, timeout), ProjectForge saves whatever outputs were completed:

```python
try:
    result = crew.kickoff()
except Exception as e:
    print(f"WARNING: WORKFLOW ERROR: {e}")
    # Still saves Tasks 1-3 even if Task 4 failed
finally:
    save_partial_results()
```

**Output example:**
```
WARNING: PARTIAL OUTPUT SAVED (Workflow failed at: HTTPError)
   Plain text: output_20260223_154523.txt
   HTML: output_20260223_154523.html
```

### 2. Safe Task Extraction (No Magic Numbers)

**Anti-Pattern (Brittle):**
```python
ba_output = tasks[0].output  # Breaks if task order changes
```

**Best Practice (Role-Based):**
```python
from project_forge.utils.task_extractors import extract_task_outputs_safe

outputs = extract_task_outputs_safe(tasks)
ba_output = outputs.get('intake')  # Maps by agent role
architect_output = outputs.get('architect')
```

If a task fails, returns `None` instead of crashing.

### 3. 12-Factor App Configuration

All configuration lives in environment variables, not code:

```python
# Hardcoded (bad)
llm = LLM(model="gemini/gemini-2.5-flash")

# Environment-driven (good)
model_name = os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash")
llm = LLM(model=model_name)
```

**Benefits:**
- Hot-swap models without code changes
- Different configs per environment (dev/staging/prod)
- Secrets managed via CI/CD, not source control

### 4. Context Synthesis Layer

The **Technical Synthesizer** agent (Task 4) prevents context bloat by condensing verbose technical outputs before they reach the Project Manager:

```
Architect Output (5000 tokens) ─┐
                                 ├─→ Synthesizer (1-page summary, 500 tokens) ─→ PM
QA Output (3000 tokens) ────────┘
```

**Result:**
- 85% reduction in PM context size
- Fewer hallucinations from excessive context
- Lower API costs

## Module Reference

### `app.py`
**Purpose:** Streamlit web UI entry point

**Key Features:**
- Session state management for persistent results
- Real-time workflow execution with spinner
- Expandable sections for agent outputs
- Download buttons for all output formats (TXT, HTML, PDF)
- Custom CSS with Font Awesome icons
- Dark mode optimized styling
- Responsive design with overflow protection

**Main Functions:**
- `initialize_session_state()` - Sets up Streamlit session variables
- `run_analysis()` - Executes workflow and stores results
- `display_results()` - Renders agent outputs and download buttons
- `main()` - Application entry point

---

### `main.py`
**Purpose:** CLI orchestration layer and entry point

**Key Functions:**
- `get_user_input()` - CLI prompt for project description + interactive mode toggle
- `main()` - Workflow execution with error handling

**Flow:**
1. Load environment variables
2. Get user input (project description + interactive mode preference)
3. Execute workflow via `run_analysis_workflow()`
4. Extract outputs and save to files
5. Display results in terminal

---

### `project_forge/core.py`
**Purpose:** Shared workflow engine for CLI and Web UI

**Function:**
```python
run_analysis_workflow(
    user_input: str,
    llm_model: str,
    api_key: str,
    interactive_mode: bool = False
) -> dict
```

**Returns:**
```python
{
    'success': bool,
    'outputs': {
        'intake': str,
        'architect': str,
        'quality': str,
        'synthesis': str,
        'manager': str
    },
    'html_content': str,
    'timestamp': str,
    'error': Optional[str],
    'raw_result': Optional[str]
}
```

**Features:**
- Centralizes workflow logic for code reuse
- Handles LLM initialization
- Creates agents and tasks
- Executes CrewAI workflow
- Safe output extraction with partial failure recovery
- HTML content generation

---

### `project_forge/agents/team.py`
**Purpose:** Agent factory for the 5-agent workflow

**Function:**
```python
create_agents(llm) -> tuple[Agent, Agent, Agent, Agent, Agent]
```

**Returns:**
- `intake_specialist` - Business Analyst
- `tech_architect` - Senior Systems Engineer
- `quality_auditor` - Senior QA Lead
- `context_synthesizer` - Staff Engineer (synthesis layer)
- `project_manager` - PM with sprint planning expertise

---

### `project_forge/tasks/workflows.py`
**Purpose:** Task creation with context passing and optional human-in-the-loop

**Function:**
```python
create_tasks(user_input, agents, interactive_mode=False) -> list[Task]
```

**Parameters:**
- `user_input` - Project description
- `agents` - Tuple of 5 agents
- `interactive_mode` - Enable human feedback between agents (CLI only)

**Task Dependencies:**
```
task1 (BA) ──────────┬───→ task4 (PM)
                     │
task2 (Architect) ───┼───→ synthesis_task ───→ task4 (PM)
                     │
task3 (QA) ──────────┘
```

**Expected Outputs:**
- Task 1: 3 features (no tables, markdown bullets)
- Task 2: Database schema (nested bullets), APIs (JSON code blocks)
- Task 3: 3 critical risks with fixes
- Synthesis: 1-page summary (non-technical language)
- Task 4: Executive summary with H2/H3 headers, optional tables

---

### `project_forge/utils/exporters.py`
**Purpose:** Markdown conversion and file I/O

**Functions:**

```python
convert_markdown_to_html(text: str) -> str
```
Uses `markdown` library with `tables` and `fenced_code` extensions.

```python
generate_text_content(timestamp, user_input, ba, arch, qa, synth, pm) -> str
```
Generates text output in memory (returns string for web UI downloads).

```python
generate_pdf_bytes(html_content) -> bytes
```
Converts HTML to PDF bytes using BytesIO (for Streamlit downloads).

```python
save_text_output(file, user_input, ba, arch, qa, synth, pm) -> None
```
Writes plain text with section headers to file.

```python
save_html_output(file, html_content) -> None
```
Writes complete HTML document to file.

```python
save_pdf_output(file, html_content) -> bool
```
Converts HTML → PDF using WeasyPrint. Returns `True` on success.

**Dependencies:**
- `markdown` - Production-grade Markdown parser
- `weasyprint` - HTML to PDF converter (requires Pango/Cairo)
- `io.BytesIO` - In-memory binary streams for web downloads

---

### `project_forge/utils/task_extractors.py`
**Purpose:** Safe task output extraction by agent role

**Functions:**

```python
extract_task_outputs_by_role(tasks: List[Task]) -> Dict[str, str]
```
**Strict mode:** Raises `ValueError` if any role missing.

```python
extract_task_outputs_safe(tasks: List[Task]) -> Dict[str, Optional[str]]
```
**Graceful mode:** Returns `None` for missing roles, never crashes.

**Role Mapping:**
```python
{
    'Requirements Intake Specialist': 'intake',
    'Technical Architect': 'architect',
    'Senior Quality Auditor': 'quality',
    'Technical Synthesizer': 'synthesis',
    'Project Manager': 'manager'
}
```

---

### `project_forge/templates.py`
**Purpose:** HTML/CSS template generation

**Function:**
```python
generate_html_template(
    timestamp, ba_html, architect_html, 
    qa_html, synthesis_html, pm_html
) -> str
```

**Features:**
- Embedded CSS (no external dependencies)
- Collapsible sections with JavaScript
- Color-coded badges per agent role
- Responsive design
- Gradient header
- Table styling with zebra stripes

**Badge Colors:**
- BA (Blue)
- Architect (Green)
- QA (Orange)
- Synthesis (Purple)
- PM (Yellow)

## Testing

### Web UI Testing

```bash
# Launch web interface
streamlit run app.py

# Test in browser
# 1. Navigate to http://localhost:8501
# 2. Enter a project description
# 3. Click "Run Analysis"
# 4. Verify agent outputs display
# 5. Test download buttons (TXT, HTML, PDF)
```

### CLI Testing

```bash
# Test with default input
python main.py
> [Press Enter to use default]

# Test interactive mode
python main.py
> test project
> y  # Enable iterative mode

# Verify outputs exist
ls -lh output_*.{txt,html,pdf}
```

### Error Handling Test

Simulate API failure by disconnecting internet, then run:
```bash
python main.py
> test project
```

Should see:
```
WARNING: WORKFLOW ERROR: ConnectionError: ...
Attempting to save partial results...
WARNING: PARTIAL OUTPUT SAVED
```

## Troubleshooting

### PDF Generation Fails

**Error:**
```
cannot load library 'libpango-1.0-0'
```

**Fix (macOS):**
```bash
brew install pango gdk-pixbuf libffi
```

**Fix (Linux/Ubuntu):**
```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

### API Key Not Found

**Error:**
```
GOOGLE_API_KEY environment variable not set
```

**Fix:**
```bash
# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'crewai'
```

**Fix:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Performance

**Typical Execution Time:**
- Task 1 (BA): ~15-30s
- Task 2 (Architect): ~30-45s
- Task 3 (QA): ~20-35s
- Task 4 (Synthesis): ~10-20s
- Task 5 (PM): ~25-40s

**Total:** ~2-3 minutes for complete analysis

**Token Usage:**
- Without synthesis: ~8,000-12,000 tokens
- With synthesis: ~5,000-7,000 tokens (40% reduction)

**Web UI Notes:**
- Results persist in session state during browser session
- Multiple analyses can be run without restarting server
- Downloads generate on-demand (no file storage)

## Deployment

### Local Development
```bash
# CLI
python main.py

# Web UI
streamlit run app.py
```

### Streamlit Cloud (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add Streamlit web UI"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Visit https://share.streamlit.io
   - Connect your GitHub repository
   - Set main file path: `app.py`
   - Add secrets (Settings → Secrets):
     ```toml
     GOOGLE_API_KEY = "your_api_key_here"
     LLM_MODEL = "gemini/gemini-2.5-flash"
     ```
   - Click "Deploy"

3. **Access your app:**
   - URL: `https://[your-app-name].streamlit.app`

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and run:**
```bash
docker build -t projectforge .
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key projectforge
```

### Cloud Run / AWS / Azure

The Streamlit app is stateless and works with any container platform:
- **Google Cloud Run**: Deploy Docker container
- **AWS ECS/Fargate**: Use Docker image
- **Azure Container Instances**: Deploy with Azure CLI

**Environment Variables Required:**
- `GOOGLE_API_KEY`
- `LLM_MODEL` (optional)

## Security

- API keys stored in `.env` (excluded from git via `.gitignore`)
- No user data stored or transmitted beyond LLM API calls
- Output files saved locally (CLI) or generated in-memory (Web UI)
- HTTPS for all API communications
- Session state isolated per browser session in web UI
- No database or persistent storage required

## Roadmap

- [ ] Support for additional LLM providers (OpenAI, Anthropic)
- [ ] Export to Markdown format
- [ ] Project templates for common use cases
- [ ] Multi-language support
- [ ] Real-time progress tracking in web UI
- [ ] User authentication for team deployments
- [ ] Analysis history and version control

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Development Guidelines:**
- Follow PEP 8 style guide
- Add docstrings to all functions
- Test both CLI and Web UI before submitting
- Update README if adding new features
- Keep commits atomic and well-described

## Acknowledgments

- **CrewAI** - Multi-agent orchestration framework
- **Streamlit** - Web UI framework
- **Google Gemini** - LLM provider
- **WeasyPrint** - PDF generation
- **Font Awesome** - Icon library

- **CrewAI** - Multi-agent orchestration framework
- **Google Gemini** - LLM provider
- **WeasyPrint** - PDF generation
- **Markdown Library** - Robust markdown parsing

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Built using CrewAI and Google Gemini**
