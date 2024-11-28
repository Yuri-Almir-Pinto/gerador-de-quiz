from models.question import Question
from .base_grading import BaseGradingTemplate

class FinalGradeOnlyGrading(BaseGradingTemplate):
    def __init__(self, *, limit: int = -1):
        BaseGradingTemplate.__init__(self, pause_after_each_correction=False, limit=limit)
    
    def show_correction(self, question: Question):
        pass
    
    def show_final_results(self):
        print(f"Total de questões: {self.total}")
        print(f"Questões corretas: {self.corretas}")
        print(f"Questões erradas: {self.erradas}")