from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lib import (
    encode_symptoms,
    get_next_questions_set,
)
from helper import (
    get_symptoms,
    get_diseases,
    initial_questions_keys,
)
from schema import SelectedSymptoms
from prolog import find_matching_diseases_prolog

app = FastAPI()

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/initial")
def get_initial_questions():
    """
    Get the initial set of questions presented to the user.
    """

    symptoms_mapping = get_symptoms()
    initial_question_keys = initial_questions_keys()

    initial_mask = 0
    for question in initial_question_keys:
        initial_mask |= 1 << symptoms_mapping[question]

    already_asked_mask: int = initial_mask

    return {
        "already_asked_mask": str(already_asked_mask),
        "selected_mask": str(0),
        "initial_questions": initial_question_keys,
    }


@app.post("/next")
def get_next_questions(request: SelectedSymptoms):
    """
    Get the next set of questions depending on the already-selected symptoms.
    """

    already_asked_mask: int = request.already_asked_mask
    already_selected_symptoms_mask: int = request.already_selected_symptoms_mask

    selected_symptoms: List[str] = request.symptoms

    symptoms_mapping = get_symptoms()
    diseases_mapping = get_diseases()

    symptoms_mask = encode_symptoms(
        symptoms=selected_symptoms,
        symptoms_mapping=symptoms_mapping,
    )

    # this is for testing purposes because for testing,
    # in real world scenario, the user will not be able to select
    # extra diseases than initial questions on the first go
    already_asked_mask |= symptoms_mask

    next_mask, next_questions_key = get_next_questions_set(
        selected_symptoms=selected_symptoms,
        already_asked_mask=already_asked_mask,
        symptoms_mapping=symptoms_mapping,
        diseases_mapping=diseases_mapping,
    )

    already_asked_mask |= next_mask
    already_selected_symptoms_mask |= symptoms_mask

    return {
        "already_asked_mask": str(already_asked_mask),
        "selected_mask": str(already_selected_symptoms_mask),
        "next_questions": next_questions_key,
    }


@app.post("/diseases")
def get_matching_diseases(request: SelectedSymptoms):
    """
    Return matching diseases to the client.
    """

    already_selected_symptoms_mask: int = request.already_selected_symptoms_mask
    selected_symptoms: List[str] = request.symptoms

    symptoms_mapping = get_symptoms()

    symptoms_mask: int = encode_symptoms(
        symptoms=selected_symptoms,
        symptoms_mapping=symptoms_mapping,
    )

    already_selected_symptoms_mask |= symptoms_mask

    matching_diseases: List[str] = find_matching_diseases_prolog(
        already_selected_symptoms_mask, symptoms_mapping
    )

    return {"diseases": matching_diseases}
