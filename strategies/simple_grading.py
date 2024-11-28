
from models.question import Question
from strategies.base_grading import BaseGradingStrategy
from templates.grader import Grader


class SimpleGradingStrategy(BaseGradingStrategy):
    
    def __call__(self, questions: list[Question]) -> None:
        grader = Grader(limit=self.limit)
        
        grader(questions)
        
        