from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    id: int
    name: str
    description: str | None = None


# 샘플 데이터
items_db: list[Item] = [
    Item(id=1, name="Item 1", description="First item"),
    Item(id=2, name="Item 2", description="Second item"),
]


@app.get("/health", response_model=HealthResponse)
def health_check():
    """헬스 체크 엔드포인트"""
    return HealthResponse(status="ok", message="API is running")


@app.get("/api/items", response_model=list[Item])
def get_items():
    """모든 아이템 조회"""
    return items_db


@app.get("/api/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """특정 아이템 조회"""
    for item in items_db:
        if item.id == item_id:
            return item
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/api/items", response_model=Item, status_code=201)
def create_item(item: Item):
    """새 아이템 생성"""
    items_db.append(item)
    return item


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """아이템 삭제"""
    global items_db
    items_db = [item for item in items_db if item.id != item_id]
    return None
