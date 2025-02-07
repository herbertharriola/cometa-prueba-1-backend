from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.endpoints import orders
from app.api.endpoints import stock

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las conexiones, cambia esto por dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir routers de endpoints
app.include_router(orders.router)
app.include_router(stock.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de cervezas"}

if __name__ == "__main__":
    port = 8000
    print(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
