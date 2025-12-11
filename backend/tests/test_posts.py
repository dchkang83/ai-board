import pytest
from unittest.mock import patch, MagicMock


class TestPostsAPI:
    """게시글 API 테스트"""

    # === 목록 조회 테스트 ===
    def test_get_posts_returns_list(self, client):
        """게시글 목록 조회 성공"""
        mock_data = [
            {
                "id": 1,
                "title": "첫 번째 글",
                "content": "내용입니다",
                "author_name": "익명",
                "view_count": 0,
                "created_at": "2025-01-01T00:00:00+00:00",
                "updated_at": "2025-01-01T00:00:00+00:00",
            }
        ]

        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.order.return_value.execute.return_value.data = (
                mock_data
            )
            mock_supabase.return_value = mock_client

            response = client.get("/api/posts")

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]["title"] == "첫 번째 글"

    def test_get_posts_empty_list(self, client):
        """게시글이 없을 때 빈 목록 반환"""
        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.order.return_value.execute.return_value.data = (
                []
            )
            mock_supabase.return_value = mock_client

            response = client.get("/api/posts")

            assert response.status_code == 200
            assert response.json() == []

    # === 상세 조회 테스트 ===
    def test_get_post_success(self, client):
        """게시글 상세 조회 성공"""
        mock_data = [
            {
                "id": 1,
                "title": "테스트 글",
                "content": "테스트 내용",
                "author_name": "테스터",
                "view_count": 5,
                "created_at": "2025-01-01T00:00:00+00:00",
                "updated_at": "2025-01-01T00:00:00+00:00",
            }
        ]

        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            # select 체인
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                mock_data
            )
            # update 체인 (조회수 증가)
            mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value = (
                MagicMock()
            )
            mock_supabase.return_value = mock_client

            response = client.get("/api/posts/1")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["title"] == "테스트 글"

    def test_get_post_not_found(self, client):
        """존재하지 않는 게시글 조회 시 404"""
        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                []
            )
            mock_supabase.return_value = mock_client

            response = client.get("/api/posts/999")

            assert response.status_code == 404
            assert response.json()["detail"] == "Post not found"

    # === 등록 테스트 ===
    def test_create_post_success(self, client):
        """게시글 등록 성공"""
        mock_created = {
            "id": 1,
            "title": "새 글",
            "content": "새 내용",
            "author_name": "익명",
            "view_count": 0,
            "created_at": "2025-01-01T00:00:00+00:00",
            "updated_at": "2025-01-01T00:00:00+00:00",
        }

        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.insert.return_value.execute.return_value.data = [
                mock_created
            ]
            mock_supabase.return_value = mock_client

            response = client.post(
                "/api/posts",
                json={
                    "title": "새 글",
                    "content": "새 내용",
                    "password": "1234",
                },
            )

            assert response.status_code == 201
            data = response.json()
            assert data["title"] == "새 글"
            assert "password" not in data  # 비밀번호는 응답에 포함되지 않음

    def test_create_post_with_author_name(self, client):
        """작성자명을 지정한 게시글 등록"""
        mock_created = {
            "id": 1,
            "title": "새 글",
            "content": "새 내용",
            "author_name": "홍길동",
            "view_count": 0,
            "created_at": "2025-01-01T00:00:00+00:00",
            "updated_at": "2025-01-01T00:00:00+00:00",
        }

        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.insert.return_value.execute.return_value.data = [
                mock_created
            ]
            mock_supabase.return_value = mock_client

            response = client.post(
                "/api/posts",
                json={
                    "title": "새 글",
                    "content": "새 내용",
                    "author_name": "홍길동",
                    "password": "1234",
                },
            )

            assert response.status_code == 201
            assert response.json()["author_name"] == "홍길동"

    def test_create_post_missing_title(self, client):
        """제목 없이 등록 시 422 에러"""
        response = client.post(
            "/api/posts",
            json={"content": "내용만", "password": "1234"},
        )
        assert response.status_code == 422

    def test_create_post_missing_password(self, client):
        """비밀번호 없이 등록 시 422 에러"""
        response = client.post(
            "/api/posts",
            json={"title": "제목", "content": "내용"},
        )
        assert response.status_code == 422

    # === 수정 테스트 ===
    def test_update_post_success(self, client):
        """게시글 수정 성공"""
        mock_existing = [
            {
                "id": 1,
                "password": "$2b$12$hashedpassword",  # bcrypt 해시
            }
        ]
        mock_updated = {
            "id": 1,
            "title": "수정된 제목",
            "content": "수정된 내용",
            "author_name": "익명",
            "view_count": 0,
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
                "/api/posts/1",
                json={
                    "title": "수정된 제목",
                    "content": "수정된 내용",
                    "password": "1234",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "수정된 제목"

    def test_update_post_wrong_password(self, client):
        """잘못된 비밀번호로 수정 시 403"""
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
                "/api/posts/1",
                json={
                    "title": "수정된 제목",
                    "content": "수정된 내용",
                    "password": "wrong",
                },
            )

            assert response.status_code == 403
            assert response.json()["detail"] == "Invalid password"

    def test_update_post_not_found(self, client):
        """존재하지 않는 게시글 수정 시 404"""
        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                []
            )
            mock_supabase.return_value = mock_client

            response = client.put(
                "/api/posts/999",
                json={
                    "title": "수정된 제목",
                    "content": "수정된 내용",
                    "password": "1234",
                },
            )

            assert response.status_code == 404

    # === 삭제 테스트 ===
    def test_delete_post_success(self, client):
        """게시글 삭제 성공"""
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
                "DELETE", "/api/posts/1", json={"password": "1234"}
            )

            assert response.status_code == 204

    def test_delete_post_wrong_password(self, client):
        """잘못된 비밀번호로 삭제 시 403"""
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
                "DELETE", "/api/posts/1", json={"password": "wrong"}
            )

            assert response.status_code == 403

    def test_delete_post_not_found(self, client):
        """존재하지 않는 게시글 삭제 시 404"""
        with patch("main.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                []
            )
            mock_supabase.return_value = mock_client

            response = client.request(
                "DELETE", "/api/posts/999", json={"password": "1234"}
            )

            assert response.status_code == 404


class TestPasswordVerification:
    """비밀번호 검증 API 테스트"""

    def test_verify_password_success(self, client):
        """비밀번호 검증 성공"""
        mock_existing = [{"id": 1, "password": "$2b$12$hashedpassword"}]

        with patch("main.get_supabase") as mock_supabase, patch(
            "main.bcrypt"
        ) as mock_bcrypt:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = (
                mock_existing
            )
            mock_supabase.return_value = mock_client
            mock_bcrypt.checkpw.return_value = True

            response = client.post(
                "/api/posts/1/verify-password", json={"password": "1234"}
            )

            assert response.status_code == 200
            assert response.json()["valid"] is True

    def test_verify_password_fail(self, client):
        """비밀번호 검증 실패"""
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

            response = client.post(
                "/api/posts/1/verify-password", json={"password": "wrong"}
            )

            assert response.status_code == 200
            assert response.json()["valid"] is False
