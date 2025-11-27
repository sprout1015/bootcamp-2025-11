# Backend Dockerfile
# 실행 전용 Dockerfile for Spring Boot GraphQL Application
FROM eclipse-temurin:17

WORKDIR /app

# 이미 빌드된 JAR을 복사 (Dockerfile과 같은 디렉토리에 두기)
COPY build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]