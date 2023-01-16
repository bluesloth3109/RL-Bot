import math

from rlbot.utils.structures.game_data_struct import PlayerInfo

from util.orientation import Orientation, relative_location
from util.vec import Vec3


def limit_to_safe_range(value: float) -> float:
    if value < -1:
        return -1
    if value > 1:
        return 1
    return value


def steer_toward_target(car: PlayerInfo, target: Vec3) -> float:
    relative = relative_location(Vec3(car.physics.location), Orientation(car.physics.rotation), target)
    angle = math.atan2(relative.y, relative.x)
    return limit_to_safe_range(angle * 5)
