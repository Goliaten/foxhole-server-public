from typing import List, Optional, TypedDict


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
    descriptionType: Optional[str]
    shardName: str
    shardId: int
    bEnabled: bool
    bEnableJoinEventsColonial: bool
    bEnableJoinEventsWarden: bool
    colonialQueueWarning: Optional[str]
    wardenQueueWarning: Optional[str]
    warServiceExternalURL: str
    warSupportURL: str
    travelMapMinimumOpenSlots: int
    bFactionLock: bool


class ClientConfig(TypedDict):
    globalShardConfig: GlobalShardConfig
    availableShardList: List[AvailableShard]
