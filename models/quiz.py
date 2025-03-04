from dataclasses import dataclass, field
from random import shuffle

from decorators.time_log import timed_and_logged

from .question import Question

@dataclass
class Quiz:
    questions: list[Question] = field(default_factory=list)
    
    @staticmethod
    def from_dict(data: dict) -> "Quiz":
        questions = [Question.from_dict(question) for question in data]
        
        return Quiz(questions=questions)
    
    def shuffle(self) -> None:
        shuffle(self.questions)
    
    @timed_and_logged("Quiz", "Tempo levado para a finalização do exame")
    def ask(self, *, limit: int = 0) -> None:
        if len(self.questions) == 0:
            print("Nenhuma questão foi encontrada no exame.")
        
        for index, question in enumerate(self.questions):
            if limit != 0 and index >= limit:
                break
            
            question.ask()
        
        print("\n")
        
    def grade(self, *, limit: int = 0) -> None:
        if len(self.questions) == 0:
            print("Nenhuma questão foi encontrada no exame.")
        
        print("-"*10)
        total: float = 0
        for index, question in enumerate(self.questions):
            if limit != 0 and index >= limit:
                break
            
            feedback, points = question.grade()
            
            total += points
                        
            print(f"{question.title}: \n{points:.1f}/1 - {feedback}")
            input("- Pressione Enter para continuar -")
            print("-"*10)
        
        print()
        print(f"Pontuação final: {((total/(len(self.questions) if limit == -1 else limit))*100):.0f}")