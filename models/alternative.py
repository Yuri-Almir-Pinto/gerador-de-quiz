from dataclasses import dataclass

@dataclass
class Alternative:
    description: str
    correct: bool = False
    
    @staticmethod
    def from_dict(data: dict) -> "Alternative":
        if "description" not in data or "correct" not in data:
            raise ValueError("O dicionário passado não contém todos os campos necessários para criar uma alternativa.")
        
        description = data["description"]
        correct = data["correct"]
        
        return Alternative(description=description, correct=correct)