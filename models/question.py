from enum import Enum
from random import shuffle
from abc import ABC, abstractmethod

from .alternative import Alternative

def _letter_to_number(value: str) -> int:
    if len(value) == 0: return 0x20
    return ord(value.upper()) - 65

def _number_to_letter(value: int) -> str:
    return chr(value + 65)

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
    

class QuestionBase(ABC):
    def __init__(self, *, title: str, alternatives: list[Alternative]) -> None:
        self._title = title
        self._alternatives = alternatives
        
    @property
    @abstractmethod
    def title(self) -> str: pass
    
    @property
    @abstractmethod
    def points(self) -> float: pass
    
    @property
    @abstractmethod
    def correct(self) -> QuestionFeedback: pass
    
    # 5. Strategy
    @abstractmethod
    def ask(self) -> tuple[QuestionFeedback, float]: 
        """Faz a pergunta ao usuário, e retorna se a resposta está correta e quantos pontos a questão valeu"""
        pass
    
    # 4. Factory
    @staticmethod
    def from_dict(data: dict) -> "QuestionBase":
        if "title" in data and "alternatives" in data:
            # Check if only one is correct
            quantity_correct = sum([1 for alternative in data["alternatives"] if alternative["correct"]])
            
            if quantity_correct == 1:
                return SingleChoiceQuestion(title=data["title"], alternatives=[Alternative.from_dict(alternative) for alternative in data["alternatives"]])
            if quantity_correct > 1:
                return MultipleChoiceQuestion(title=data["title"], alternatives=[Alternative.from_dict(alternative) for alternative in data["alternatives"]])
            
        
        raise ValueError("O dicionário passado não contém todos os campos necessários para criar uma questão.")
        

class SingleChoiceQuestion(QuestionBase):
    def __init__(self, *, title: str, alternatives: list[Alternative]) -> None:
        super().__init__(title=title, alternatives=alternatives)
        
        shuffle(self._alternatives)
    
    def pick(self, alternative: str) -> None:
        if _letter_to_number(alternative) > len(self._alternatives):
            return
        
        self.chosen_letter = alternative.upper()

    def shuffle(self) -> None:
        shuffle(self._alternatives)

    def ask(self) -> tuple[QuestionFeedback, float]:
        print(self.title)
        
        for index, alternative in enumerate(self._alternatives):
            print(f"{_number_to_letter(index)} - {alternative.description}")
        
        escolha = input("Escolha: ")
        
        self.pick(escolha)
        
        return self.correct, self.points
        
    @property
    def points(self) -> float:
        return 1 if self.correct_letter == self.chosen_letter else 0

    @property
    def correct(self) -> QuestionFeedback:
        return QuestionFeedback.CORRECT if self.points == 1 else QuestionFeedback.INCORRECT
    
    @property
    def title(self) -> str:
        return self._title
        
    @property
    def correct_letter(self) -> str:
        for index, alternative in enumerate(self._alternatives):
            if alternative.correct:
                return _number_to_letter(index)
            
        raise ValueError("Nenhuma alternativa correta foi encontrada")
    
class MultipleChoiceQuestion(QuestionBase):
    def __init__(self, *, title: str, alternatives: list[Alternative]) -> None:
        super().__init__(title=title, alternatives=alternatives)
        
        shuffle(self._alternatives)
        
    def ask(self) -> tuple[QuestionFeedback, float]:
        print(self.title)
        
        for index, alternative in enumerate(self._alternatives):
            print(f"{_number_to_letter(index)} - {alternative.description}")
            
        print("Escolha (Pressione 'Enter' para finalizar):")
        
        self.chosen: list[str] = []
        while True:
            escolha = input()
            
            if escolha == "":
                break
            
            if _letter_to_number(escolha) > len(self._alternatives):
                continue
            
            self.chosen.append(escolha.upper())
            
        return self.correct, self.points
            
    @property
    def points(self) -> float:
        points: float = 0
        for correct in self.correct_letters:
            if correct in self.chosen:
                points += 1 / len(self.correct_letters)
                
        return points
    
    @property
    def correct(self) -> QuestionFeedback:
        if self.points == 1:
            return QuestionFeedback.CORRECT
        if self.points == 0: 
            return QuestionFeedback.INCORRECT
        
        return QuestionFeedback.PARTIAL
    
    @property
    def title(self) -> str:
        return self._title
            
    @property
    def correct_letters(self) -> list[str]:
        return [_number_to_letter(index) for index, alternative in enumerate(self._alternatives) if alternative.correct]
        
        