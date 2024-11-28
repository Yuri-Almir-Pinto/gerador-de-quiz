from dataclasses import dataclass
from models.question import Question
from enum import Enum

@dataclass
class Grader:
    
    @dataclass
    class GraderResult:
        acertos: int
        erros: int
        totais: int = 0
        
        def __post_init__(self):
            self.totais = self.acertos + self.erros
            
    limit: int = -1
    mostrar_texto: bool = True
    mostrar_resultado_final: bool = True
    avisar_nenhuma_questao_encontrada: bool = True
    esperar_por_input: bool = True
    mostrar_titulo_questao: bool = True
    mostrar_escolha_invalida: bool = True
    mostrar_escolhida_e_correta: tuple[bool, bool] | bool = True
    mostrar_acertou_ou_errou: tuple[bool, bool] | bool = True
        
    def __call__(self, questions: list[Question]) -> GraderResult:
        return self._grade(questions)
    
    def _grade(self, questions: list[Question]) -> GraderResult:
        
        self._warn_no_questions_found(questions)
        
        (acertadas, erradas) = self._grade_questions(questions)
            
        self._print_final_result(acertadas, erradas)
        
        return Grader.GraderResult(acertos=acertadas, erros=erradas)
        
    def _grade_questions(self, questions: list[Question]) -> tuple[int, int]:
        acertadas = 0
        erradas = 0
        
        for index, question in enumerate(questions):
            if index > self.limit and self.limit != -1:
                break
            
            if self.mostrar_titulo_questao:
                self._show(f"Questão: {question.title}")
            
            if question.chosen is None:
                if self.mostrar_escolha_invalida:
                    self._show("Escolha inválida")
            
            self._show_correct_or_incorrect(question)
            
            acertadas, erradas = self._get_correct_or_incorrect(question, acertadas, erradas)
                
            self._wait_for_input()
            
        return (acertadas, erradas)
    
    def _get_correct_or_incorrect(self, question: Question, acertadas: int, erradas: int) -> tuple[int, int]:
        acertou = False if question.chosen is None else question.chosen.alternative.correct
        
        opt = self.mostrar_acertou_ou_errou
        
        if acertou:
            if (isinstance(opt, tuple) and opt[0]) or opt:
                self._show("Acertou")
            acertadas += 1
        else:
            if (isinstance(opt, tuple) and opt[1]) or opt:
                self._show("Errou")
            erradas += 1
            
        return (acertadas, erradas)
    
    def _show_correct_or_incorrect(self, question: Question) -> None:
        if question.chosen is None:
            return
        
        opt = self.mostrar_escolhida_e_correta
        
        if (isinstance(opt, tuple) and opt[0]) or opt:
            self._show("Alternativa escolhida: ", question.chosen.chosen_letter)
        if (isinstance(opt, tuple) and opt[1]) or opt:
            self._show("Alternativa correta: ", question.chosen.correct_letter)
    
    def _wait_for_input(self):
        if not self.esperar_por_input:
            print("-"*30)
            return
        
        input(f"{"-"*5} Pressione enter para continuar {"-"*5}")
        
    def _warn_no_questions_found(self, questions: list[Question]) -> None:
        if not self.avisar_nenhuma_questao_encontrada:
            return
    
        if len(questions) == 0:
            self._show("Nenhuma questão foi encontrada no exame.")
        
    def _print_final_result(self, acertadas: int, erradas: int) -> None:
        if not self.mostrar_resultado_final:
            return
        
        self._show("\n")
        self._show(f"Acertadas: {acertadas}")
        self._show(f"Erradas: {erradas}")
        
    def _show(self, *args, **kwargs) -> None:
        if not self.mostrar_texto:
            return
        
        print(*args, **kwargs)