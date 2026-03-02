"""CLI entrypoint: sync local knowledge base to ElevenLabs agent.

Usage: cd backend && python -m app.scripts.sync_knowledge
"""

import logging
import sys

from dotenv import load_dotenv

load_dotenv()

from app.config import settings
from app.services.elevenlabs_kb import ElevenLabsKBSync

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    if not settings.elevenlabs_api_key:
        logger.error("ELEVENLABS_API_KEY not set")
        sys.exit(1)
    if not settings.elevenlabs_agent_id:
        logger.error("ELEVENLABS_AGENT_ID not set")
        sys.exit(1)

    syncer = ElevenLabsKBSync()
    docs = syncer.sync()
    print(f"Synced {len(docs)} docs to ElevenLabs agent {settings.elevenlabs_agent_id}")
    for doc in docs:
        print(f"  - {doc.get('name', doc.get('id', '?'))}")


if __name__ == "__main__":
    main()
