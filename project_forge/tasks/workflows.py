"""Agent workflow task definitions for ProjectForge."""

from crewai import Task


def create_tasks(user_input, agents):
    """Create and return all tasks for the ProjectForge workflow.
    
    Args:
        user_input: The project description from the user
        agents: Tuple of (intake_specialist, tech_architect, quality_auditor, context_synthesizer, project_manager)
        
    Returns:
        list: List of Task objects in execution order
    """
    intake_specialist, tech_architect, quality_auditor, context_synthesizer, project_manager = agents
    
    task1 = Task(
        description=f"Analyze this project idea: '{user_input}'",
        expected_output="A list of 3 priority features with business justifications. Use standard Markdown formatting. Do not use tables.",
        agent=intake_specialist
    )
    
    task2 = Task(
        description="Create the technical requirements (Schema, APIs) for the features identified.",
        expected_output="A technical brief with Database Schema, API Endpoints, and Integrations. Format the database schema using nested markdown bullet points. Format API endpoints using bold text and code blocks (```json) for payloads. Do not use markdown tables.",
        agent=tech_architect,
        context=[task1]
    )
    
    task3 = Task(
        description="""Review the technical brief from the Architect. 
        Find 3 potential 'Edge Cases' or 'Risks' the Architect missed (e.g., Privacy, Offline Mode, Data Validation).""",
        expected_output="A 'Risk Assessment' report with 3 critical gaps and suggested fixes.",
        agent=quality_auditor,
        context=[task2]
    )
    
    synthesis_task = Task(
        description="""Synthesize the technical architecture and risk assessment into a concise 1-page executive summary.
        Extract only the most critical technical decisions, architecture choices, and risk mitigation strategies.
        Focus on business-relevant information that a PM needs to create a roadmap.""",
        expected_output="A strict 1-page summary with: (1) Key technical architecture decisions in bullet points, (2) Top 3 critical risks with mitigation strategies, (3) Integration dependencies. Use clear, non-technical language.",
        agent=context_synthesizer,
        context=[task2, task3]
    )
    
    task4 = Task(
        description="""Create an executive summary with:
        1. Project overview (1 paragraph)
        2. Key features prioritized by effort vs impact
        3. Critical risks and mitigation strategies
        4. Recommended sprint breakdown (2-week sprints)
        5. Success metrics""",
        expected_output="Executive summary with sprint plan and success criteria. Output the roadmap using standard H2 and H3 markdown headers. If comparing features, use a markdown table.",
        agent=project_manager,
        context=[task1, synthesis_task]
    )
    
    return [task1, task2, task3, synthesis_task, task4]
