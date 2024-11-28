from dataclasses import dataclass
from models.alternative import Alternative

@dataclass
class Choice:
    alternative: Alternative
    chosen_letter: str
    correct_letter: str
    
    def __post_init__(self) -> None:
        self.chosen_letter = self.chosen_letter.upper()
        self.correct_letter = self.correct_letter.upper()