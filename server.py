from pydantic import BaseModel, Field, validator
# from langchain.pydantic_v2 import BaseModel, Field, validator
from typing import List

from dotenv import load_dotenv
load_dotenv()


class TaskResponse(BaseModel):
    score: float  # We set the type as float but will validate further
    concerns: List[str]

    @validator('score')
    def ensure_score_is_numeric(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Score must be numeric (integer or float).')
        if v < 0 or v > 10:
            raise ValueError('Score must be between 0 and 10.')
        return v

class CohesionAndCoherence(BaseModel):
    score: float
    concerns: List[str]

    @validator('score')
    def ensure_score_is_numeric(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Score must be numeric (integer or float).')
        if v < 0 or v > 10:
            raise ValueError('Score must be between 0 and 10.')
        return v

class Vocabulary(BaseModel):
    score: float
    concerns: List[str]

    @validator('score')
    def ensure_score_is_numeric(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Score must be numeric (integer or float).')
        if v < 0 or v > 10:
            raise ValueError('Score must be between 0 and 10.')
        return v

class Grammar(BaseModel):
    score: float
    concerns: List[str]

    @validator('score')
    def ensure_score_is_numeric(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Score must be numeric (integer or float).')
        if v < 0 or v > 10:
            raise ValueError('Score must be between 0 and 10.')
        return v

class Overall(BaseModel):
    score: float
    main_issue: str

    @validator('score')
    def ensure_score_is_numeric(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Score must be numeric (integer or float).')
        if v < 0 or v > 10:
            raise ValueError('Score must be between 0 and 10.')
        return v

class WritingAssessment(BaseModel):
    task_response: TaskResponse
    cohesion_and_coherence: CohesionAndCoherence
    vocabulary: Vocabulary
    grammar: Grammar
    overall: Overall
    reference_answers: List[str]

    def to_dict(self) -> dict:
        return self.dict()


class Input(BaseModel):
    original_text: str
    your_paraphrase: str

    def to_dict(self) -> dict:
        return self.dict()

from fastapi import FastAPI
app = FastAPI()

from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.output_parsers import PydanticOutputParser



from prompts import PARAPHRASE_GRADE_PROMPT_TEMPLATE, WRITING_ASSESSMENT_FORMAT


parser = PydanticOutputParser(pydantic_object=WritingAssessment)

def get_llm():
    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=1000)
    llm = GoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0, max_tokens=1000)
    return llm


def create_chain():
    llm = get_llm()

    paraphrase_grade_prompt = PromptTemplate(
        template=PARAPHRASE_GRADE_PROMPT_TEMPLATE,
        # input_variables=["original_text"]
        partial_variables={"WRITING_ASSESSMENT_FORMAT": WRITING_ASSESSMENT_FORMAT}
    )

    parser = PydanticOutputParser(pydantic_object=WritingAssessment)

    chain = paraphrase_grade_prompt | llm | parser

    return chain


@app.get("/")
def hello():
    return({"Hello": "World!"})

@app.post("/assess")
async def generate_reponse(input: Input):
    chain = create_chain()
    response = chain.invoke(input.to_dict())

    # print(response)

    return response




# Start server
# uvicorn server:app --host 127.0.0.1 --port 8000 --reload