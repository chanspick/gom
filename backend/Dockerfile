# Backend Dockerfile

# Python 베이스 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# FastAPI 서버 실행 (기본적으로 8000번 포트 사용)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
