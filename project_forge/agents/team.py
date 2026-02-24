"""Agent definitions for ProjectForge."""

from crewai import Agent


def create_agents(llm):
    """Create and return all agents for the ProjectForge workflow.
    
    Args:
        llm: The language model instance to use for all agents
        
    Returns:
        tuple: (intake_specialist, tech_architect, quality_auditor, context_synthesizer, project_manager)
    """
    intake_specialist = Agent(
        role='Requirements Intake Specialist',
        goal='Identify core features from messy notes.',
        backstory="You are a veteran Business Analyst expert at identifying user needs.",
        llm=llm,
        verbose=True
    )
    
    tech_architect = Agent(
        role='Technical Architect',
        goal='Create a high-level technical implementation plan.',
        backstory="You are a Senior Systems Engineer who designs scalable, secure backends.",
        llm=llm,
        verbose=True
    )
    
    quality_auditor = Agent(
        role='Senior Quality Auditor',
        goal='Identify gaps, security risks, and edge cases in the technical plan.',
        backstory="""You are a cynical Senior QA Lead. You look for what could go wrong. 
        You check for data privacy, missing error states, and logic gaps.""",
        llm=llm,
        verbose=True
    )
    
    context_synthesizer = Agent(
        role='Technical Synthesizer',
        goal='Condense complex technical and QA reports into brief, actionable executive bullet points',
        backstory="You are a Staff Engineer who translates technical jargon into business-ready summaries.",
        llm=llm,
        verbose=True
    )
    
    project_manager = Agent(
        role='Project Manager',
        goal='Create executive summary and next steps from the audit.',
        backstory="""You are an experienced PM who synthesizes technical details into 
        actionable roadmaps with clear priorities and timelines.""",
        llm=llm,
        verbose=True
    )
    
    return intake_specialist, tech_architect, quality_auditor, context_synthesizer, project_manager
