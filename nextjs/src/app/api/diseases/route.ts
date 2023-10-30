import { SERVER_URL } from "@/data/api"
import { NextResponse } from "next/server";

export const POST = async (req: Request, res: Response) => {
  const {
    symptoms,
    already_asked_mask,
    already_selected_symptoms_mask
  } = await req.json()

  const resp = await fetch(SERVER_URL + "/matching-diseases", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      symptoms,
      already_asked_mask,
      already_selected_symptoms_mask,
    }),
  });
  const data = await resp.json();
  return NextResponse.json(data)
}
