from dataclasses import dataclass, field
from models.alternative import Alternative
from models.choice import Choice
from random import shuffle

def letter_to_number(value: str) -> int:
    if len(value) == 0: return 0x20
    return ord(value.upper()) - 65

def number_to_letter(value: int) -> str:
    return chr(value + 65)

@dataclass
class Question:
    title: str
    alternatives: list[Alternative] = field(default_factory=list)
    chosen: Choice | None = None
    
    def __post_init__(self) -> None:
        self.shuffle()
        
        for alternative in self.alternatives:
            if alternative.correct:
                return
        
        raise ValueError("Nenhuma alternativa correta foi encontrada")
    
    @staticmethod
    def from_dict(data: dict) -> "Question":
        if "title" not in data or "alternatives" not in data:
            raise ValueError("O dicionário passado não contém todos os campos necessários para criar uma questão.")
        
        title = data["title"]
        alternatives = [Alternative.from_dict(alternative) for alternative in data["alternatives"]]
        
        return Question(title=title, alternatives=alternatives)
    
    def pick(self, alternative: str) -> Choice | None:
        if letter_to_number(alternative) > len(self.alternatives):
            return None
        
        correct_letter = self.alternatives.index([alternative for alternative in self.alternatives if alternative.correct][0])
        
        self.chosen = Choice(alternative=self.alternatives[letter_to_number(alternative)], 
                             chosen_letter=alternative, 
                             correct_letter=number_to_letter(correct_letter))
        
        return self.chosen
    
    def shuffle(self) -> None:
        shuffle(self.alternatives)
    
    def ask(self) -> None:
        print(self.title)
        
        for index, alternative in enumerate(self.alternatives):
            print(f"{number_to_letter(index)} - {alternative.description}")
        
        escolha = input("Escolha: ")
        
        self.pick(escolha)