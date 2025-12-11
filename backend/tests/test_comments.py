import pytest
from unittest.mock import patch, MagicMock


class TestCommentsAPI:
    """댓글 API 테스트"""

    # === 댓글 목록 조회 테스트 ===
    def test_get_comments_returns_list(self, client):
        """게시글의 댓글 목록 조회 성공"""
        mock_data = [
            {
                "id": 1,
                "post_id": 1,
                "parent_id": None,
                "content": "첫 번째 댓글",
                "author_name": "익명",
                "created_at": "2025-01-01T00:00:00+00:00",
                "updated_at": "2025-01-01T00:00:00+00:00",
            },
            {
                "id": 2,
                "post_id": 1,
                "parent_id": 1,  # 대댓글
                "content": "첫 번째 댓글의 답글",
                "author_name": "다른익명",
                "created_at": "2025-01-01T01:00:00+00:00",
                "updated_at": "2025-01-01T01:00:00+00:00",
            },
        ]

        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = (
                mock_data
            )
            mock_supabase.return_value = mock_client

            response = client.get("/api/posts/1/comments")

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["content"] == "첫 번째 댓글"
            assert data[1]["parent_id"] == 1

    def test_get_comments_empty_list(self, client):
        """댓글이 없을 때 빈 목록 반환"""
        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = (
                []
            )
            mock_supabase.return_value = mock_client

            response = client.get("/api/posts/1/comments")

            assert response.status_code == 200
            assert response.json() == []

    # === 댓글 등록 테스트 ===
    def test_create_comment_success(self, client):
        """댓글 등록 성공"""
        mock_created = {
            "id": 1,
            "post_id": 1,
            "parent_id": None,
            "content": "새 댓글",
            "author_name": "익명",
            "created_at": "2025-01-01T00:00:00+00:00",
            "updated_at": "2025-01-01T00:00:00+00:00",
        }

        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            # 게시글 존재 확인
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
                {"id": 1}
            ]
            # 댓글 삽입
            mock_client.table.return_value.insert.return_value.execute.return_value.data = [
                mock_created
            ]
            mock_supabase.return_value = mock_client

            response = client.post(
                "/api/posts/1/comments",
                json={
                    "content": "새 댓글",
                    "password": "1234",
                },
            )

            assert response.status_code == 201
            data = response.json()
            assert data["content"] == "새 댓글"
            assert data["parent_id"] is None  # 댓글이므로 parent_id 없음
            assert "password" not in data

    def test_create_reply_success(self, client):
        """대댓글 등록 성공"""
        mock_created = {
            "id": 2,
            "post_id": 1,
            "parent_id": 1,
            "content": "대댓글",
            "author_name": "익명",
            "created_at": "2025-01-01T00:00:00+00:00",
            "updated_at": "2025-01-01T00:00:00+00:00",
        }

        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            # 게시글 존재 확인
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
                {"id": 1}
            ]
            # 댓글 삽입
            mock_client.table.return_value.insert.return_value.execute.return_value.data = [
                mock_created
            ]
            mock_supabase.return_value = mock_client

            response = client.post(
                "/api/posts/1/comments",
                json={
                    "content": "대댓글",
                    "password": "1234",
                    "parent_id": 1,
                },
            )

            assert response.status_code == 201
            data = response.json()
            assert data["content"] == "대댓글"
            assert data["parent_id"] == 1

    def test_create_comment_post_not_found(self, client):
        """존재하지 않는 게시글에 댓글 등록 시 404"""
        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                []
            )
            mock_supabase.return_value = mock_client

            response = client.post(
                "/api/posts/999/comments",
                json={
                    "content": "새 댓글",
                    "password": "1234",
                },
            )

            assert response.status_code == 404
            assert response.json()["detail"] == "Post not found"

    def test_create_comment_missing_content(self, client):
        """내용 없이 등록 시 422 에러"""
        response = client.post(
            "/api/posts/1/comments",
            json={"password": "1234"},
        )
        assert response.status_code == 422

    # === 댓글 수정 테스트 ===
    def test_update_comment_success(self, client):
        """댓글 수정 성공"""
        mock_existing = [
            {
                "id": 1,
                "post_id": 1,
                "password": "$2b$12$hashedpassword",
            }
        ]
        mock_updated = {
            "id": 1,
            "post_id": 1,
            "parent_id": None,
            "content": "수정된 댓글",
            "author_name": "익명",
            "created_at": "2025-01-01T00:00:00+00:00",
            "updated_at": "2025-01-02T00:00:00+00:00",
        }

        with patch("main.get_supabase") as mock_supabase, patch(
            "main.bcrypt"
        ) as mock_bcrypt:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                mock_existing
            )
            mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [
                mock_updated
            ]
            mock_supabase.return_value = mock_client
            mock_bcrypt.checkpw.return_value = True

            response = client.put(
                "/api/comments/1",
                json={
                    "content": "수정된 댓글",
                    "password": "1234",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["content"] == "수정된 댓글"

    def test_update_comment_wrong_password(self, client):
        """잘못된 비밀번호로 댓글 수정 시 403"""
        mock_existing = [{"id": 1, "password": "$2b$12$hashedpassword"}]

        with patch("main.get_supabase") as mock_supabase, patch(
            "main.bcrypt"
        ) as mock_bcrypt:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                mock_existing
            )
            mock_supabase.return_value = mock_client
            mock_bcrypt.checkpw.return_value = False

            response = client.put(
                "/api/comments/1",
                json={
                    "content": "수정된 댓글",
                    "password": "wrong",
                },
            )

            assert response.status_code == 403
            assert response.json()["detail"] == "Invalid password"

    def test_update_comment_not_found(self, client):
        """존재하지 않는 댓글 수정 시 404"""
        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                []
            )
            mock_supabase.return_value = mock_client

            response = client.put(
                "/api/comments/999",
                json={
                    "content": "수정된 댓글",
                    "password": "1234",
                },
            )

            assert response.status_code == 404

    # === 댓글 삭제 테스트 ===
    def test_delete_comment_success(self, client):
        """댓글 삭제 성공"""
        mock_existing = [{"id": 1, "password": "$2b$12$hashedpassword"}]

        with patch("main.get_supabase") as mock_supabase, patch(
            "main.bcrypt"
        ) as mock_bcrypt:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                mock_existing
            )
            mock_client.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = (
                mock_existing
            )
            mock_supabase.return_value = mock_client
            mock_bcrypt.checkpw.return_value = True

            response = client.request(
                "DELETE", "/api/comments/1", json={"password": "1234"}
            )

            assert response.status_code == 204

    def test_delete_comment_wrong_password(self, client):
        """잘못된 비밀번호로 댓글 삭제 시 403"""
        mock_existing = [{"id": 1, "password": "$2b$12$hashedpassword"}]

        with patch("main.get_supabase") as mock_supabase, patch(
            "main.bcrypt"
        ) as mock_bcrypt:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                mock_existing
            )
            mock_supabase.return_value = mock_client
            mock_bcrypt.checkpw.return_value = False

            response = client.request(
                "DELETE", "/api/comments/1", json={"password": "wrong"}
            )

            assert response.status_code == 403

    def test_delete_comment_not_found(self, client):
        """존재하지 않는 댓글 삭제 시 404"""
        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                []
            )
            mock_supabase.return_value = mock_client

            response = client.request(
                "DELETE", "/api/comments/999", json={"password": "1234"}
            )

            assert response.status_code == 404
