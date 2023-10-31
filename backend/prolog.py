import subprocess
from subprocess import CalledProcessError
from typing import Dict, List, Optional

from lib import decrypt_symptoms


def find_matching_diseases_prolog(
    symptoms: int | List[str],
    symptoms_mapping: Optional[Dict[str, int]] = None,
) -> List[str]:
    symptoms_list: List[str]
    matching_diseases: list[str] = []

    if isinstance(symptoms, List):
        symptoms_list = symptoms
    elif isinstance(symptoms, int) and symptoms_mapping is not None:
        symptoms_list = decrypt_symptoms(symptoms, symptoms_mapping)
    else:
        raise ValueError(
            "symptoms must be either int or List[str].\nIn case of int, symptoms_mapping must be provided."
        )

    symptoms_string = ", ".join([f"{symptom}(X)" for symptom in symptoms_list])

    with open("./data/query.pl", "w") as query_file:
        print(
            f"?- findall(X, ({symptoms_string}), List), print(List), nl.\n?- halt.",
            file=query_file,
        )

    check_cmd: list[str] = ["which", "swipl"]

    prolog_cmd: list[str] = [
        "swipl",
        "./data/knowledge_base.pl",
        "./data/query.pl",
    ]

    try:
        returned_output = subprocess.check_output(check_cmd)
        returned_string = returned_output.decode("utf-8").strip()
        if len(returned_string) == 0:
            raise FileNotFoundError(
                "swipl is not installed, please install it before using"
            )

        returned_output: bytes = subprocess.check_output(prolog_cmd)
        returned_string = returned_output.decode("utf-8").strip()
        # [1:-1] indexing is done to remove the opening and closing square brackets
        returned_string = returned_string[1:-1]

        if len(returned_string) != 0:
            matching_diseases = [
                disease.strip() for disease in returned_string.split(",")
            ]
    except CalledProcessError as e:
        print(f"CalledProcessError :: {e.cmd}")
    except FileNotFoundError as e:
        print(e)

    return matching_diseases

