# utils/llm_utils.py
from litellm import completion
from .prompt_template import SYSTEM_PROMPT

def generate_prompt(task_or_prompt: str) -> str:
    """
    Generate an improved prompt using the LLM.
    
    Args:
        task_or_prompt (str): Input task description or existing prompt
        
    Returns:
        str: Generated improved prompt
    """
    response = completion(
        model="anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Task, Goal, or Current Prompt:\n{task_or_prompt}",
            },
        ]
    )
    return response.choices[0].message.content
