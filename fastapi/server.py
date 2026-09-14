from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_root():
    return {"status": "online"}

@app.get("/users")
def get_users():
    return {"users": []}

@app.get("/users/{id}")
def get_user(id):
    return {"user": {
        "user_id": id
    }}