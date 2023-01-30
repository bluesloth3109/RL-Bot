from rlbot.utils.structures.game_data_struct import FieldInfoPacket
from vec import Vec3


	

#Returns distance from player to goal as a vector
def get_goal_distance(team, playerlocation, packet: FieldInfoPacket):
	for i in range(packet.num_goals):
		goal = packet.goals[i]
		if goal.team_num == team:
			target = goal.location
	distance = Vec3.dist(playerlocation, target)
	return distance

#Returns direction from player to goal as a vector
def get_goal_direction(packet, team, playerdirection):
	info = packet.get_field_info()
	for i in range(info.num_goals):
		goal = info.goals[i]
		if goal.team_num == team:
			target = goal.direction
	direction = Vec3.ang_to(playerdirection, target)
	return direction

#returns the exact centre of the goal
def middle_of_goal(team):
	if team == 0:
		middle = Vec3(0, -5120, 642.775//2) #blue
		return middle
	elif team == 1:
		middle = Vec3(0, 5120, 642.775//2) #orange
		return middle
class GoalTracker:
	def initialize(self, game_info: FieldInfoPacket):
        raw_boosts = [game_info.boost_pads[i] for i in range(game_info.num_boosts)]
        self.boost_pads: List[BoostPad] = [BoostPad(Vec3(rb.location), rb.is_full_boost, False, 0) for rb in raw_boosts]
        # Cache the list of full boosts since they're commonly requested.
        # They reference the same objects in the boost_pads list.
        self._full_boosts_only: List[BoostPad] = [bp for bp in self.boost_pads if bp.is_full_boost]