import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.api.routers import task, user
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
PORT = int(os.getenv("PORT"))


# Include SessionMiddleware to enable session support
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
# app.add_middleware(
#     SessionManager,
#     secret_key="your_secret_key",
#     lifetime_seconds=3600,
#     session_cookie="my_user_session",
# )


# Include routers here as you create them
# Include the tasks router
app.include_router(user.router, prefix="/users")
app.include_router(task.router, prefix="/tasks")

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=PORT, reload=True)
