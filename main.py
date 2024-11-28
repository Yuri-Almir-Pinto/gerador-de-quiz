import json
from models.exam import Exam
from templates.base_grading import BaseGradingTemplate
from templates.percentage_grading import PercentageGradingTemplate
from templates.final_grade_only_grading import FinalGradeOnlyGrading

class App:
    _instance: "App | None" = None
    
    # Singleton pattern
    def __new__(cls, *args, **kwargs) -> "App":
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls, *args, **kwargs)
            
        return cls._instance
        
    def __init__(self) -> None:
        if App._instance is not None:
            return
        
        self.exam: Exam | None = None
        
    def load_file(self, questions_file_name: str) -> bool:
        try:
            with open(questions_file_name, "r", encoding="utf-8") as file:
                self.exam = Exam.from_dict(json.load(file))
                return True
        except FileNotFoundError:
            print("Erro ao tentar carregar arquivo de exame: Arquivo não encontrado")
            return False
        except json.JSONDecodeError:
            print("Erro ao tentar carregar arquivo de exame: Arquivo não é um json válido")
            return False
        except Exception as e:
            print(f"Erro ao tentar carregar arquivo de exame: {e}")
            return False
            
        
    # Facade pattern  
    def take_exam(self, file_name: str, *, limit: int = -1) -> None:
        try:
            if limit < -1:
                print("O limite de questões deve ser maior ou igual a -1")
                return
            
            loaded = self.load_file(file_name)
            
            if not loaded:
                return
            
            if self.exam is None:
                print("Nenhum exame foi carregado")
                return
            
            self.exam.shuffle()
            self.exam.ask(limit)
            self.exam.grade(FinalGradeOnlyGrading(limit=limit))
        except Exception as e:
            print(f"Erro ao tentar realizar o exame: {e}")

if __name__ == "__main__":
    app = App()
    
    print(f"{"-"*5} Iniciando teste... {"-"*5}")
    app.take_exam("data/questions.json", limit=2)
    print(f"{"-"*5} Teste finalizado {"-"*5}")