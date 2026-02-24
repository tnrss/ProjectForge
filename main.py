"""ProjectForge - AI-Powered Business Analysis Tool

Main entry point for the ProjectForge application.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew, Process, LLM

from project_forge.agents.team import create_agents
from project_forge.tasks.workflows import create_tasks
from project_forge.utils.exporters import (
    convert_markdown_to_html,
    save_text_output,
    save_html_output,
    save_pdf_output
)
from project_forge.utils.task_extractors import extract_task_outputs_safe
from project_forge.templates import generate_html_template

load_dotenv()


def get_user_input():
    """Prompt user for project description.
    
    Returns:
        str: Project description from user input
    """
    print("\n" + "="*60)
    print("   PROJECTFORGE - AI Business Analyst")
    print("="*60 + "\n")
    
    print("Describe your project idea:")
    print("(You can include features, constraints, or just a general concept)\n")
    
    user_input = input("> ").strip()
    
    if not user_input:
        user_input = "We need a carbon tracking app with car trip logging and Google Login."
        print(f"Using default: {user_input}")
    
    return user_input


def main():
    """Main execution function for ProjectForge."""
    # Get user input
    user_input = get_user_input()
    
    # Generate timestamp for output files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"output_{timestamp}.txt"
    html_output_file = f"output_{timestamp}.html"
    pdf_output_file = f"output_{timestamp}.pdf"
    
    # Initialize LLM (12-Factor App: config from environment)
    model_name = os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash")
    my_llm = LLM(
        model=model_name,
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create agents and tasks
    agents = create_agents(my_llm)
    tasks = create_tasks(user_input, agents)
    
    # Create crew
    aba_crew = Crew(
        agents=list(agents),
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # Execute workflow with partial failure recovery
    print("\n### ProjectForge: Initiating Full Analysis Workflow ###\n")
    
    workflow_error = None
    result = None
    
    try:
        result = aba_crew.kickoff()
        
        print("\n\n" + "="*60)
        print("  FINAL PROJECT PLAN")
        print("="*60 + "\n")
        print(result)
        
    except Exception as e:
        workflow_error = e
        print(f"\nWARNING: WORKFLOW ERROR: {type(e).__name__}: {e}")
        print("Attempting to save partial results...\n")
    
    finally:
        # Safe extraction: works even if workflow failed partway through
        outputs = extract_task_outputs_safe(tasks)
        
        ba_output = outputs.get('intake') or "[Task did not complete]"
        architect_output = outputs.get('architect') or "[Task did not complete]"
        qa_output = outputs.get('quality') or "[Task did not complete]"
        synthesis_output = outputs.get('synthesis') or "[Task did not complete]"
        pm_output = outputs.get('manager') or "[Task did not complete]"
        
        # Save text output (even partial results are valuable)
        try:
            save_text_output(output_file, user_input, ba_output, architect_output, qa_output, synthesis_output, pm_output)
            
            # Convert to HTML
            ba_html = convert_markdown_to_html(ba_output)
            architect_html = convert_markdown_to_html(architect_output)
            qa_html = convert_markdown_to_html(qa_output)
            synthesis_html = convert_markdown_to_html(synthesis_output)
            pm_html = convert_markdown_to_html(pm_output)
            
            # Generate HTML content
            html_content = generate_html_template(timestamp, ba_html, architect_html, qa_html, synthesis_html, pm_html)
            
            # Save HTML output
            save_html_output(html_output_file, html_content)
            
            # Generate PDF
            pdf_generated = save_pdf_output(pdf_output_file, html_content)
            
            # Print summary
            print(f"\n{'='*60}")
            if workflow_error:
                print(f"  WARNING: PARTIAL OUTPUT SAVED (Workflow failed at: {type(workflow_error).__name__})")
            else:
                print(f"  OUTPUT SAVED")
            print("="*60)
            print(f"   Plain text: {output_file}")
            print(f"   HTML: {html_output_file}")
            if pdf_generated:
                print(f"   PDF: {pdf_output_file}")
            print("="*60 + "\n")
            
        except Exception as save_error:
            print(f"\nCRITICAL: Failed to save outputs: {save_error}")
            raise
        
        # Re-raise workflow error after saving partial results
        if workflow_error:
            print("\nWARNING: Workflow did not complete successfully.")
            print("Partial results have been saved to output files.\n")


if __name__ == "__main__":
    main()
