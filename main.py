from fastapi import Depends, FastAPI, HTTPException
from api.repo.chat_repo import get_previous_messages
from db.configure import SessionLocal, get_db
from model.models import process_query
from fastapi.middleware.cors import CORSMiddleware
from api.schema.request import QueryRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/ping")
async def health_check():
    return {"status": "ok"}


@app.get("/fetch")
async def get_chat_history(user_id: str, db: SessionLocal = Depends(get_db)): # type: ignore
    try: 
        response = get_previous_messages(user_id, db)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/query")
async def query_bot(request: QueryRequest, db: SessionLocal = Depends(get_db)): # type: ignore
    try:
        response = process_query(db, request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

