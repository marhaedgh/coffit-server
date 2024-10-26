from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controller import InferenceController, UserController, NotificationController

from service.AgentService import AgentService

import ModelLoader

SWAGGER_HEADERS = {
    "title": "말해다규현 api 서버 테스트",
    "version": "0.1.0",
    "description": "## 말해다규현 api 서버 입니다.\n",
    "contact": {
        "name": "wagyu",
    },
}
app = FastAPI(
    swagger_ui_parameters={
        "deepLinking": True,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "operationsSorter": "method",
        "filter": True,
    },
    **SWAGGER_HEADERS
)

origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add router
app.include_router(InferenceController.router)
app.include_router(UserController.router)
app.include_router(NotificationController.router)

agent_service = AgentService(ModelLoader.InferenceModel())