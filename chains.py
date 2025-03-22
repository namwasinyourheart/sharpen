from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llms import get_llm
from prompts import PARAPHRASE_GRADE_PROMPT_TEMPLATE, WRITING_ASSESSMENT_FORMAT
from schemas import WritingAssessment

def create_writing_assessment_chain(provider="google_genai", model=None):
    """Creates a writing assessment chain using the selected LLM provider and model."""
    llm = get_llm(provider, model)
    prompt = PromptTemplate(
        template=PARAPHRASE_GRADE_PROMPT_TEMPLATE,
        partial_variables={"WRITING_ASSESSMENT_FORMAT": WRITING_ASSESSMENT_FORMAT}
    )
    parser = PydanticOutputParser(pydantic_object=WritingAssessment)
    return prompt | llm | parser

def grammar_check_chain(text: str, provider="google_genai", model=None) -> str:
    """Grammar correction using an LLM."""
    llm = get_llm(provider, model)
    prompt = f"Check and correct grammar in the following text:\n\n{text}"
    return llm.invoke(prompt)

def plagiarism_check_chain(text: str, provider="google_genai", model=None) -> str:
    """Check for plagiarism using an LLM."""
    llm = get_llm(provider, model)
    prompt = f"Analyze the following text for plagiarism and provide feedback:\n\n{text}"
    return llm.invoke(prompt)

def translation_chain(text: str, target_language: str, provider="google_genai", model=None) -> str:
    """Translate text into a specified language."""
    llm = get_llm(provider, model)
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    return llm.invoke(prompt)

def word_count_chain(text: str) -> int:
    """Count the number of words in the text."""
    return len(text.split())

def summarization_chain(text: str, provider="google_genai", model=None) -> str:
    """Summarize the given text."""
    llm = get_llm(provider, model)
    prompt = f"Summarize the following text concisely:\n\n{text}"
    return llm.invoke(prompt)

def paraphrasing_chain(text: str, provider="google_genai", model=None) -> str:
    """Paraphrase the given text."""
    llm = get_llm(provider, model)
    prompt = f"Reword the following text while keeping its original meaning:\n\n{text}"
    return llm.invoke(prompt)
