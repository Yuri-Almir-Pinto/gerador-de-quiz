import typing
from decorators.time_log import timed_and_logged
from enums.question_feedback import QuestionFeedback
from factories.question_asking_factory import QuestionAskingFactory
from factories.question_grading_factory import QuestionGradingFactory
from models.alternative import Alternative

if typing.TYPE_CHECKING:
    from strategies.question_asking_strategy import QuestionAskingStrategy
    from strategies.question_grading_strategy import QuestionGradingStrategy
    
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
    
    @timed_and_logged("Pergunta", "Tempo levado para a resposta de uma pergunta do exame")
    def ask(self):
        self._results = self._asking_strategy.ask(self)
        
    def grade(self) -> tuple[QuestionFeedback, float]:
        return self._grading_strategy.grade(self._results)







