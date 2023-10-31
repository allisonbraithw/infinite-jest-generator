import os
import openai
from llama_index import ServiceContext
from llama_index.evaluation import RelevancyEvaluator
from llama_index.llms import OpenAI


def evaluate_relevancy(query: str, docs: list, response: str) -> bool:
    openai.organization = os.environ.get("OPENAI_ORG")
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    gpt4 = OpenAI(temperature=0, model="gpt-4")
    service_context_gpt4 = ServiceContext.from_defaults(llm=gpt4)
    evaluator = RelevancyEvaluator(service_context=service_context_gpt4)
    eval_source_result_full = evaluator.evaluate(
        query=query,
        response=response,
        contexts=docs
    )
    print(eval_source_result_full)
    return eval_source_result_full.passing
