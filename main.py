import json
import os
import uvicorn
from fastapi import FastAPI
from configparser import ConfigParser

from core.parser import Parser
from resources.matches import matches_server


app = FastAPI()
app.include_router(matches_server.router)

@app.get("/")
async def root():
    return "Quake parser is running!"


def main():

    settings = ConfigParser()
    settings.read("settings.ini")

    log_parser = Parser(settings["data"]["input_file"])
    log_parser.build_json(settings["data"]["output_file"])

    uvicorn.run(
        "main:app",
        host=settings["server"]["host"],
        port=int(settings["server"]["port"]),
        reload=True
    )


if __name__ == "__main__":
    main()
