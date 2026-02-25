"""Core workflow execution engine for ProjectForge.

This module provides the reusable workflow function that can be called
from both CLI (main.py) and Web UI (app.py) entry points.
"""

from datetime import datetime
from typing import Dict, Optional, Any
from crewai import Crew, Process, LLM

from project_forge.agents.team import create_agents
from project_forge.tasks.workflows import create_tasks
from project_forge.utils.exporters import convert_markdown_to_html
from project_forge.utils.task_extractors import extract_task_outputs_safe
from project_forge.templates import generate_html_template


def run_analysis_workflow(
    user_input: str,
    llm_model: str,
    api_key: str,
    interactive_mode: bool = False
) -> Dict[str, Any]:
    """
    Execute the full ProjectForge analysis workflow.
    
    Args:
        user_input: Project description from user
        llm_model: LLM model identifier (e.g., 'gemini/gemini-2.5-flash')
        api_key: API key for the LLM provider
        interactive_mode: Enable human-in-the-loop feedback (CLI only)
    
    Returns:
        dict: {
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
            'error': Optional[str],  # Error message if failed
            'raw_result': Any  # Raw CrewAI result object
        }
    """
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Initialize result structure
    result = {
        'success': False,
        'outputs': {
            'intake': None,
            'architect': None,
            'quality': None,
            'synthesis': None,
            'manager': None
        },
        'html_content': '',
        'timestamp': timestamp,
        'error': None,
        'raw_result': None
    }
    
    workflow_error = None
    crew_result = None
    tasks = []  # Initialize tasks to empty list
    
    try:
        # Initialize LLM
        my_llm = LLM(
            model=llm_model,
            api_key=api_key
        )
        
        # Create agents and tasks
        agents = create_agents(my_llm)
        tasks = create_tasks(user_input, agents, interactive_mode)
        
        # Create crew
        aba_crew = Crew(
            agents=list(agents),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute workflow
        crew_result = aba_crew.kickoff()
        result['raw_result'] = crew_result
        
    except Exception as e:
        workflow_error = e
        result['error'] = f"{type(e).__name__}: {str(e)}"
    
    finally:
        # Extract outputs (works even if workflow failed partway)
        outputs = extract_task_outputs_safe(tasks) if tasks else {}
        
        # Update result with extracted outputs
        result['outputs']['intake'] = outputs.get('intake') or "[Task did not complete]"
        result['outputs']['architect'] = outputs.get('architect') or "[Task did not complete]"
        result['outputs']['quality'] = outputs.get('quality') or "[Task did not complete]"
        result['outputs']['synthesis'] = outputs.get('synthesis') or "[Task did not complete]"
        result['outputs']['manager'] = outputs.get('manager') or "[Task did not complete]"
        
        # Generate HTML content
        try:
            ba_html = convert_markdown_to_html(result['outputs']['intake'])
            architect_html = convert_markdown_to_html(result['outputs']['architect'])
            qa_html = convert_markdown_to_html(result['outputs']['quality'])
            synthesis_html = convert_markdown_to_html(result['outputs']['synthesis'])
            pm_html = convert_markdown_to_html(result['outputs']['manager'])
            
            result['html_content'] = generate_html_template(
                timestamp, ba_html, architect_html, qa_html, synthesis_html, pm_html
            )
        except Exception as html_error:
            result['error'] = f"HTML generation failed: {str(html_error)}"
        
        # Determine success
        result['success'] = workflow_error is None
    
    return result
