import pandas as pd
from typing import List
from templates.test_case_templates import TestCase

class ExcelExporter:
    """Handles Excel export:
    1. Takes list of TestCase objects
    2. Creates Excel file
    3. Writes test cases as rows
    """
    def export(self, test_cases: List[TestCase], output_file: str) -> str:
        """
        Export test cases to Excel file
        
        Args:
            test_cases: List of TestCase objects
            output_file: Path to output Excel file
            
        Returns:
            str: Path to the exported file
        """
        # Extract just the descriptions
        data = [{'Test Case': tc.description} for tc in test_cases]
        
        # Create DataFrame with single column
        df = pd.DataFrame(data)
        
        # Export to Excel
        df.to_excel(output_file, index=False, sheet_name='Test Cases')
        
        return output_file 