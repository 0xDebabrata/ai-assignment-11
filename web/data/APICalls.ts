const SERVER_URL = "http://localhost:8000";

export const getInitialQuestions = async () => {
  const resp = await fetch(SERVER_URL + "/initial-questions");
  const {
    initial_questions,
    already_asked_mask,
    selected_mask,
  }: {
    initial_questions: string[];
    already_asked_mask: string;
    selected_mask: string;
  } = await resp.json();

  const numerical_already_asked_mask = BigInt(already_asked_mask);
  const numerical_selected_mask = BigInt(selected_mask);

  return {
    initial_questions: initial_questions,
    selected_mask: numerical_selected_mask,
    already_asked_mask: numerical_already_asked_mask,
  };
};

export const getNextQuestions = async (
  selectedSymptoms: string[],
  selectedMask: bigint,
  alreadyAskedMask: bigint
) => {
  const resp = await fetch(SERVER_URL + "/next-questions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      symptoms: selectedSymptoms,
      already_asked_mask: alreadyAskedMask.toString(),
      already_selected_symptoms_mask: selectedMask.toString(),
    }),
  });

  const {
    next_questions,
    already_asked_mask,
    selected_mask,
  }: {
    next_questions: string[];
    already_asked_mask: string;
    selected_mask: string;
  } = await resp.json();
  const numerical_already_asked_mask = BigInt(already_asked_mask);
  const numerical_selected_mask = BigInt(selected_mask);

  return {
    next_questions: next_questions,
    selected_mask: numerical_selected_mask,
    already_asked_mask: numerical_already_asked_mask,
  };
};

export const getDiseases = async (
  selectedSymptoms: string[],
  selectedMask: bigint,
  alreadyAskedMask: bigint
) => {
  const resp = await fetch(SERVER_URL + "/matching-diseases", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      symptoms: selectedSymptoms,
      already_asked_mask: alreadyAskedMask.toString(),
      already_selected_symptoms_mask: selectedMask.toString(),
    }),
  });

  const {
    diseases,
  }: {
    diseases: string[];
  } = await resp.json();

  return diseases;
};
