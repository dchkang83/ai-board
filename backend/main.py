from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import bcrypt
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


# === 게시글 관련 모델 ===
class Post(BaseModel):
    id: int
    title: str
    content: str
    author_name: str
    view_count: int
    created_at: str
    updated_at: str


class PostCreate(BaseModel):
    title: str
    content: str
    author_name: str = "익명"
    password: str


class PostUpdate(BaseModel):
    title: str
    content: str
    password: str


class PasswordCheck(BaseModel):
    password: str


class PasswordVerifyResponse(BaseModel):
    valid: bool


# === 댓글 관련 모델 ===
class Comment(BaseModel):
    id: int
    post_id: int
    parent_id: int | None
    content: str
    author_name: str
    created_at: str
    updated_at: str


class CommentCreate(BaseModel):
    content: str
    author_name: str = "익명"
    password: str
    parent_id: int | None = None


class CommentUpdate(BaseModel):
    content: str
    password: str


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


# === 게시글 API ===


@app.get("/api/posts", response_model=list[Post])
def get_posts():
    """게시글 목록 조회 (최신순)"""
    supabase = get_supabase()
    response = (
        supabase.table("posts")
        .select("id, title, content, author_name, view_count, created_at, updated_at")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


@app.get("/api/posts/{post_id}", response_model=Post)
def get_post(post_id: int):
    """게시글 상세 조회 (조회수 증가)"""
    supabase = get_supabase()
    response = (
        supabase.table("posts")
        .select("id, title, content, author_name, view_count, created_at, updated_at")
        .eq("id", post_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Post not found")

    # 조회수 증가
    supabase.table("posts").update(
        {"view_count": response.data[0]["view_count"] + 1}
    ).eq("id", post_id).execute()

    return response.data[0]


@app.post("/api/posts", response_model=Post, status_code=201)
def create_post(post: PostCreate):
    """게시글 등록"""
    supabase = get_supabase()

    # 비밀번호 해시화
    hashed_password = bcrypt.hashpw(
        post.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    data = {
        "title": post.title,
        "content": post.content,
        "author_name": post.author_name,
        "password": hashed_password,
    }

    response = supabase.table("posts").insert(data).execute()

    # password 필드 제외하고 반환
    result = response.data[0]
    return {
        "id": result["id"],
        "title": result["title"],
        "content": result["content"],
        "author_name": result["author_name"],
        "view_count": result["view_count"],
        "created_at": result["created_at"],
        "updated_at": result["updated_at"],
    }


@app.put("/api/posts/{post_id}", response_model=Post)
def update_post(post_id: int, post: PostUpdate):
    """게시글 수정"""
    supabase = get_supabase()

    # 기존 게시글 조회 (비밀번호 포함)
    response = supabase.table("posts").select("id, password").eq("id", post_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Post not found")

    # 비밀번호 확인
    stored_password = response.data[0]["password"]
    if not bcrypt.checkpw(post.password.encode("utf-8"), stored_password.encode("utf-8")):
        raise HTTPException(status_code=403, detail="Invalid password")

    # 게시글 수정
    update_data = {
        "title": post.title,
        "content": post.content,
        "updated_at": datetime.now().isoformat(),
    }
    update_response = (
        supabase.table("posts").update(update_data).eq("id", post_id).execute()
    )

    result = update_response.data[0]
    return {
        "id": result["id"],
        "title": result["title"],
        "content": result["content"],
        "author_name": result["author_name"],
        "view_count": result["view_count"],
        "created_at": result["created_at"],
        "updated_at": result["updated_at"],
    }


@app.delete("/api/posts/{post_id}", status_code=204)
def delete_post(post_id: int, body: PasswordCheck = Body(...)):
    """게시글 삭제"""
    supabase = get_supabase()

    # 기존 게시글 조회 (비밀번호 포함)
    response = supabase.table("posts").select("id, password").eq("id", post_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Post not found")

    # 비밀번호 확인
    stored_password = response.data[0]["password"]
    if not bcrypt.checkpw(body.password.encode("utf-8"), stored_password.encode("utf-8")):
        raise HTTPException(status_code=403, detail="Invalid password")

    # 게시글 삭제
    supabase.table("posts").delete().eq("id", post_id).execute()
    return None


@app.post("/api/posts/{post_id}/verify-password", response_model=PasswordVerifyResponse)
def verify_post_password(post_id: int, body: PasswordCheck):
    """게시글 비밀번호 검증"""
    supabase = get_supabase()

    response = supabase.table("posts").select("id, password").eq("id", post_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Post not found")

    stored_password = response.data[0]["password"]
    is_valid = bcrypt.checkpw(body.password.encode("utf-8"), stored_password.encode("utf-8"))

    return {"valid": is_valid}


# === 댓글 API ===


@app.get("/api/posts/{post_id}/comments", response_model=list[Comment])
def get_comments(post_id: int):
    """게시글의 댓글 목록 조회 (생성순)"""
    supabase = get_supabase()
    response = (
        supabase.table("comments")
        .select("id, post_id, parent_id, content, author_name, created_at, updated_at")
        .eq("post_id", post_id)
        .order("created_at", desc=False)
        .execute()
    )
    return response.data


@app.post("/api/posts/{post_id}/comments", response_model=Comment, status_code=201)
def create_comment(post_id: int, comment: CommentCreate):
    """댓글/대댓글 등록"""
    supabase = get_supabase()

    # 게시글 존재 확인
    post_response = supabase.table("posts").select("id").eq("id", post_id).execute()
    if not post_response.data:
        raise HTTPException(status_code=404, detail="Post not found")

    # 비밀번호 해시화
    hashed_password = bcrypt.hashpw(
        comment.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    data = {
        "post_id": post_id,
        "parent_id": comment.parent_id,
        "content": comment.content,
        "author_name": comment.author_name,
        "password": hashed_password,
    }

    response = supabase.table("comments").insert(data).execute()

    result = response.data[0]
    return {
        "id": result["id"],
        "post_id": result["post_id"],
        "parent_id": result["parent_id"],
        "content": result["content"],
        "author_name": result["author_name"],
        "created_at": result["created_at"],
        "updated_at": result["updated_at"],
    }


@app.put("/api/comments/{comment_id}", response_model=Comment)
def update_comment(comment_id: int, comment: CommentUpdate):
    """댓글 수정"""
    supabase = get_supabase()

    # 기존 댓글 조회 (비밀번호 포함)
    response = (
        supabase.table("comments").select("id, password").eq("id", comment_id).execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 비밀번호 확인
    stored_password = response.data[0]["password"]
    if not bcrypt.checkpw(
        comment.password.encode("utf-8"), stored_password.encode("utf-8")
    ):
        raise HTTPException(status_code=403, detail="Invalid password")

    # 댓글 수정
    update_data = {
        "content": comment.content,
        "updated_at": datetime.now().isoformat(),
    }
    update_response = (
        supabase.table("comments").update(update_data).eq("id", comment_id).execute()
    )

    result = update_response.data[0]
    return {
        "id": result["id"],
        "post_id": result["post_id"],
        "parent_id": result["parent_id"],
        "content": result["content"],
        "author_name": result["author_name"],
        "created_at": result["created_at"],
        "updated_at": result["updated_at"],
    }


@app.delete("/api/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, body: PasswordCheck = Body(...)):
    """댓글 삭제"""
    supabase = get_supabase()

    # 기존 댓글 조회 (비밀번호 포함)
    response = (
        supabase.table("comments").select("id, password").eq("id", comment_id).execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 비밀번호 확인
    stored_password = response.data[0]["password"]
    if not bcrypt.checkpw(body.password.encode("utf-8"), stored_password.encode("utf-8")):
        raise HTTPException(status_code=403, detail="Invalid password")

    # 댓글 삭제 (대댓글도 cascade로 삭제됨)
    supabase.table("comments").delete().eq("id", comment_id).execute()
    return None
