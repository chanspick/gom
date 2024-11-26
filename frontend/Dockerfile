# Frontend Dockerfile

# 빌드를 위한 Node 베이스 이미지 사용
FROM node:20 AS build

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 파일 복사 및 의존성 설치
COPY package*.json ./
RUN npm install

# 소스 코드 복사 및 빌드
COPY . .
RUN npm run build

# 빌드된 파일을 서빙하기 위한 Nginx 이미지 사용
FROM nginx:alpine

# Nginx 설정 파일 덮어쓰기 (선택 사항)
# COPY nginx.conf /etc/nginx/nginx.conf

# 빌드된 정적 파일을 Nginx 기본 경로로 복사
COPY --from=build /app/public /usr/share/nginx/html

# Nginx 실행 (기본적으로 80번 포트 사용)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
