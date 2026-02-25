"""ProjectForge - AI-Powered Business Analysis Tool

Main entry point for the ProjectForge application.
"""

import os
from datetime import datetime
from dotenv import load_dotenv

from project_forge.core import run_analysis_workflow
from project_forge.utils.exporters import (
    generate_text_content,
    save_text_output,
    save_html_output,
    save_pdf_output
)

load_dotenv()


def get_user_input():
    """Prompt user for project description and interactive mode preference.
    
    Returns:
        tuple: (project_description, interactive_mode_boolean)
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
    
    print("\nDo you want to enable Iterative Mode to provide feedback between agents? (y/n)")
    interactive_choice = input("> ").strip().lower()
    interactive_mode = interactive_choice in ['y', 'yes']
    
    return user_input, interactive_mode


def main():
    """Main execution function for ProjectForge."""
    # Get user input
    user_input, interactive_mode = get_user_input()
    
    # Get configuration from environment
    model_name = os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Execute workflow with partial failure recovery
    print("\n### ProjectForge: Initiating Full Analysis Workflow ###\n")
    
    result = run_analysis_workflow(
        user_input=user_input,
        llm_model=model_name,
        api_key=api_key,
        interactive_mode=interactive_mode
    )
    
    # Display final result if successful
    if result['success'] and result['raw_result']:
        print("\n\n" + "="*60)
        print("  FINAL PROJECT PLAN")
        print("="*60 + "\n")
        print(result['raw_result'])
    elif result['error']:
        print(f"\nWARNING: WORKFLOW ERROR: {result['error']}")
        print("Attempting to save partial results...\n")
    
    # Generate timestamp for output files
    timestamp = result['timestamp']
    output_file = f"output_{timestamp}.txt"
    html_output_file = f"output_{timestamp}.html"
    pdf_output_file = f"output_{timestamp}.pdf"
    
    # Save outputs (even partial results are valuable)
    try:
        # Extract outputs
        outputs = result['outputs']
        ba_output = outputs['intake']
        architect_output = outputs['architect']
        qa_output = outputs['quality']
        synthesis_output = outputs['synthesis']
        pm_output = outputs['manager']
        
        # Save text output
        save_text_output(output_file, user_input, ba_output, architect_output, 
                        qa_output, synthesis_output, pm_output)
        
        # Save HTML output
        save_html_output(html_output_file, result['html_content'])
        
        # Generate PDF
        pdf_generated = save_pdf_output(pdf_output_file, result['html_content'])
        
        # Print summary
        print(f"\n{'='*60}")
        if result['error']:
            print(f"  WARNING: PARTIAL OUTPUT SAVED")
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
    
    # Print warning if workflow had errors
    if result['error']:
        print("\nWARNING: Workflow did not complete successfully.")
        print("Partial results have been saved to output files.\n")


if __name__ == "__main__":
    main()
