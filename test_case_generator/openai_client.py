import openai
from typing import Dict, Any
import os

class OpenAIClient:
    """Manages OpenAI API interactions:
    1. Initializes API connection
    2. Sends prompts
    3. Returns generated responses
    """
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate_test_cases(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate test cases using OpenAI API
        
        Args:
            system_prompt: System context prompt
            user_prompt: User story prompt
            
        Returns:
            str: Generated test cases text
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            raise 