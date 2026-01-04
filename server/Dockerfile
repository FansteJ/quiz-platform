# Koristimo Python 3.11 kao osnovu
FROM python:3.11-slim

# Postavimo radni direktorijum u kontejneru
WORKDIR /app

# Kopiraj requirements.txt u kontejner
COPY requirements.txt .

# Instaliraj sve Python pakete
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj sav kod u kontejner
COPY . .

# Aplikacija sluša na portu 5000
EXPOSE 5000

# Pokreni aplikaciju
CMD ["python", "app.py"]