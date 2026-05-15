from typing import Optional

from src.core.Logger import Logger


class PacketAnalyzer:
    @staticmethod
    def get_packet_opcode(data: bytes) -> Optional[int]:

        if not isinstance(data, (bytes, bytearray)) or len(data) < 8:
            Logger().get().debug(f"{type(data)=} {len(data)=}")
            Logger().get().error("Data is not `bytes` or `bytearray` or len(data) < 8.")
            return None

        root_off = int.from_bytes(data[:4], "little")

        if not (0 < root_off < len(data) - 4):
            Logger().get().debug(f"{root_off=} {len(data)=}")
            Logger().get().error(
                "Invalid root offset. Expected (0 < root_off < len(data) - 4)"
            )
            return None

        vt_neg = int.from_bytes(data[root_off : root_off + 4], "little", signed=True)
        vt = root_off - vt_neg
        if not (0 <= vt < len(data) - 6):
            Logger().get().debug(f"{vt=} {len(data)=}")
            Logger().get().error(
                "Unexpected vtable index. Expected (0 <= vt < len(data) - 6)"
            )
            return None

        field0_off = int.from_bytes(data[vt + 4 : vt + 6], "little")
        if field0_off > 0 and root_off + field0_off < len(data):
            opcode = data[root_off + field0_off]
            return opcode
        else:
            return None
