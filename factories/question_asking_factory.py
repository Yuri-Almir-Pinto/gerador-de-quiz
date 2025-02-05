import types
import typing

from strategies.question_asking_strategy import MultipleChoiceAskingStrategy, SingleChoiceAskingStrategy

if typing.TYPE_CHECKING:
    from strategies.question_asking_strategy import QuestionAskingStrategy

# 3. Factory
class QuestionAskingFactory:
    _registry: dict[str, types.FunctionType] = {}

    @staticmethod
    def register(question_type: str, constructor):
        QuestionAskingFactory._registry[question_type] = constructor

    @staticmethod
    def create(data: dict) -> "QuestionAskingStrategy":
        if "type" not in data:
            raise ValueError("O dicionário deve conter um campo 'type' para identificar a questão.")

        if data["type"] not in QuestionAskingFactory._registry:
            raise ValueError(f"Tipo de questão desconhecido: {data['type']}")

        return QuestionAskingFactory._registry[data["type"]]()

QuestionAskingFactory.register("single", SingleChoiceAskingStrategy)
QuestionAskingFactory.register("multiple", MultipleChoiceAskingStrategy)