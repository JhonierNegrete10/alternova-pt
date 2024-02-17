# main.py

import logging

import users
import uvicorn
from db.configDatabase import init_db
from fastapi import FastAPI

logging.basicConfig(
    filename="app.log",
    # filemode='w',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
log = logging.getLogger("uvicorn")

# Configuración de FastAPI
app = FastAPI()

app.include_router(users.user_routes)


@app.on_event("startup")
async def startup_event():
    log.info("INIT: ___Starting up___")
    try:
        init_db()
    #   print(x)
    except Exception as e:
        print(f"An exception occurred {e}")

    log.info("INIT: ___end___")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        # host="192.168.0.190",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
