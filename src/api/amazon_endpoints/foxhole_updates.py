from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.core.TypedDicts.ClientConfig import ClientConfig
from src.core.Logger import Logger

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
                "normalizedGlobalPopulation": 0.9,
                "descriptionType": "LiveRegularPlayers",
                "shardName": "ABLE",
                "shardId": 5,
                "bEnabled": True,
                "bEnableJoinEventsColonial": False,
                "bEnableJoinEventsWarden": False,
                "colonialQueueWarning": "Auto",
                "wardenQueueWarning": "Auto",
                # "warServiceExternalURL": "http://s3.amazonaws.com/war-service-live/",
                "warServiceExternalURL": "https://war-service-live.foxholeservices.com/external",
                # "warSupportURL": "http://s3.amazonaws.com/war-support-live/",
                "warSupportURL": "https://war-support-live.foxholeservices.com/api",
                "travelMapMinimumOpenSlots": 2,
                "bFactionLock": True,
            },
        ],
    }

    return JSONResponse(content=jsonable_encoder(out))


@router.get("/", response_model=None)
@router.get("/{path:path}", response_model=None)
async def default_path(path=""):
    Logger().get().warning(f"/foxhole-updates/{path=}")
    return
