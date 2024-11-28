from dataclasses import dataclass, field
from random import shuffle
from models.question import Question
from templates.base_grading import BaseGradingTemplate

@dataclass
class Exam:
    questions: list[Question] = field(default_factory=list)
    
    @staticmethod
    def from_dict(data: dict) -> "Exam":
        questions = [Question.from_dict(question) for question in data]
        
        return Exam(questions=questions)
    
    def shuffle(self) -> None:
        shuffle(self.questions)
        
    def ask(self, limit: int = -1) -> None:
        if len(self.questions) == 0:
            print("Nenhuma questão foi encontrada no exame.")
        
        for index, question in enumerate(self.questions):
            if index > limit and limit != -1:
                break
            
            question.ask()
        
        print("\n")
        
    def grade(self, grading_template: BaseGradingTemplate) -> None:
        grading_template(self.questions)