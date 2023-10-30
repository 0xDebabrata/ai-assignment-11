'use client'
import { ChangeEvent, useEffect, useState } from "react";

import Diseases from "@/components/Diseases";
import {
  getDiseases,
  getInitialQuestions,
  getNextQuestions,
} from "@/data/api";

enum Steps {
  INITIAL_INQUIRY,
  FIRST_DETAILED_INQUIRY,
  SECOND_DETAILED_INQUIRY,
  DISEASE_DIAGNOSIS,
}

const headings = [
  "do you have any of these symptoms?",
  "do you have any of these symptoms?",
  "any other symptoms?",
]

function App() {
  const [step, setStep] = useState<Steps>(Steps.INITIAL_INQUIRY);
  const [error, setError] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [questions, setQuestions] = useState<string[]>([]);
  const [alreadyAskedMask, setAlreadyAskedMask] = useState<bigint>(BigInt(0n));
  const [selectedMask, setSelectedMask] = useState<bigint>(BigInt(0n));
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [diseases, setDiseases] = useState<string[]>([]);

  const addOrRemoveSymptom = async (e: ChangeEvent<HTMLInputElement>) => {
    setError(false);
    if (selectedSymptoms.includes(e.target.value)) {
      setSelectedSymptoms((prev) =>
        prev.filter((symptom) => symptom !== e.target.value)
      );
    } else {
      setSelectedSymptoms((prev) => [...prev, e.target.value]);
    }
  };

  const renderInitialQuestions = async () => {
    const { initial_questions, selected_mask, already_asked_mask } =
      await getInitialQuestions();

    setQuestions(initial_questions);
    console.log(initial_questions)
    setSelectedMask(selected_mask);
    setAlreadyAskedMask(already_asked_mask);
    setLoading(false);
  };

  const nextStep = async () => {
    setLoading(true);

    if (step === Steps.INITIAL_INQUIRY) {
      if (selectedSymptoms.length === 0) {
        // alert("must select atleast one symptom to continue...");
        setError(true);
      } else {
        const { next_questions, selected_mask, already_asked_mask } =
          await getNextQuestions(
            selectedSymptoms,
            selectedMask,
            alreadyAskedMask
          );

        if (next_questions.length === 0) {
          setStep(Steps.DISEASE_DIAGNOSIS);
          setDiseases([]);
          setLoading(false);
          return;
        }

        setQuestions(next_questions);
        setSelectedMask(selected_mask);
        setAlreadyAskedMask(already_asked_mask);
        setStep(Steps.FIRST_DETAILED_INQUIRY);
      }
    } else if (step === Steps.FIRST_DETAILED_INQUIRY) {
      setStep(Steps.SECOND_DETAILED_INQUIRY);
    } else if (step === Steps.SECOND_DETAILED_INQUIRY) {
      const diseases = await getDiseases(
        selectedSymptoms,
        selectedMask,
        alreadyAskedMask
      );

      setDiseases(diseases);
      setStep(Steps.DISEASE_DIAGNOSIS);
    }

    setLoading(false);
  };

  useEffect(() => {
    renderInitialQuestions();
  }, []);

  if (loading) {
    return (
      <section className="bg-neutral-200 min-h-screen text-neutral-800 w-full flex justify-center items-center flex-col">
        <h1 className="text-4xl py-4">disease prediction system</h1>
        <h2 className="text-2xl pb-4">ai assignment 11</h2>
        <p>Loading...</p>
      </section>
    )
  }

  return (
    <section className="bg-neutral-200 min-h-screen text-neutral-800 w-full flex justify-center items-center flex-col">
      <h1 className="text-4xl py-4">disease prediction system</h1>
      <h2 className="text-2xl pb-4">ai assignment 11</h2>
      {/*
      <div className="flex space-x-2 px-10 py-4 flex-wrap items-center justify-center">
        <p>
          symptoms:
        </p>
        {selectedSymptoms.map(symptom => (
          <div key={symptom} className="rounded-full py-1 px-3 bg-indigo-200 text-sm border border-indigo-500">
            {symptom.replaceAll("_", " ")}
          </div>
        ))}
      </div>
      */}
      {step === 3 ? (
        <Diseases diseases={diseases} />
      ) : (
        questions.length && (
          <>
            <form className="w-full items-start max-w-2xl">
              <h1 className="w-full text-left text-xl py-5">
                {headings[step]}
              </h1>
              {step === 0 ? questions
                .map((question) => (
                  <div key={question} className="py-1.5">
                    <input
                      onChange={addOrRemoveSymptom}
                      type="checkbox"
                      value={question}
                      className="mr-3 my-2"
                    />
                    <label htmlFor="question">
                      {question.replaceAll("_", " ")}
                    </label>
                  </div>
              )) : questions.slice((step - 1) * questions.length / 2, step * questions.length / 2)
                .map((question) => (
                  <div key={question} className="py-1.5">
                    <input
                      onChange={addOrRemoveSymptom}
                      type="checkbox"
                      value={question}
                      className="mr-3 my-2"
                    />
                    <label htmlFor="question">
                      {question.replaceAll("_", " ")}
                    </label>
                  </div>
              ))}

              {error && (
                <h4 className=" text-red-400 text-sm py-3">
                  please select a symptom.
                </h4>
              )}
              <button
                className="border border-indigo-500 py-1.5 rounded-md my-5 text-indigo-600 duration-150 hover:bg-indigo-500 hover:text-white"
                type="button"
                onClick={nextStep}
              >
                {step === Steps.SECOND_DETAILED_INQUIRY
                  ? "check disease"
                  : "continue"}
              </button>
            </form>
          </>
        )
      )}
    </section>
  );
}

export default App;
