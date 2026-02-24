# API Reference - ProjectForge

## Table of Contents
1. [Agents Module](#agents-module)
2. [Tasks Module](#tasks-module)
3. [Utils Module](#utils-module)
4. [Templates Module](#templates-module)

---

## Agents Module

### `project_forge.agents.team`

#### `create_agents(llm: LLM) -> tuple`

Creates and configures the 5-agent team for the ProjectForge workflow.

**Parameters:**
- `llm` (LLM): Configured language model instance from `crewai.LLM`

**Returns:**
- `tuple`: 5-element tuple containing:
  1. `intake_specialist` (Agent) - Requirements Intake Specialist
  2. `tech_architect` (Agent) - Technical Architect  
  3. `quality_auditor` (Agent) - Senior Quality Auditor
  4. `context_synthesizer` (Agent) - Technical Synthesizer
  5. `project_manager` (Agent) - Project Manager

**Agent Details:**

##### 1. Requirements Intake Specialist
```python
Agent(
    role='Requirements Intake Specialist',
    goal='Identify core features from messy notes.',
    backstory="Veteran Business Analyst expert at identifying user needs.",
    llm=llm,
    verbose=True
)
```
**Expertise:** Feature prioritization, stakeholder interviews, business justification

##### 2. Technical Architect
```python
Agent(
    role='Technical Architect',
    goal='Create a high-level technical implementation plan.',
    backstory="Senior Systems Engineer who designs scalable, secure backends.",
    llm=llm,
    verbose=True
)
```
**Expertise:** Database design, API architecture, integration planning

##### 3. Senior Quality Auditor
```python
Agent(
    role='Senior Quality Auditor',
    goal='Identify gaps, security risks, and edge cases.',
    backstory="Cynical Senior QA Lead who looks for what could go wrong.",
    llm=llm,
    verbose=True
)
```
**Expertise:** Security audits, edge case analysis, data validation

##### 4. Technical Synthesizer
```python
Agent(
    role='Technical Synthesizer',
    goal='Condense technical/QA reports into executive bullet points',
    backstory="Staff Engineer who translates technical jargon into business-ready summaries.",
    llm=llm,
    verbose=True
)
```
**Expertise:** Technical writing, executive communication, context reduction

##### 5. Project Manager
```python
Agent(
    role='Project Manager',
    goal='Create executive summary and next steps.',
    backstory="Experienced PM who synthesizes technical details into actionable roadmaps.",
    llm=llm,
    verbose=True
)
```
**Expertise:** Sprint planning, success metrics, stakeholder communication

**Example Usage:**
```python
from crewai import LLM
from project_forge.agents.team import create_agents

llm = LLM(model="gemini/gemini-2.5-flash", api_key="your_key")
agents = create_agents(llm)

intake, architect, qa, synthesizer, pm = agents
```

---

## Tasks Module

### `project_forge.tasks.workflows`

#### `create_tasks(user_input: str, agents: tuple) -> list[Task]`

Creates the 5-task sequential workflow with proper context dependencies.

**Parameters:**
- `user_input` (str): Project description from user
- `agents` (tuple): 5-element tuple from `create_agents()`

**Returns:**
- `list[Task]`: List of 5 Task objects in execution order

**Task Definitions:**

##### Task 1: Business Analysis
```python
Task(
    description=f"Analyze this project idea: '{user_input}'",
    expected_output="A list of 3 priority features with business justifications. "
                   "Use standard Markdown formatting. Do not use tables.",
    agent=intake_specialist
)
```
**Output Format:** Markdown with H3 headers and bullet points  
**Context:** None (first task)

##### Task 2: Technical Design
```python
Task(
    description="Create the technical requirements (Schema, APIs) for the features identified.",
    expected_output="A technical brief with Database Schema, API Endpoints, and Integrations. "
                   "Format database schema using nested markdown bullet points. "
                   "Format API endpoints using bold text and code blocks (```json). "
                   "Do not use markdown tables.",
    agent=tech_architect,
    context=[task1]
)
```
**Output Format:** Markdown with nested bullets and JSON code blocks  
**Context:** Task 1 output (feature list)

##### Task 3: Risk Assessment
```python
Task(
    description="Review the technical brief from the Architect. "
               "Find 3 potential 'Edge Cases' or 'Risks' the Architect missed "
               "(e.g., Privacy, Offline Mode, Data Validation).",
    expected_output="A 'Risk Assessment' report with 3 critical gaps and suggested fixes.",
    agent=quality_auditor,
    context=[task2]
)
```
**Output Format:** Markdown with H3 headers and bullet points  
**Context:** Task 2 output (technical brief)

##### Task 4: Technical Synthesis
```python
Task(
    description="Synthesize the technical architecture and risk assessment "
               "into a concise 1-page executive summary. "
               "Extract only the most critical technical decisions, architecture choices, "
               "and risk mitigation strategies. "
               "Focus on business-relevant information that a PM needs to create a roadmap.",
    expected_output="A strict 1-page summary with: "
                   "(1) Key technical architecture decisions in bullet points, "
                   "(2) Top 3 critical risks with mitigation strategies, "
                   "(3) Integration dependencies. "
                   "Use clear, non-technical language.",
    agent=context_synthesizer,
    context=[task2, task3]
)
```
**Output Format:** 1-page markdown with H2/H3 headers  
**Context:** Task 2 (architecture) + Task 3 (risks)  
**Purpose:** Context reduction layer

##### Task 5: Project Roadmap
```python
Task(
    description="Create an executive summary with: "
               "1. Project overview (1 paragraph) "
               "2. Key features prioritized by effort vs impact "
               "3. Critical risks and mitigation strategies "
               "4. Recommended sprint breakdown (2-week sprints) "
               "5. Success metrics",
    expected_output="Executive summary with sprint plan and success criteria. "
                   "Output the roadmap using standard H2 and H3 markdown headers. "
                   "If comparing features, use a markdown table.",
    agent=project_manager,
    context=[task1, synthesis_task]
)
```
**Output Format:** Markdown with tables for feature comparison  
**Context:** Task 1 (features) + Synthesis task (condensed tech summary)

**Context Flow Diagram:**
```
task1 (BA) ──────────┬──────────→ task5 (PM)
                     │
task2 (Arch) ────┐   │
                 ├───┼──→ synthesis_task ──→ task5 (PM)
task3 (QA) ──────┘   │
```

**Example Usage:**
```python
from project_forge.agents.team import create_agents
from project_forge.tasks.workflows import create_tasks

agents = create_agents(llm)
tasks = create_tasks("Build a carbon tracking app", agents)

# Execute with CrewAI
crew = Crew(agents=list(agents), tasks=tasks, process=Process.sequential)
result = crew.kickoff()
```

---

## Utils Module

### `project_forge.utils.exporters`

#### `convert_markdown_to_html(text: str) -> str`

Converts markdown text to HTML using production-grade parser.

**Parameters:**
- `text` (str): Markdown-formatted string

**Returns:**
- `str`: HTML-formatted string

**Extensions Enabled:**
- `tables` - GitHub-flavored tables
- `fenced_code` - Triple-backtick code blocks with syntax highlighting

**Example:**
```python
from project_forge.utils.exporters import convert_markdown_to_html

markdown_text = """
## Database Schema

- **User**
  - `id` (UUID)
  - `email` (String)
"""

html = convert_markdown_to_html(markdown_text)
# Output: <h2>Database Schema</h2><ul><li><strong>User</strong>...
```

---

#### `save_text_output(...) -> None`

Saves all task outputs to a plain text file with section headers.

**Parameters:**
- `output_file` (str): Path to output .txt file
- `user_input` (str): Original project description
- `ba_output` (str): Business Analyst output
- `architect_output` (str): Technical Architect output
- `qa_output` (str): Quality Auditor output
- `synthesis_output` (str): Technical Synthesizer output
- `pm_output` (str): Project Manager output

**Returns:** None (writes to file)

**File Format:**
```
ProjectForge Analysis
Generated: February 23, 2026 at 11:39 PM
Project: [user input]
================================================================================

## Business Requirements

[ba_output]

## Technical Design

[architect_output]

## Risk Assessment

[qa_output]

## Technical Synthesis

[synthesis_output]

## Executive Summary & Roadmap

[pm_output]
```

**Example:**
```python
save_text_output(
    "output_20260223_233953.txt",
    "Carbon tracking app",
    ba_output="...",
    architect_output="...",
    qa_output="...",
    synthesis_output="...",
    pm_output="..."
)
```

---

#### `save_html_output(html_output_file: str, html_content: str) -> None`

Writes HTML content to file with UTF-8 encoding.

**Parameters:**
- `html_output_file` (str): Path to output .html file
- `html_content` (str): Complete HTML document string

**Returns:** None (writes to file)

**Example:**
```python
html_content = generate_html_template(timestamp, ba_html, ...)
save_html_output("output.html", html_content)
```

---

#### `save_pdf_output(pdf_output_file: str, html_content: str) -> bool`

Converts HTML to PDF using WeasyPrint.

**Parameters:**
- `pdf_output_file` (str): Path to output .pdf file
- `html_content` (str): Complete HTML document string

**Returns:**
- `bool`: `True` if PDF generated successfully, `False` otherwise

**Error Handling:**
- Catches `ImportError` if WeasyPrint not installed
- Catches rendering exceptions (missing fonts, invalid CSS)
- Prints helpful error messages

**Example:**
```python
html_content = generate_html_template(...)
success = save_pdf_output("output.pdf", html_content)

if success:
    print("PDF generated successfully")
else:
    print("PDF generation failed")
```

**System Requirements:**
- macOS: `brew install pango gdk-pixbuf libffi`
- Linux: `apt-get install libpango-1.0-0 libpangoft2-1.0-0`

---

### `project_forge.utils.task_extractors`

#### `extract_task_outputs_by_role(tasks: List[Task]) -> Dict[str, str]`

Safely extracts task outputs by mapping agent roles to output content (strict mode).

**Parameters:**
- `tasks` (List[Task]): List of completed Task objects from CrewAI

**Returns:**
- `Dict[str, str]`: Dictionary mapping role keys to outputs:
  ```python
  {
      'intake': 'Business Analyst output...',
      'architect': 'Technical Architect output...',
      'quality': 'QA Auditor output...',
      'synthesis': 'Synthesizer output...',
      'manager': 'Project Manager output...'
  }
  ```

**Raises:**
- `ValueError`: If any required role is missing from tasks

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

**Example:**
```python
from project_forge.utils.task_extractors import extract_task_outputs_by_role

try:
    outputs = extract_task_outputs_by_role(tasks)
    print(outputs['intake'])  # BA output
except ValueError as e:
    print(f"Missing roles: {e}")
```

---

#### `extract_task_outputs_safe(tasks: List[Task]) -> Dict[str, Optional[str]]`

Extracts task outputs with graceful degradation (never crashes).

**Parameters:**
- `tasks` (List[Task]): List of Task objects (may include failed/incomplete)

**Returns:**
- `Dict[str, Optional[str]]`: Dictionary with `None` for missing roles:
  ```python
  {
      'intake': 'BA output...',
      'architect': None,  # Task failed
      'quality': 'QA output...',
      'synthesis': 'Synthesis output...',
      'manager': None  # Task didn't complete
  }
  ```

**Error Handling:**
- First attempts `extract_task_outputs_by_role()`
- On `ValueError`, returns partial results with `None` for missing
- Catches individual task output exceptions

**Example:**
```python
from project_forge.utils.task_extractors import extract_task_outputs_safe

outputs = extract_task_outputs_safe(tasks)

ba_output = outputs.get('intake') or "[Task did not complete]"
architect_output = outputs.get('architect') or "[Task did not complete]"
```

**Use Case:** Partial failure recovery in production workflows

---

## Templates Module

### `project_forge.templates`

#### `generate_html_template(...) -> str`

Generates complete HTML document with embedded CSS and content sections.

**Parameters:**
- `timestamp` (str): Timestamp string for report header (e.g., "20260223_233953")
- `ba_html` (str): Business Analyst section HTML
- `architect_html` (str): Technical Architect section HTML
- `qa_html` (str): Quality Auditor section HTML
- `synthesis_html` (str): Technical Synthesizer section HTML
- `pm_html` (str): Project Manager section HTML

**Returns:**
- `str`: Complete HTML5 document as string

**Features:**

1. **Responsive Design**
   - Mobile-first CSS
   - Max-width container (1200px)
   - Flexible padding/margins

2. **Collapsible Sections**
   - JavaScript toggle functionality
   - Visual indicators (▼/▶)
   - Smooth animations

3. **Color-Coded Badges**
   - 🔵 BA: `#e3f2fd` / `#1565c0`
   - 🟢 Architect: `#e8f5e9` / `#2e7d32`
   - 🟠 QA: `#fff3e0` / `#e65100`
   - 🟣 Synthesis: `#f3e5f5` / `#6a1b9a`
   - 🟡 PM: `#fff9c4` / `#f57f17`

4. **Typography**
   - System fonts (-apple-system, BlinkMacSystemFont, Segoe UI)
   - 1.6 line-height for readability
   - Hierarchical heading sizes

5. **Table Styling**
   - Zebra striping (alternating row colors)
   - Border collapse
   - Full-width layout

6. **Code Blocks**
   - `#f4f4f4` background
   - Monospace font
   - Padding and rounded corners

**HTML Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProjectForge Analysis - {timestamp}</title>
    <style>/* Embedded CSS */</style>
</head>
<body>
    <div class="container">
        <h1>ProjectForge Analysis</h1>
        <div class="meta">Generated: {formatted_timestamp}</div>
        
        <!-- 5 collapsible sections -->
        <div class="section">
            <div class="section-header" onclick="toggleSection(this)">
                <h2><span class="badge badge-ba">BA</span>Business Requirements</h2>
                <span class="toggle-icon">▼</span>
            </div>
            <div class="section-content">{ba_html}</div>
        </div>
        
        <!-- ... 4 more sections ... -->
    </div>
    
    <script>/* Toggle functionality */</script>
</body>
</html>
```

**Example Usage:**
```python
from project_forge.templates import generate_html_template
from project_forge.utils.exporters import convert_markdown_to_html

# Convert markdown to HTML
ba_html = convert_markdown_to_html(ba_output)
architect_html = convert_markdown_to_html(architect_output)
# ... etc

# Generate complete HTML document
html_doc = generate_html_template(
    timestamp="20260223_233953",
    ba_html=ba_html,
    architect_html=architect_html,
    qa_html=qa_html,
    synthesis_html=synthesis_html,
    pm_html=pm_html
)

# Save to file
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_doc)
```

**JavaScript Toggle Function:**
```javascript
function toggleSection(header) {
    const content = header.nextElementSibling;
    const icon = header.querySelector('.toggle-icon');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        icon.textContent = '▼';
    } else {
        content.style.display = 'none';
        icon.textContent = '▶';
    }
}
```

---

## Type Hints Reference

```python
from typing import Dict, List, Optional, Tuple
from crewai import Agent, Task, LLM

