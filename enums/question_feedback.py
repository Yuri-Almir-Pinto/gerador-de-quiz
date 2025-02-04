from enum import Enum


class QuestionFeedback(Enum):
    CORRECT = 1
    INCORRECT = 2
    PARTIAL = 3
    
    def __str__(self) -> str:
        match(self):
            case self.CORRECT:
                return "Correto"
            case self.INCORRECT:
                return "Incorreto"
            case self.PARTIAL:
                return "Parcial"
            
        raise Exception("Valor inválido para representação de QuestionFeedback.")