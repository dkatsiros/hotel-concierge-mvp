import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import health, chat, tools

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Sync knowledge base to ElevenLabs on startup
    if settings.elevenlabs_api_key and settings.elevenlabs_agent_id:
        try:
            from app.services.elevenlabs_kb import ElevenLabsKBSync

            syncer = ElevenLabsKBSync()
            docs = syncer.sync()
            print(f"ElevenLabs KB synced: {len(docs)} docs")
        except Exception as e:
            print(f"WARNING: ElevenLabs KB sync failed on startup: {e}")

        # Sync tools if webhook URL is configured
        if settings.webhook_base_url:
            try:
                from app.services.elevenlabs_tools import ElevenLabsToolSync

                syncer = ElevenLabsToolSync()
                tools_created = syncer.sync()
                print(f"ElevenLabs tools synced: {len(tools_created)} tools")
            except Exception as e:
                print(f"WARNING: ElevenLabs tool sync failed on startup: {e}")
    yield


app = FastAPI(title="Hotel Concierge API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(tools.router)
