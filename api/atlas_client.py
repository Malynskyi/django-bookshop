import logging
import os

import requests

logger = logging.getLogger(__name__)


class AtlasAPIError(Exception):
    pass


def get_warehouses():
    atlas_url = os.getenv("ATLAS_API_URL", "https://atlas-service-ovqp.onrender.com")

    try:
        print("ATLAS TOKEN:", os.getenv("ATLAS_ACCESS_TOKEN"))
        response = requests.get(
            f"{atlas_url}/api/stock/",
            headers={
                "Authorization": f"Bearer {os.getenv('ATLAS_ACCESS_TOKEN')}",
            },
            timeout=30,
        )

        if response.status_code == 401:
            logger.warning("Atlas API unauthorized")
            raise AtlasAPIError("Atlas API requires authentication")

        response.raise_for_status()
        logger.info("Successfully received warehouses from Atlas")
        return response.json()

    except requests.RequestException as exc:
        logger.exception("Atlas API request failed")
        raise AtlasAPIError(str(exc)) from exc