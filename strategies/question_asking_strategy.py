# 5. Strategy
from abc import ABC, abstractmethod
import typing

from helpers.letter_conversion import letter_to_number, number_to_letter

if typing.TYPE_CHECKING:
    from models.question import Question


class QuestionAskingStrategy(ABC):
    @abstractmethod
    def ask(self, question: "Question") -> dict:
        pass

class SingleChoiceAskingStrategy(QuestionAskingStrategy):
    def ask(self, question: "Question") -> dict:
        print(question.title)
        
        correct_letter: str = ""
        
        for index, alternative in enumerate(question.alternatives):
            print(f"{number_to_letter(index)} - {alternative.description}")
            
            if alternative.correct:
                correct_letter = number_to_letter(index)
        
        escolha = input("Escolha: ")
        
        return { "choice": escolha.upper(), "correct_letter": correct_letter }
    
class MultipleChoiceAskingStrategy(QuestionAskingStrategy):
    def ask(self, question: "Question") -> dict:
        print(question.title)
        
        correct_letters: list[str] = []
        
        for index, alternative in enumerate(question.alternatives):
            print(f"{number_to_letter(index)} - {alternative.description}")
            
            if alternative.correct:
                correct_letters.append(number_to_letter(index))
        
        print("Escolha (Pressione 'Enter' para finalizar):")
        
        escolhas: list[str] = []
        while True:
            escolha = input()
            
            if escolha == "":
                break
            
            if letter_to_number(escolha) >= len(question.alternatives):
                continue
            
            escolhas.append(escolha.upper())
            
        return { "choices": escolhas, "correct_letters": correct_letters }