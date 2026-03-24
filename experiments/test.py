import httpx
import asyncio

from src.helpers.response_helper import get_response_details

# URL = "https://war-support-live.foxholeservices.com/api"
URL = "https://war-service-live.foxholeservices.com/external"


async def test():
    async with httpx.AsyncClient(base_url=URL, verify=False) as client:
        headers = {
            "accept-encoding": "deflate, gzip",
            "x-steam-id": "",
            "x-steam-token": "",
            "user-agent": "War/++UE4+Release-4.24-CL-0 Windows/6.2.9200.1.256.64bit",
        }

        req = client.build_request("GET", url="modReply", headers=headers)
        r = await client.send(req, stream=True)
        print(await get_response_details(r))


if __name__ == "__main__":
    asyncio.run(test())
