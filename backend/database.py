import sys
import pickle

from typing import Dict, Any, List


class Database:
    __SYMPTOMS_PICKLE_FILE_PATH = "./pickle_files/symptoms_mapping_file.pkl"
    __DISEASES_PICKLE_FILE_PATH = "./pickle_files/diseases_mapping_file.pkl"
    __QUESTION_PICKLE_FILE_PATH = "./pickle_files/question_mapping_file.pkl"

    @staticmethod
    def allowed_origins():
        origins: List[str] = [
            "http://127.0.0.1:5173",
            "http://localhost:5173",
        ]
        return origins

    @staticmethod
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

    @staticmethod
    def __create_mapping(
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

    @classmethod
    def get_symptoms(cls) -> Dict[str, int]:
        symptoms_mapping: Dict[str, int] = Database.__create_mapping(
            cls.__SYMPTOMS_PICKLE_FILE_PATH
        )
        return symptoms_mapping

    @classmethod
    def get_diseases(cls) -> Dict[str, int]:
        diseases_mapping: Dict[str, int] = Database.__create_mapping(
            cls.__DISEASES_PICKLE_FILE_PATH
        )
        return diseases_mapping

    @classmethod
    def get_questions(cls) -> Dict[str, str]:
        questions_mapping: Dict[str, str] = Database.__create_mapping(
            cls.__QUESTION_PICKLE_FILE_PATH
        )
        return questions_mapping
