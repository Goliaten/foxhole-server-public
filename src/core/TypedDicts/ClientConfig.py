from typing import List, TypedDict


class GlobalShardConfig(TypedDict):
    defaultShardId: int
    bEnableOverpopMode: bool
    bRedirectToShardSelector: bool
    overpopShardId: int
    overpopTextType: str
    overpopYesButtonType: str
    overpopNoButtonType: str
    bEnableRandomHomeRegion: bool
    deployDelayMin: int
    deployDelayMax: int
    preConquestDeployDelayMin: int
    preConquestDeployDelayMax: int
    serverRestartDeployDelayMin: int
    serverRestartDeployDelayMax: int


class AvailableShard(TypedDict):
    normalizedGlobalPopulation: float
    descriptionType: str
    shardName: str
    shardId: int
    bEnabled: bool
    bEnableJoinEventsColonial: bool
    bEnableJoinEventsWarden: bool
    colonialQueueWarning: str
    wardenQueueWarning: str
    warServiceExternalURL: str
    warSupportURL: str
    travelMapMinimumOpenSlots: int
    bFactionLock: bool


class ClientConfig(TypedDict):
    globalShardConfig: GlobalShardConfig
    availableShardList: List[AvailableShard]
