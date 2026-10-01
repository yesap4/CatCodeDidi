from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_ai import ask_gemini

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserResponse(BaseModel):
    Prompt: str


@app.get("/")
def root():
    return {"CatCodeDidi": "Made With Patience and Curiosity"}


@app.post("/Prompt")
def reply_to_prompt(response: UserResponse):
    answer = ask_gemini(response.Prompt)
    return {"UserPrompt":answer}