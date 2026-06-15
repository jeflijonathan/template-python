import uvicorn
from fastapi import FastAPI
from config.env.env import env
from domains.users.user_controller import UserController
from domains.uploadFile.upload_file_controller import UploadController


class Router:
    def __init__(self):
        self.app = FastAPI(title="Python API Server", version="1.0")
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
        """
        Menjalankan server FastAPI menggunakan Uvicorn ASGI Server
        (setara dengan this.app.listen() di Express)
        """
        print(f"🚀 Server running at http://{self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)
