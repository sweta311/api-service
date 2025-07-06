FROM python:3.11-slim-bullseye as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --prefix="/install" -r requirements.txt

COPY . .


FROM python:3.11-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN adduser --system --group nonroot

COPY --from=builder /install /usr/local

COPY --from=builder /app .

RUN chown -R nonroot:nonroot /app

USER nonroot

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
