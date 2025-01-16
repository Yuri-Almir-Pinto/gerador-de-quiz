import json
from math import floor
from models.quiz import Quiz

# Padrões de projeto utilizados:
# 1. Singleton (Ter apenas uma instância da classe App)
# 2. Facade (Utilizado para realizar o exame)
# 3. Factory (Para criar as questões)
# 4. Builder (Para instanciar e configurar o App)
# 5. Strategy (Para a forma de perguntar as questões)

# 1. Singleton
class App:
    _instance: "App | None" = None
    
    def __new__(cls, *args, **kwargs) -> "App":
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls, *args, **kwargs)
            
        return cls._instance
        
    def __init__(self) -> None:
        if App._instance is not None:
            return
        
    def _load_file(self, questions_file_name: str) -> bool:
        try:
            with open(questions_file_name, "r", encoding="utf-8") as file:
                self._exam = Quiz.from_dict(json.load(file))
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
    
    # 2. Facade
    def take_exam(self, file_name: str, *, limit: int = 0) -> None:
        try:
            limit = floor(limit)
            
            if limit < 0:
                print("O limite de questões deve ser maior ou igual a 0")
                return
            
            self._load_file(file_name)
            
            self._exam.shuffle()
            self._exam.ask(limit)
            self._exam.grade(limit=limit)
        except Exception as e:
            print(f"Erro ao tentar realizar o exame: {e}")

if __name__ == "__main__":
    app = App()
    
    print(f"{"-"*5} Iniciando teste... {"-"*5}")
    app.take_exam("data/quiz.json", limit=2)
    print(f"{"-"*5} Teste finalizado {"-"*5}")