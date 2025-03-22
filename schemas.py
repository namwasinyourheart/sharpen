from pydantic import BaseModel, Field, validator
from typing import List

class ScoreBase(BaseModel):
    score: float
    concerns: List[str]

    @validator("score")
    def validate_score(cls, v):
        if not isinstance(v, (int, float)) or not (0 <= v <= 10):
            raise ValueError("Score must be between 0 and 10.")
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
            raise ValueError("Score must be between 0 and 10.")
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
