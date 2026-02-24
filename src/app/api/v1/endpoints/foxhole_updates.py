from fastapi import APIRouter

from app.core.TypedDicts.ClientConfig import ClientConfig

router = APIRouter(prefix="/foxhole-updates", tags=["foxhole-updates"])


@router.get("/config/client_config.json", response_model=ClientConfig)
async def client_config() -> ClientConfig:
    print("path=/config/client_config.json")
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
                "warServiceExternalURL": "https://war-service-live.foxholeservices.com/external",
                "warSupportURL": "https://war-support-live.foxholeservices.com/api",
                "travelMapMinimumOpenSlots": 2,
                "bFactionLock": True,
            },
        ],
    }
    return out


@router.get("/{path:path}", response_model=None)
async def default_path(path):
    print(f"{path=}")
    return
