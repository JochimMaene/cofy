from datetime import datetime

from godot.core.tempo import Epoch


def godot_epoch_to_datetime(godot_epoch: Epoch) -> datetime:
    return datetime.fromisoformat(godot_epoch.calStr("UTC")[:-4] + "Z")
