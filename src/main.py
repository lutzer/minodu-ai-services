from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from rag.rag import RAG

# Initialize FastAPI app with root_path prefix
app = FastAPI(root_path="/services")

# Request model
class RagRequest(BaseModel):
    conversation: str
    language: str
    question: str

# Response model
class RagResponse(BaseModel):
    status: str
    answer: str

@app.get("/")
async def root():
    return {"message": "Simple FastAPI boilerplate"}

@app.post("/rag/ask", response_model=RagResponse)
async def send_message(request: RagRequest):

    rag = RAG(request.language)
    
    # result = rag.ask(request.question, request.conversation, stream=False)

    response = RagResponse(
        status="success",
        answer="test"
    )
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3010, reload=True)