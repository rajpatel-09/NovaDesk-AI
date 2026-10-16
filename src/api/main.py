from fastapi import FastAPI
from pydantic import BaseModel, field_validator         # BaseModel defines expected structure of incoming json
from src.rag.pipeline import RAGPipeline

app = FastAPI(title="NovaDesk AI API")  # Initialize the application

# Create the RAG pipeline once when the API application starts.
rag_pipeline = RAGPipeline()

class QuestionRequest(BaseModel):
    question: str

    @field_validator("question")        # tells Pydantic to validate the question field.
    @classmethod
    def validate_question(cls, value:str) -> str:
        value=value.strip()             # removes spaces at the beginning and end.

        if not value:
            raise ValueError("Question must not be empty.")

        return value

# **********************************************************************************************

# open NovaDesk AI and want to check whether its API server is working.
# Think of /health as asking your application: "Are you there and responding?"

@app.get("/health")     # defines an endpoint that responds to HTTP GET requests at /health
def health_check():     # returns a small JSON response confirming that the API is available
    return {
        "status": "ok",
        "project": "NovaDesk AI"
    }

# get usually retrieves info

# *********************************************************************************************



# ********************************************************************************************************

# Previously, you asked questions by running Python commands in the VS Code terminal. Now we want another application—or a frontend—to send questions to NovaDesk AI through an API.

@app.post("/ask")
def ask_question(request:QuestionRequest):
    answer = rag_pipeline.ask(request.question)

    return{
        "question":request.question,
        "answer":answer,
    }

# POST commonly sends data for the server to process.