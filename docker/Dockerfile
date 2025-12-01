FROM python:3.10-slim


WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy minimal project pieces for gateway demo
COPY services /app/services
COPY libs /app/libs
COPY .env /app/.env
ENV PYTHONPATH=/app


EXPOSE 8080
CMD ["uvicorn", "services.gateway.app:app", "--host", "0.0.0.0", "--port", "8080"]