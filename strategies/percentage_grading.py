
from models.question import Question
from strategies.base_grading import BaseGradingStrategy
from templates.grader import Grader

class PercentageGradingStrategy(BaseGradingStrategy):
    
    def __call__(self, questions: list[Question]) -> None:
        grader = Grader(limit=self.limit, mostrar_resultado_final=False)
        
        grade_results = grader(questions)
        
        percentage_unit = 100 / grade_results.totais
        percentage_total = grade_results.acertos * percentage_unit
        
        print(f"Porcentagem de acertos: {percentage_total:.2f}%")
        