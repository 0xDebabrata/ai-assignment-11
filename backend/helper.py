import sys
import pickle

from typing import Dict, Any, List

SYMPTOMS_FILE_PATH = "./data/symptoms_map.pkl"
DISEASES_FILE_PATH = "./data/diseases_map.pkl"

def initial_questions_keys():
    keys: List[str] = [
        'chills',
        'malaise',
        'high_fever',
        'fatigue',
        'swelling_joints',
        'skin_rash',
        'constipation',
        'headache',
        'vomiting',
    ]

    return keys

def get_mapping(
    file: str,
    mode: str = "rb",
    error_msg: str = "could not open file",
) -> Dict[Any, Any]:
    try:
        with open(file, mode) as mapping_file:
            mapping = pickle.load(mapping_file)
            return mapping
    except OSError:
        print(error_msg)
        sys.exit(1)

def get_symptoms() -> Dict[str, int]:
    symptoms_mapping: Dict[str, int] = get_mapping(SYMPTOMS_FILE_PATH)
    return symptoms_mapping

def get_diseases() -> Dict[str, int]:
    diseases_mapping: Dict[str, int] = get_mapping(DISEASES_FILE_PATH)
    return diseases_mapping
