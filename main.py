from config.router.router import Router

# from config.database.db import engine

# # 1. Connect database
# engine.connect()

# 2. Buat instance router dari Class Router
router_instance = Router()

# 3. Ekspos app ke luar agar uvicorn/reload mode bisa membacanya jika diperlukan
app = router_instance.app
