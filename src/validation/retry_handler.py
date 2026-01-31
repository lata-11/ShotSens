from langchain.output_parsers import OutputFixingParser
from services.llm_service import get_llm

def get_safe_parser(base_parser):
    # Automatically retries/fixes malformed JSON
    return OutputFixingParser.from_llm(llm=get_llm(), parser=base_parser)