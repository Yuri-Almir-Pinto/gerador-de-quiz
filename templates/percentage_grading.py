from .base_grading import BaseGradingTemplate

class PercentageGradingTemplate(BaseGradingTemplate):
    def show_final_results(self):
        super().show_final_results()
        print(f"Porcentagem de acerto: {self.corretas/self.total*100:.2f}%")