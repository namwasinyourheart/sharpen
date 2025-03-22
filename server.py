# server.py
from pydantic import BaseModel, Field, validator
from typing import List
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from prompts import PARAPHRASE_GRADE_PROMPT_TEMPLATE, WRITING_ASSESSMENT_FORMAT

load_dotenv()

class ScoreBase(BaseModel):
    score: float
    concerns: List[str]

    @validator("score")
    def validate_score(cls, v):
        if not isinstance(v, (int, float)) or not (0 <= v <= 10):
            raise ValueError("Score must be a number between 0 and 10.")
        return v

class TaskResponse(ScoreBase): pass
class CohesionAndCoherence(ScoreBase): pass
class Vocabulary(ScoreBase): pass
class Grammar(ScoreBase): pass

class Overall(BaseModel):
    score: float
    main_issue: str

    @validator("score")
    def validate_score(cls, v):
        if not isinstance(v, (int, float)) or not (0 <= v <= 10):
            raise ValueError("Score must be a number between 0 and 10.")
        return v

class WritingAssessment(BaseModel):
    task_response: TaskResponse
    cohesion_and_coherence: CohesionAndCoherence
    vocabulary: Vocabulary
    grammar: Grammar
    overall: Overall
    reference_answers: List[str]

    def to_dict(self):
        return self.dict()

class Input(BaseModel):
    original_text: str
    your_paraphrase: str

    def to_dict(self):
        return self.dict()

app = FastAPI()

def get_llm():
    return GoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0, max_tokens=1000)

def create_chain():
    llm = get_llm()
    prompt = PromptTemplate(template=PARAPHRASE_GRADE_PROMPT_TEMPLATE, partial_variables={"WRITING_ASSESSMENT_FORMAT": WRITING_ASSESSMENT_FORMAT})
    parser = PydanticOutputParser(pydantic_object=WritingAssessment)
    return prompt | llm | parser

@app.get("/")
def hello():
    return {"Hello": "World!"}

@app.post("/assess")
async def generate_response(input: Input):
    chain = create_chain()
    response = chain.invoke(input.to_dict())
    return response
