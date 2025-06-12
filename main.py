import os
from typing import List
from test_case_generator.parser import TestCaseParser
from test_case_generator.exporters.excel_exporter import ExcelExporter
from datetime import datetime
from config import OPENAI_API_KEY

class TestCaseApp:
    """Main application class that:
    1. Initializes parser and exporter
    2. Sets up output directory
    3. Coordinates test case generation and export
    """
    
    def __init__(self):
        self.parser = TestCaseParser(api_key=OPENAI_API_KEY)
        self.excel_exporter = ExcelExporter()
        self.output_dir = os.path.join(os.path.dirname(__file__), "generated_test_cases")
        self.setup_output_directory()
        
    def setup_output_directory(self):
        """Create output directory if it doesn't exist"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_and_export(self, user_story: str) -> str:
        """Generate test cases and export them to Excel"""
        test_cases = self.parser.parse_user_story(user_story)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(
            self.output_dir, 
            f"test_cases_{timestamp}.xlsx"
        )
        
        return self.excel_exporter.export(test_cases, output_file)

def main():
    app = TestCaseApp()
    
    try:
        # For command line testing only
        user_story = "Sample user story for testing"
        output_path = app.generate_and_export(user_story)
        print(f"\nTest cases generated successfully!")
        print(f"Output file: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.exception("Error in test case generation")

if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        logging.exception("Unexpected error in main program") 