# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Working Directory ----------
WORKDIR /app

# ---------- System Dependencies ----------
# Install minimal system dependencies required by pdfplumber & sentence-transformers
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     build-essential \
     libpoppler-cpp-dev \
     pkg-config \
     poppler-utils \
     git \
  && rm -rf /var/lib/apt/lists/*

# ---------- Install Python Dependencies ----------
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy Application Code ----------
COPY . /app

# ---------- Expose Port ----------
EXPOSE 8000

# ---------- Run FastAPI ----------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
