
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m -s /bin/bash appuser

COPY app.py .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD ["python", "app.py"]