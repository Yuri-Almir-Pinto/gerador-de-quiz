from models.question import Question

class BaseGradingTemplate:
    def __init__(self, *, limit: int = -1) -> None:
        self.limit = limit

    def __call__(self, questions: list[Question]) -> None:
        self.total = self.limit + 1 if self.limit < len(questions) else len(questions)
        self.questions = questions[:self.total]
        self.corretas = len([question for question in questions if question.chosen_letter == question.correct_letter])
        self.erradas = self.total - self.corretas
        
        self.begin_grading_hook()
        
        self.show_all_corrections()
        
        self.show_final_results()
        
        self.end_grading_hook()
    
    def show_all_corrections(self):
        for index, question in enumerate(self.questions):
            if index > self.limit and self.limit != -1:
                break
            
            self.before_show_question_hook()
            self.show_correction(question)
            self.after_show_question_hook()
    
    def show_correction(self, question: Question):
        print(f"Questão: {question.title}")
        print(f"Alternativa escolhida: {question.chosen_letter if question.chosen_letter else 'Nenhuma'}")
        print(f"Alternativa correta: {question.correct_letter}")
        print("Acertou" if question.chosen_letter == question.correct_letter else "Errou")
    
    def show_final_results(self):
        print(f"Total de questões: {self.total}")
        print(f"Questões corretas: {self.corretas}")
        print(f"Questões erradas: {self.erradas}")
        
    def before_show_question_hook(self):
        pass
    
    def after_show_question_hook(self):
        input(f"{"-"*5}Pressione enter para continuar...{"-"*5}")
    
    def begin_grading_hook(self):
        pass
    
    def end_grading_hook(self):
        pass