# Agents module
def create_agents(llm: LLM) -> Tuple[Agent, Agent, Agent, Agent, Agent]: ...

# Tasks module
def create_tasks(user_input: str, agents: Tuple[Agent, ...]) -> List[Task]: ...

# Exporters module
def convert_markdown_to_html(text: str) -> str: ...
def save_text_output(
    output_file: str, 
    user_input: str, 
    ba_output: str, 
    architect_output: str, 
    qa_output: str, 
    synthesis_output: str, 
    pm_output: str
) -> None: ...
def save_html_output(html_output_file: str, html_content: str) -> None: ...
def save_pdf_output(pdf_output_file: str, html_content: str) -> bool: ...

# Task extractors module
def extract_task_outputs_by_role(tasks: List[Task]) -> Dict[str, str]: ...
def extract_task_outputs_safe(tasks: List[Task]) -> Dict[str, Optional[str]]: ...

# Templates module
def generate_html_template(
    timestamp: str,
    ba_html: str,
    architect_html: str,
    qa_html: str,
    synthesis_html: str,
    pm_html: str
) -> str: ...
```

---

## Error Handling Patterns

### 1. Partial Failure Recovery
```python
workflow_error = None
try:
    result = crew.kickoff()
except Exception as e:
    workflow_error = e
    print(f"⚠️  WORKFLOW ERROR: {type(e).__name__}: {e}")
finally:
    # Save whatever completed
    outputs = extract_task_outputs_safe(tasks)
    save_text_output(...)
```

### 2. Safe Task Extraction
```python
outputs = extract_task_outputs_safe(tasks)
ba_output = outputs.get('intake') or "[Task did not complete]"
```

### 3. PDF Generation Fallback
```python
pdf_generated = save_pdf_output(pdf_file, html_content)
if not pdf_generated:
    print("⚠️  PDF generation skipped")
```

---

## Performance Considerations

### Token Optimization
- Use synthesis layer to reduce PM context by ~40%
- Strict output format constraints prevent verbose responses
- Context passing only includes relevant prior tasks

### Execution Time
- Sequential execution: ~2-3 minutes total
- Parallel would be faster but loses context benefits
- Most time spent in LLM API calls (network latency)

### Memory Usage
- Minimal: Only stores task outputs in memory
- Largest object: HTML template string (~50-100KB)
- Safe for long-running processes

---

**Last Updated:** February 23, 2026  
**API Version:** 1.0.0
