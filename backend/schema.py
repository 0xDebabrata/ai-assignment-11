from __future__ import annotations
from typing import List
from pydantic import BaseModel, validator


class SelectedSymptoms(BaseModel):
    already_asked_mask: int
    already_selected_symptoms_mask: int
    symptoms: List[str]

    @validator("symptoms")
    def validate_symptoms(cls, symptoms: List[str]):
        if len(symptoms) == 0:
            raise ValueError(
                "alteast one symptom must be selected to proceed further."
            )
        else:
            return symptoms
