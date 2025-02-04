import json
from math import floor
from models.quiz import Quiz

# Padrões de projeto utilizados:
# 1. Singleton (Ter apenas uma instância da classe App)
# 2. Decorator (Para criar um log de tempo de execução)
# 3. Factory (Para criar as questões)
# 4. Builder (Para instanciar e configurar o App)
# 5. Strategy (Para a forma de perguntar as questões)

class AppBuilder:
    def __init__(self) -> None:
        self._limit: int = 0
        self._shuffle: bool = True
        self._questions_file_name: str = "questions.json"
        
        
    def set_limit(self, limit: int) -> "AppBuilder":
        self._limit = limit
        return self
    
    def set_file(self, questions_file_name: str) -> "AppBuilder":
        self._questions_file_name = questions_file_name
        return self
    
    def set_shuffle(self, shuffle: bool) -> "AppBuilder":
        self._shuffle = shuffle
        return self
    
    def build(self) -> "App":
        return App(questions_file_name=self._questions_file_name, 
                   shuffle=self._shuffle, 
                   limit=self._limit)
        

# 1. Singleton
class App:
    _instance: "App | None" = None
    
    def __new__(cls, *args, **kwargs) -> "App":
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls)
            
        return cls._instance
        
    def __init__(self, questions_file_name: str, shuffle: bool, limit: int) -> None:
        if App._instance is None:
            return
        
        self._questions_file_name = questions_file_name
        self._shuffle = shuffle
        self._limit = limit
        
    def _load_file(self) -> bool:
        try:
            with open(self._questions_file_name, "r", encoding="utf-8") as file:
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

    def take_exam(self) -> None:
        try:
            limit = floor(self._limit)
            
            if limit < 0:
                raise Exception("O limite de questões deve ser maior ou igual a 0")
            
            self._load_file()
            
            if self._shuffle:
                self._exam.shuffle()
            self._exam.ask(limit=limit)
            self._exam.grade(limit=limit)
        except Exception as e:
            print(f"Erro ao tentar realizar o exame: {e}")

if __name__ == "__main__":
    app = AppBuilder()\
            .set_file("data/questions.json")\
            .set_limit(5)\
            .set_shuffle(True)\
            .build()
    
    print(f"{"-"*5} Iniciando teste... {"-"*5}")
    app.take_exam()
    print(f"{"-"*5} Teste finalizado {"-"*5}")