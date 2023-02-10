from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket,FieldInfoPacket
from util.vec import Vec3
from util.ball_prediction_analysis import find_slice_at_time

def set_behaviour(packet, command, car, ball, my_goal, ball_prediction):
    
    if command == "get_off_wall":
        return Vec3(car[0], car[1], 0)

    elif command == "ball_in_future":
          # This can predict bounces, etc
        ball_in_future = find_slice_at_time(ball_prediction, packet.game_info.seconds_elapsed + 1)

        # ball_in_future might be None if we don't have an adequate ball prediction right now, like during
        # replays, so check it to avoid errors.
        if ball_in_future is not None:
            return Vec3(ball_in_future.physics.location)
        else:
            pass

    elif command == "defense":
        return Vec3(car[0], my_goal[1], car[2])

    elif command == "chase_ball":
        return ball
    
    else:
        return ball