from dataclasses import dataclass, field
from random import shuffle
from abc import ABC, abstractmethod

from .alternative import Alternative

def _letter_to_number(value: str) -> int:
    if len(value) == 0: return 0x20
    return ord(value.upper()) - 65

def _number_to_letter(value: int) -> str:
    return chr(value + 65)

class QuestionBase(ABC):
    @property
    @abstractmethod
    def title(self) -> str: pass
    
    # 5. Strategy
    @abstractmethod
    def ask(self) -> tuple[bool, float]: 
        """Faz a pergunta ao usuário, e retorna se a resposta está correta e quantos pontos a questão valeu"""
        pass
    
    # 4. Factory
    @staticmethod
    def from_dict(data: dict) -> "QuestionBase":
        if "title" in data and "alternatives" in data:
            return SingleChoiceQuestion(title=data["title"], alternatives=[Alternative.from_dict(alternative) for alternative in data["alternatives"]])
        
        raise ValueError("O dicionário passado não contém todos os campos necessários para criar uma questão.")
        

class SingleChoiceQuestion(QuestionBase):
    def __init__(self, *, title: str, alternatives: list[Alternative]) -> None:
        self._title = title
        self._alternatives = alternatives
        
        self.shuffle()
    
    def pick(self, alternative: str) -> None:
        if _letter_to_number(alternative) > len(self._alternatives):
            return None
        
        self.chosen_letter = alternative.upper()

    def shuffle(self) -> None:
        shuffle(self._alternatives)

    def ask(self) -> tuple[bool, float]:
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
    def correct(self) -> bool:
        return self.points == 1
    
    @property
    def title(self) -> str:
        return self._title
        
    @property
    def correct_letter(self) -> str:
        for index, alternative in enumerate(self._alternatives):
            if alternative.correct:
                return _number_to_letter(index)
            
        raise ValueError("Nenhuma alternativa correta foi encontrada")