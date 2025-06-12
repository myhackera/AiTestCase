from typing import List
import re
from templates.test_case_templates import TestCase

class TestCaseParser:
    """Handles test case generation:
    1. Takes user story and prompt
    2. Calls OpenAI API
    3. Parses response into TestCase objects
    """
    def __init__(self, api_key: str):
        from .openai_client import OpenAIClient
        self.openai_client = OpenAIClient(api_key)
        # Default prompts
        self.system_prompt = "You are an experienced QA expert."
        self.test_case_prompt = """
Write one liner test cases based on the following user story. Write each test case in a separate line.
Use format:
1. 
2. 
3. ...
If table is present, write cases around table and its values.

{user_story}
"""

    def parse_user_story(self, user_story: str) -> List[TestCase]:
        """Generate test cases using GPT API based on user story"""
        try:
            # Create prompt and get response from OpenAI
            formatted_prompt = self.test_case_prompt.format(user_story=user_story)
            response_text = self.openai_client.generate_test_cases(
                self.system_prompt, 
                formatted_prompt
            )
            
            # Parse response into test cases
            test_cases = self._parse_gpt_response(response_text)
            print(f"\nGenerated {len(test_cases)} test cases")
            return test_cases
            
        except Exception as e:
            print(f"Error generating test cases: {str(e)}")
            return [TestCase(
                id="TC001", 
                description="Basic functionality test",
                expected_result="Operation completes successfully"
            )]

    def _parse_gpt_response(self, response: str) -> List[TestCase]:
        """Parse GPT response into TestCase objects"""
        test_cases = []
        lines = response.strip().split('\n')
        
        for idx, line in enumerate(lines, 1):
            if not line.strip():
                continue
                
            # Remove leading number and dot if present
            line = re.sub(r'^\d+\.\s*', '', line.strip())
            
            if line:
                test_case = TestCase(
                    id=f"TC_{str(idx).zfill(3)}", 
                    description=line,
                    expected_result="Test completes successfully"
                )
                test_cases.append(test_case)
        
        return test_cases

    def _validate_test_coverage(self, test_cases: List[TestCase]) -> List[TestCase]:
        """Validate test case coverage"""
        required_keywords = [
            'validation', 'error', 'boundary', 'integration',
            'security', 'performance', 'recovery', 'negative'
        ]
        
        coverage = {keyword: False for keyword in required_keywords}
        
        # Check coverage
        for test_case in test_cases:
            for keyword in required_keywords:
                if keyword in test_case.description.lower():
                    coverage[keyword] = True
        
        # Generate missing scenarios
        missing = [k for k, v in coverage.items() if not v]
        if missing:
            print(f"Warning: Missing test scenarios for: {', '.join(missing)}")
            # Could add logic to generate additional test cases
        
        return test_cases