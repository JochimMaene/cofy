from typing import Any

import msgspec


class BaseStruct(msgspec.Struct, tag=True):
    def to_dict(self) -> dict[str, Any]:
        return {f: getattr(self, f) for f in self.__struct_fields__ if getattr(self, f, None) != msgspec.UNSET}


class CamelizedBaseStruct(BaseStruct, rename="camel", tag=True):
    """Camelized Base Struct"""


class Message(CamelizedBaseStruct):
    message: str
