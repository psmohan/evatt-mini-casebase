from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ingest import ingest_file
from search import search_query

app = FastAPI(title="Evatt Mini Casebase - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    q: str
    top_k: int = 5


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "text/plain"):
        raise HTTPException(
            status_code=400, detail="Only PDF or plain text files are supported"
        )
    content = await file.read()
    count = ingest_file(file.filename, content)
    return {"ingested_chunks": count}


@app.post("/search")
async def search(req: SearchRequest):
    results = search_query(req.q, top_k=req.top_k)
    return {"query": req.q, "results": results}
