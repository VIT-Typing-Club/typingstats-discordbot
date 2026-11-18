import aiohttp
import logging

from config import API_URL

log = logging.getLogger(__name__)


async def sync_typegg_scores(discord_id: str) -> dict:
    timeout = aiohttp.ClientTimeout(total=30)

    url = f"{API_URL}/api/scores/typegg/sync/{discord_id}"

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url) as response:

                try:
                    data = await response.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError):
                    data = {}

                if not isinstance(data, dict):
                    data = {}

                success = 200 <= response.status < 300

                return {
                    "success": success,
                    "status": response.status,
                    "message": data.get(
                        "message",
                        data.get("error", "Unknown API response")
                    ),
                }

    except aiohttp.ClientError as e:
        log.error("TypeGG SYNC API ERROR: %s", e)

        return {
            "success": False,
            "status": None,
            "message": "Could not connect to the TypeGG API."
        }

    except TimeoutError:
        log.error("TypeGG SYNC API timed out.")

        return {
            "success": False,
            "status": None,
            "message": "The TypeGG API took too long to respond."
        }
