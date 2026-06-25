import uvicorn
from fastapi import FastAPI
from config.env.env import env
from domains.users.user_controller import UserController
from domains.uploadFile.upload_file_controller import UploadController
from config.limiter.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


class Router:
    def __init__(self):
        self.app = FastAPI(title="Python API Server", version="1.0")
        self.app.state.limiter = limiter
        self.app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        self.host = env.beHost
        self.port = int(env.bePort)
        self._setup_routes()

    def _setup_routes(self):
        self.app.include_router(UserController.get_router())
        self.app.include_router(UploadController.get_router())

        @self.app.get("/")
        def root():
            return {"message": "Welcome to Python FastAPI + MySQL!"}

        @self.app.get("/api/health-check")
        def health_check():
            return {"status": "OK", "message": "Health check passed"}

    def listen(self):
        print(f"🚀 Server running at http://{self.host}:{self.port}")

        uvicorn.run(
            "main:router_instance.app", host=self.host, port=self.port, reload=True
        )
