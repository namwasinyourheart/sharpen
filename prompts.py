PARAPHRASE_GRADE_PROMPT_TEMPLATE = """
You are an expert in scoring IELTS exams. Your task is to evaluate the quality of the user's paraphrase of the original text. Score the paraphrase on a scale from 0 to 9, suggest corrections if necessary, and provide reference phrases. 
Note:
- Maintain the format of the original text
- Your output should follow this structure:
- Score ranging from 0-9, similar to IELTS grading
- Include at least 3 reference phrases in addition to the original text
- If user's paraphrase is EMPTY, fill empty string for all criteria

{WRITING_ASSESSMENT_FORMAT}
original text: {original_text}
user's paraphrase: {your_paraphrase}

"""

WRITING_ASSESSMENT_FORMAT = """
{
  "task_response": {
    "score": "PLACEHOLDER_SCORE",
    "concerns": [
      "PLACEHOLDER_CONCERN_1",
      "PLACEHOLDER_CONCERN_2"
    ]
  },
  "cohesion_and_coherence": {
    "score": "PLACEHOLDER_SCORE",
    "concerns": [
      "PLACEHOLDER_CONCERN_3",
      "PLACEHOLDER_CONCERN_4"
    ]
  },
  "vocabulary": {
    "score": "PLACEHOLDER_SCORE",
    "concerns": [
      "PLACEHOLDER_VOCAB_CONCERN"
    ]
  },
  "grammar": {
    "score": "PLACEHOLDER_SCORE",
    "concerns": [
      "PLACEHOLDER_GRAMMAR_CONCERN"
    ]
  },
  "overall": {
    "score": "PLACEHOLDER_SCORE",
    "main_issue": "PLACEHOLDER_MAIN_ISSUE"
  },
  "reference_answers": [
    "PLACEHOLDER_REFERENCE_ANSWERS
  ]
}

"""

REFERENCE_ANSWER = """
"""