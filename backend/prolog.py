import subprocess
from subprocess import CalledProcessError
from typing import Dict, List, Optional

from lib import decode_symptoms 


def find_matching_diseases_prolog(
    symptoms: int | List[str],
    symptoms_mapping: Optional[Dict[str, int]] = None,
) -> List[str]:
    """
    Execute swipl statements to get results from Prolog runtime.
    This function is used to find the matching diseases for the provided
    symptoms.

    Arguments:
    ---------

    `symptoms` - List of symptoms or an integer representing the bit mask

    `symptoms_mapping` - Symptom to disease mapping. Should be provided in case
    the bit mask is also provided.
    """

    symptoms_list: List[str]
    matching_diseases: list[str] = []

    if isinstance(symptoms, List):
        symptoms_list = symptoms
    elif isinstance(symptoms, int) and symptoms_mapping is not None:
        symptoms_list = decode_symptoms(symptoms, symptoms_mapping)
    else:
        raise ValueError(
            "Invalid symptoms configuration provided."
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
        resp = subprocess.check_output(check_cmd)
        data = resp.decode("utf-8").strip()
        if len(data) == 0:
            raise FileNotFoundError(
                "swipl is not installed, please install it before using"
            )

        resp: bytes = subprocess.check_output(prolog_cmd)
        data = resp.decode("utf-8").strip()
        data = data[1:-1]       # remove square enclosing brackets

        if len(data) != 0:
            matching_diseases = [
                disease.strip() for disease in data.split(",")
            ]
    except CalledProcessError as e:
        print(f"CalledProcessError :: {e.cmd}")
    except FileNotFoundError as e:
        print(e)

    return matching_diseases
