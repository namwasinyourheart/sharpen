from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from chains import (
    grammar_check_chain, plagiarism_check_chain, translation_chain,
    word_count_chain, summarization_chain, paraphrasing_chain
)

app = FastAPI()

# Updated models to include provider and model
class TextInput(BaseModel):
    text: str
    provider: Optional[str] = "google_genai"  # Default provider
    model: Optional[str] = None  # Model selection

class TranslationInput(BaseModel):
    text: str
    target_language: str
    provider: str = "google_genai"
    model: Optional[str] = None


@app.get("/")
def hello():
    return {"message": "Sharpen API is running!"}

@app.post("/grammar-check")
def grammar_check(input: TextInput):
    result = grammar_check_chain(input.text, provider=input.provider, model=input.model)
    return {"corrected_text": result}

@app.post("/plagiarism-check")
def plagiarism_check(input: TextInput):
    result = plagiarism_check_chain(input.text, provider=input.provider, model=input.model)
    return {"plagiarism_result": result}

@app.post("/translate")
def translate(input: TranslationInput):
    result = translation_chain(input.text, input.target_language, provider=input.provider, model=input.model)
    return {"translated_text": result}

@app.post("/word-count")
def word_count(input: TextInput):
    result = word_count_chain(input.text)
    return {"word_count": result}

@app.post("/summarize")
def summarize(input: TextInput):
    result = summarization_chain(input.text, provider=input.provider, model=input.model)
    return {"summary": result}

@app.post("/paraphrase")
def paraphrase(input: TextInput):
    result = paraphrasing_chain(input.text, provider=input.provider, model=input.model)
    return {"paraphrased_text": result}
