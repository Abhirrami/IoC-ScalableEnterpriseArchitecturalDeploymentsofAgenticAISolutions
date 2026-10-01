# Single-service production image: build the React application, then serve it with FastAPI.
FROM node:20-alpine AS frontend-build
WORKDIR /frontend
COPY Assignment/2023103552-Santhosh-K/frontend/package*.json ./
RUN npm ci
COPY Assignment/2023103552-Santhosh-K/frontend/ ./
RUN npm run build

FROM python:3.12-slim AS runtime
WORKDIR /app
COPY Assignment/2023103552-Santhosh-K/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY Assignment/2023103552-Santhosh-K/backend/app ./app
COPY --from=frontend-build /frontend/dist ./app/static
ENV PORT=10000
EXPOSE 10000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
