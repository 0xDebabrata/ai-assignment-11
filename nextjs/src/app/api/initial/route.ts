import { SERVER_URL } from "@/data/api"
import { NextResponse } from "next/server";

export const dynmic = 'force-dynamic'

export const GET = async (req: Request, res: Response) => {
  const resp = await fetch(SERVER_URL + "/initial-questions");
  const data = await resp.json();
  return NextResponse.json(data)
}
