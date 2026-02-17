from fastapi import FastAPI

app = FastAPI(title="Airplane E‑Ticketing API")


@app.get("/")
def root():
    return {"message": "API is running successfully"}