from abc import ABC, abstractmethod
from models.question import Question

class BaseGradingStrategy(ABC):
    def __init__(self, *, limit: int = -1) -> None:
        self.limit = limit

    @abstractmethod
    def __call__(self, questions: list[Question]) -> None:
        pass