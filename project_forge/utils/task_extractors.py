"""Safe task output extraction utilities."""

from typing import Dict, List, Optional
from crewai import Task


def extract_task_outputs_by_role(tasks: List[Task]) -> Dict[str, str]:
    """Safely extract task outputs by mapping agent role to output content.
    
    This prevents brittle magic-number indexing that breaks when task order changes.
    
    Args:
        tasks: List of completed Task objects from CrewAI workflow
        
    Returns:
        Dict mapping agent role keywords to task output strings:
        {
            'intake': '...',
            'architect': '...',
            'quality': '...',
            'synthesis': '...',
            'manager': '...'
        }
        
    Raises:
        ValueError: If a required role is missing from tasks
    """
    role_mapping = {
        'Requirements Intake Specialist': 'intake',
        'Technical Architect': 'architect',
        'Senior Quality Auditor': 'quality',
        'Technical Synthesizer': 'synthesis',
        'Project Manager': 'manager'
    }
    
    outputs = {}
    
    for task in tasks:
        if not task.agent:
            continue
            
        agent_role = task.agent.role
        
        # Find matching role key
        for full_role, short_key in role_mapping.items():
            if full_role in agent_role:
                output_text = task.output.raw if hasattr(task.output, 'raw') else str(task.output)
                outputs[short_key] = output_text
                break
    
    # Validate all required roles are present
    required_roles = set(role_mapping.values())
    found_roles = set(outputs.keys())
    missing_roles = required_roles - found_roles
    
    if missing_roles:
        raise ValueError(
            f"Missing outputs for roles: {missing_roles}. "
            f"Found only: {found_roles}. "
            f"This may indicate a workflow configuration error."
        )
    
    return outputs


def extract_task_outputs_safe(tasks: List[Task]) -> Dict[str, Optional[str]]:
    """Extract task outputs with graceful degradation (no exceptions).
    
    Use this version when you want partial results even if some tasks failed.
    
    Args:
        tasks: List of Task objects (may include failed/incomplete tasks)
        
    Returns:
        Dict mapping agent role keywords to task outputs (None for missing):
        {
            'intake': '...',
            'architect': None,  # Missing
            'quality': '...',
            'synthesis': '...',
            'manager': None  # Failed
        }
    """
    try:
        return extract_task_outputs_by_role(tasks)
    except ValueError:
        # Fallback: return whatever we can extract
        role_mapping = {
            'Requirements Intake Specialist': 'intake',
            'Technical Architect': 'architect',
            'Senior Quality Auditor': 'quality',
            'Technical Synthesizer': 'synthesis',
            'Project Manager': 'manager'
        }
        
        outputs = {key: None for key in role_mapping.values()}
        
        for task in tasks:
            if not task.agent:
                continue
                
            agent_role = task.agent.role
            
            for full_role, short_key in role_mapping.items():
                if full_role in agent_role:
                    try:
                        output_text = task.output.raw if hasattr(task.output, 'raw') else str(task.output)
                        outputs[short_key] = output_text
                    except Exception:
                        outputs[short_key] = None
                    break
        
        return outputs
