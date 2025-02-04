from abc import ABC, abstractmethod
import types
from enums.question_feedback import QuestionFeedback
from models.alternative import Alternative

def _letter_to_number(letter: str) -> int:
    return ord(letter.upper()) - ord("A")

def _number_to_letter(number: int) -> str:
    return chr(number + 65).upper()
    
class Question:
    def __init__(self, *, title: str, 
                 alternatives: list[Alternative], 
                 asking_strategy: "QuestionAskingStrategy",
                 grading_strategy: "QuestionGradingStrategy") -> None:
        self._title = title
        self._alternatives = alternatives
        self._asking_strategy = asking_strategy
        self._grading_strategy = grading_strategy
        
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def alternatives(self) -> list[Alternative]:
        return self._alternatives
    
    @staticmethod
    def from_dict(data: dict) -> "Question":
        if "title" not in data or type(data["title"]) != str:
            raise ValueError("O dicionário passado não contém a chave 'title' ou o valor associado não é uma string.")
        
        if "alternatives" not in data or type(data["alternatives"]) != list:
            raise ValueError("O dicionário passado não contém a chave 'alternatives' ou o valor associado não é uma lista.")
        
        return Question(title=data["title"], 
                        alternatives=[Alternative.from_dict(alternative) for alternative in data["alternatives"]],
                        asking_strategy=QuestionAskingFactory.create(data),
                        grading_strategy=QuestionGradingFactory.create(data))
        
    def ask(self):
        self._results = self._asking_strategy.ask(self)
        
    def grade(self) -> tuple[QuestionFeedback, float]:
        return self._grading_strategy.grade(self._results)

# 5. Strategy
class QuestionAskingStrategy(ABC):
    @abstractmethod
    def ask(self, question: Question) -> dict:
        pass
    
class SingleChoiceAskingStrategy(QuestionAskingStrategy):
    def ask(self, question: Question) -> dict:
        print(question.title)
        
        correct_letter: str = ""
        
        for index, alternative in enumerate(question.alternatives):
            print(f"{_number_to_letter(index)} - {alternative.description}")
            
            if alternative.correct:
                correct_letter = _number_to_letter(index)
        
        escolha = input("Escolha: ")
        
        return { "choice": escolha.upper(), "correct_letter": correct_letter }
    
class MultipleChoiceAskingStrategy(QuestionAskingStrategy):
    def ask(self, question: Question) -> dict:
        print(question.title)
        
        correct_letters: list[str] = []
        
        for index, alternative in enumerate(question.alternatives):
            print(f"{_number_to_letter(index)} - {alternative.description}")
            
            if alternative.correct:
                correct_letters.append(_number_to_letter(index))
        
        print("Escolha (Pressione 'Enter' para finalizar):")
        
        escolhas: list[str] = []
        while True:
            escolha = input()
            
            if escolha == "":
                break
            
            if _letter_to_number(escolha) >= len(question.alternatives):
                continue
            
            escolhas.append(escolha.upper())
            
        return { "choices": escolhas, "correct_letters": correct_letters }

# 5. Strategy
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

# 3. Factory
class QuestionGradingFactory:
    _registry: dict[str, types.FunctionType] = {}

    @staticmethod
    def register(question_type: str, constructor):
        QuestionGradingFactory._registry[question_type] = constructor

    @staticmethod
    def create(data: dict) -> QuestionGradingStrategy:
        if "type" not in data:
            raise ValueError("O dicionário deve conter um campo 'type' para identificar a questão.")

        if data["type"] not in QuestionGradingFactory._registry:
            raise ValueError(f"Tipo de questão desconhecido: {data['type']}")

        return QuestionGradingFactory._registry[data["type"]]()

QuestionGradingFactory.register("single", SingleChoiceGradingStrategy)
QuestionGradingFactory.register("multiple", MultipleChoiceGradingStrategy)

# 3. Factory
class QuestionAskingFactory:
    _registry: dict[str, types.FunctionType] = {}

    @staticmethod
    def register(question_type: str, constructor):
        QuestionAskingFactory._registry[question_type] = constructor

    @staticmethod
    def create(data: dict) -> QuestionAskingStrategy:
        if "type" not in data:
            raise ValueError("O dicionário deve conter um campo 'type' para identificar a questão.")

        if data["type"] not in QuestionAskingFactory._registry:
            raise ValueError(f"Tipo de questão desconhecido: {data['type']}")

        return QuestionAskingFactory._registry[data["type"]]()

QuestionAskingFactory.register("single", SingleChoiceAskingStrategy)
QuestionAskingFactory.register("multiple", MultipleChoiceAskingStrategy)