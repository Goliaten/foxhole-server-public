from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.core.Models.ClientConfig import ClientConfig
from src.core.Logger import Logger
import src.config as cfg

router = APIRouter(prefix="/foxhole-updates")


@router.get("/config/client_config.json", response_model=ClientConfig)
async def client_config():
    Logger().get().debug("path=/foxhole-updates/config/client_config.json")

    out: ClientConfig = {
        "globalShardConfig": {
            "defaultShardId": 7,
            "bEnableOverpopMode": True,
            "bRedirectToShardSelector": False,
            "overpopShardId": 7,
            "overpopTextType": "ShardAtCapacity",
            "overpopYesButtonType": "ChangeShard",
            "overpopNoButtonType": "WaitInQueue",
            "bEnableRandomHomeRegion": True,
            "deployDelayMin": 2,
            "deployDelayMax": 14,
            "preConquestDeployDelayMin": 10,
            "preConquestDeployDelayMax": 360,
            "serverRestartDeployDelayMin": 10,
            "serverRestartDeployDelayMax": 300,
        },
        "availableShardList": [
            {
                "normalizedGlobalPopulation": 0.0,
                "descriptionType": None,
                "shardName": "Internal-2",
                "shardId": 1,
                "bEnabled": False,
                "bEnableJoinEventsColonial": False,
                "bEnableJoinEventsWarden": False,
                "colonialQueueWarning": "Auto",
                "wardenQueueWarning": "Auto",
                "warServiceExternalURL": "https://internal-2-war.foxholeservices.com/external",
                "warSupportURL": "https://war-support.foxholeservices.com/api",
                "travelMapMinimumOpenSlots": 5,
                "bFactionLock": True,
            },
            {
                "normalizedGlobalPopulation": 0.0,
                "descriptionType": None,
                "shardName": "LocalDevTest",
                "shardId": 2,
                "bEnabled": False,
                "bEnableJoinEventsColonial": False,
                "bEnableJoinEventsWarden": False,
                "colonialQueueWarning": "Auto",
                "wardenQueueWarning": "Auto",
                "warServiceExternalURL": "http://127.0.0.1:9998/external",
                "warSupportURL": "https://war-support-live.foxholeservices.com/api",
                "travelMapMinimumOpenSlots": 2,
                "bFactionLock": True,
            },
            {
                "normalizedGlobalPopulation": 0.0,
                "descriptionType": None,
                "shardName": "Internal-1",
                "shardId": 3,
                "bEnabled": False,
                "bEnableJoinEventsColonial": False,
                "bEnableJoinEventsWarden": False,
                "colonialQueueWarning": "Auto",
                "wardenQueueWarning": "Auto",
                "warServiceExternalURL": "https://internal-war.foxholeservices.com/external",
                "warSupportURL": "https://war-support.foxholeservices.com/api",
                "travelMapMinimumOpenSlots": 2,
                "bFactionLock": True,
            },
            {
                "normalizedGlobalPopulation": 0.6,
                "descriptionType": "TestingFeatures",
                "shardName": "DevBranch",
                "shardId": 4,
                "bEnabled": False,
                "bEnableJoinEventsColonial": False,
                "bEnableJoinEventsWarden": False,
                "colonialQueueWarning": "Auto",
                "wardenQueueWarning": "Auto",
                "warServiceExternalURL": "https://war-service-dev.foxholeservices.com/external",
                "warSupportURL": "https://war-support-live.foxholeservices.com/api",
                "travelMapMinimumOpenSlots": 2,
                "bFactionLock": False,
            },
            {
                "normalizedGlobalPopulation": 0.9,
                "descriptionType": "LiveRegularPlayers",
                "shardName": "ABLE",
                "shardId": 5,
                "bEnabled": True,
                "bEnableJoinEventsColonial": False,
                "bEnableJoinEventsWarden": False,
                "colonialQueueWarning": "Auto",
                "wardenQueueWarning": "Auto",
                "warServiceExternalURL": "http://localhost/war-service-live",
                # "warServiceExternalURL": "http://s3.amazonaws.com/war-service-live/",
                # "warServiceExternalURL": "https://war-service-live.foxholeservices.com/external",
                # "warSupportURL": "http://localhost/war-support-live",
                # "warSupportURL": "http://s3.amazonaws.com/war-support-live/",
                "warSupportURL": "https://war-support-live.foxholeservices.com/api",
                "travelMapMinimumOpenSlots": 2,
                "bFactionLock": True,
            },
            {
                "normalizedGlobalPopulation": 0.4,
                "descriptionType": "LiveReturningPlayers",
                "shardName": "BAKER",
                "shardId": 6,
                "bEnabled": False,
                "bEnableJoinEventsColonial": False,
                "bEnableJoinEventsWarden": False,
                "colonialQueueWarning": "Auto",
                "wardenQueueWarning": "Auto",
                "warServiceExternalURL": "https://war-service-live-2.foxholeservices.com/external",
                "warSupportURL": "https://war-support-live.foxholeservices.com/api",
                "travelMapMinimumOpenSlots": 2,
                "bFactionLock": True,
            },
            {
                "normalizedGlobalPopulation": 0.7,
                "descriptionType": "LiveReturningPlayers",
                "shardName": "CHARLIE",
                "shardId": 7,
                "bEnabled": True,
                "bEnableJoinEventsColonial": False,
                "bEnableJoinEventsWarden": False,
                "colonialQueueWarning": None,
                "wardenQueueWarning": None,
                "warServiceExternalURL": "https://war-service-live-3.foxholeservices.com/external",
                "warSupportURL": "https://war-support-live.foxholeservices.com/api",
                "travelMapMinimumOpenSlots": 2,
                "bFactionLock": True,
            },
        ],
    }

    return JSONResponse(content=jsonable_encoder(out))


@router.api_route("/", response_model=None, methods=cfg.ALL_METHODS)
@router.api_route("/{path:path}", response_model=None, methods=cfg.ALL_METHODS)
async def default_path(request: Request, path=""):
    Logger().get().warning(f"/foxhole-updates/{path=}")
    headers = dict(request.headers)

    # Query parameters
    query_params = dict(request.query_params)

    # Client IP (if behind a proxy, use X-Forwarded-For)
    client_host = request.client.host if request.client else None

    # Body (only for POST, PUT, PATCH, etc.)
    body = None
    try:
        body = await request.body()
        body = body.decode("utf-8") if body else None
    except Exception as e:
        body = f"Error reading body: {e}"

    # URL and method
    url = str(request.url)
    method = request.method
    Logger().get().debug(
        {
            "url": url,
            "method": method,
            "path": path,
            "client_host": client_host,
            "headers": headers,
            "query_params": query_params,
            "body": body,
        }
    )
    return
