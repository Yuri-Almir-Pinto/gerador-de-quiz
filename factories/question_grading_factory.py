import types
import typing

from strategies.question_grading_strategy import MultipleChoiceGradingStrategy, SingleChoiceGradingStrategy

if typing.TYPE_CHECKING:
    from strategies.question_grading_strategy import QuestionGradingStrategy

# 3. Factory
class QuestionGradingFactory:
    _registry: dict[str, types.FunctionType] = {}

    @staticmethod
    def register(question_type: str, constructor):
        QuestionGradingFactory._registry[question_type] = constructor

    @staticmethod
    def create(data: dict) -> "QuestionGradingStrategy":
        if "type" not in data:
            raise ValueError("O dicionário deve conter um campo 'type' para identificar a questão.")

        if data["type"] not in QuestionGradingFactory._registry:
            raise ValueError(f"Tipo de questão desconhecido: {data['type']}")

        return QuestionGradingFactory._registry[data["type"]]()

QuestionGradingFactory.register("single", SingleChoiceGradingStrategy)
QuestionGradingFactory.register("multiple", MultipleChoiceGradingStrategy)