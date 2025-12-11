from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_supabase

app = FastAPI(title="AI Board API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3010"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    message: str


class Item(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


@app.get("/health", response_model=HealthResponse)
def health_check():
    """헬스 체크 엔드포인트"""
    return HealthResponse(status="ok", message="API is running")


@app.get("/api/items", response_model=list[Item])
def get_items():
    """모든 아이템 조회"""
    supabase = get_supabase()
    response = supabase.table("items").select("*").execute()
    return response.data


@app.get("/api/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """특정 아이템 조회"""
    supabase = get_supabase()
    response = supabase.table("items").select("*").eq("id", item_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Item not found")
    return response.data[0]


@app.post("/api/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    """새 아이템 생성"""
    supabase = get_supabase()
    response = supabase.table("items").insert(item.model_dump()).execute()
    return response.data[0]


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """아이템 삭제"""
    supabase = get_supabase()
    response = supabase.table("items").delete().eq("id", item_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
