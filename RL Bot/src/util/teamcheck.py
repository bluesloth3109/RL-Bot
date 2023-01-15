from rlbot.utils.structures.game_data_struct import GameTickPacket
from util.vec import Vec3


def check_team(packet:GameTickPacket,team):
    team_setup = packet.game_cars[team]

    if team_setup == 0:
        my_goal_mid = Vec3(0, -5120, 642.775//2)
        opp_goal_mid = Vec3(0, 5120, 642.775//2)  
   
    elif team_setup == 1:
        my_goal_mid = Vec3(0, 5120, 642.775//2)
        opp_goal_mid = Vec3(0, -5120, 642.775//2)

    return(my_goal_mid, opp_goal_mid)