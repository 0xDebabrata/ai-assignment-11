from __future__ import annotations
from typing import List
from pydantic import BaseModel, validator


class SelectedSymptoms(BaseModel):
    already_asked_mask: int

    already_selected_symptoms_mask: int

    symptoms: List[str]
    """
    A list of string, consisting of the keys, corresponding to
    the symptoms selected by the user from the initial questions set.
    
    Notes:

    1. If handling `BigInt` in the frontend is feasible, consider 
    changing this representation to an integer that is the bitwise 
    OR of integers corresponding to the symptoms selected by the user.
    """

    @validator("symptoms")
    def validate_symptoms(cls, symptoms: List[str]):
        if len(symptoms) == 0:
            raise ValueError(
                "alteast one symptom must be selected to proceed further."
            )
        else:
            return symptoms
