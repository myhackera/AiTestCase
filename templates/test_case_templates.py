from dataclasses import dataclass

@dataclass
class TestCase:
    """Data structure for test cases with:
    - ID
    - Description
    - Expected Result
    """
    id: str
    description: str
    expected_result: str = ""

    def to_dict(self) -> dict:
        """Convert test case to dictionary format"""
        return {
            'Test Case': self.description
        }