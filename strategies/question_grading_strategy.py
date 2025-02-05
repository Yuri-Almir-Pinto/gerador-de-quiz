# 5. Strategy
from abc import ABC, abstractmethod

from enums.question_feedback import QuestionFeedback


class QuestionGradingStrategy(ABC):
    @abstractmethod
    def grade(self, result: dict) -> tuple[QuestionFeedback, float]:
        pass
    
class SingleChoiceGradingStrategy(QuestionGradingStrategy):
    def grade(self, result: dict) -> tuple[QuestionFeedback, float]:
        if "choice" not in result or type(result["choice"]) != str:
            raise ValueError("O dicionário passado não contém a chave 'choice' ou o valor associado não é uma string.")
        
        if "correct_letter" not in result or type(result["correct_letter"]) != str:
            raise ValueError("O dicionário passado não contém a chave 'correct_letter' ou o valor associado não é uma string.")
        
        choice, correct_letter = result["choice"], result["correct_letter"]
        
        if correct_letter == choice:
            return QuestionFeedback.CORRECT, 1
        
        return QuestionFeedback.INCORRECT, 0
    
class MultipleChoiceGradingStrategy(QuestionGradingStrategy):
    def grade(self, result: dict) -> tuple[QuestionFeedback, float]:
        if "choices" not in result or type(result["choices"]) != list:
            raise ValueError("O dicionário passado não contém a chave 'choices' ou o valor associado não é uma lista.")
        
        if "correct_letters" not in result or type(result["correct_letters"]) != list:
            raise ValueError("O dicionário passado não contém a chave 'correct_letters' ou o valor associado não é uma lista.")
        
        choices, correct_letters = result["choices"], result["correct_letters"]
        
        points: float = 0
        for correct in correct_letters:
            if correct in choices:
                points += 1 / len(correct_letters)
                
        if points == 1:
            return QuestionFeedback.CORRECT, 1
        if points == 0:
            return QuestionFeedback.INCORRECT, 0
        
        return QuestionFeedback.PARTIAL, points