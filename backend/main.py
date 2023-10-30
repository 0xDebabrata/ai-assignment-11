from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils import (
    encrypt_symptoms,
    find_matching_diseases,
    get_next_questions_set,
)
from database import Database
from schema import SelectedSymptoms
from prolog_utils import find_matching_diseases_prolog

app = FastAPI()

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=Database.allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/initial-questions")
def get_initial_questions():
    symptoms_mapping = Database.get_symptoms()
    questions_mapping = Database.get_questions()
    initial_questions_keys = Database.initial_questions_keys()

    initial_mask = 0
    for question in initial_questions_keys:
        initial_mask |= 1 << symptoms_mapping[question]

    already_asked_mask: int = initial_mask

    return {
        "already_asked_mask": str(already_asked_mask),
        "selected_mask": str(0),
        "initial_questions": initial_questions_keys,
    }


@app.post("/next-questions")
def get_next_questions(request: SelectedSymptoms):
    already_asked_mask: int = request.already_asked_mask
    already_selected_symptoms_mask: int = request.already_selected_symptoms_mask

    selected_symptoms: List[str] = request.symptoms

    symptoms_mapping = Database.get_symptoms()
    diseases_mapping = Database.get_diseases()
    questions_mapping = Database.get_questions()

    symptoms_mask = encrypt_symptoms(
        symptoms_list=selected_symptoms,
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


@app.post("/matching-diseases")
def get_matching_diseases(request: SelectedSymptoms):
    already_selected_symptoms_mask: int = request.already_selected_symptoms_mask
    selected_symptoms: List[str] = request.symptoms

    symptoms_mapping = Database.get_symptoms()
    diseases_mapping = Database.get_diseases()

    symptoms_mask: int = encrypt_symptoms(
        symptoms_list=selected_symptoms,
        symptoms_mapping=symptoms_mapping,
    )

    already_selected_symptoms_mask |= symptoms_mask

    matching_diseases: List[str] = find_matching_diseases_prolog(
        already_selected_symptoms_mask, symptoms_mapping
    )

    return {"diseases": matching_diseases}
