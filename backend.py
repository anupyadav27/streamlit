import openai  # Add this line to import the OpenAI library
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI API Key
openai_api_key = os.getenv('OPENAI_API_KEY')

def generate_section(prompt_template, user_input, section_name, context):
    """
    Generate a specific section of the document by providing the prompt, context, and user input.
    """
    aws_llm = ChatOpenAI(temperature=0.5, model_name="gpt-4", openai_api_key=openai.api_key)
    
    # Modify the template to focus on a single section and include the context
    section_prompt = f"Using the context: '{context}', generate the section '{section_name}' of the cloud architecture document. \n\n{prompt_template}"
    
    aws_chain = LLMChain(llm=aws_llm, prompt=PromptTemplate(input_variables=["user_input"], template=section_prompt))
    try:
        return aws_chain.run(user_input=user_input)
    except Exception as e:
        logging.error(f"Error generating {section_name}: {e}")
        return None


def process_text_and_user_input(user_responses, context):
    """
    Process user inputs and generate a cloud architecture document in chunks, using the context for each section.
    """
    # Convert user responses dictionary to a formatted string
    formatted_user_input = "\n".join([f"**{q}**\n{a}" for q, a in user_responses.items()])
    logging.info(f"User Input: {formatted_user_input}")

    # Path to the prompt template
    prompt_file_path = 'prompt_file.txt'
    
    # Read the prompt template
    try:
        with open(prompt_file_path, 'r') as file:
            prompt_template = file.read()
    except Exception as e:
        logging.error(f"Error reading file {prompt_file_path}: {e}")
        return "Error loading the prompt file."
    
    # Define the sections of the document
    sections = [
        "Solution Summary",
        "Core Functions",
        "Assumptions, Constraints, and Recommendations",
        "Solution Requirements",
        "Proposed Solution",
        "Environment Considerations",
        "Governance & Compliance",
        "Implementation Plan",
        "Conclusion"
    ]
    
    # Generate the document in chunks, using the context for each section
    full_document = ""
    for section in sections:
        logging.info(f"Generating section: {section}")
        section_content = generate_section(prompt_template, formatted_user_input, section, context)
        if section_content:
            full_document += f"\n\n## {section}\n{section_content}"
        else:
            logging.error(f"Error generating section: {section}")
    
    return full_document
