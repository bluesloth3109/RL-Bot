from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from vec import Vec3


	
class GoalTracker():
	def get_goal_distance(packet: FieldInfoPacket, team, playerlocation):
		info = packet.get_field_info()
		for i in range(info.num_goals):
			goal = info.goals[i]
			if goal.team_num == team:
				target = goal.location
		distance = Vec3.dist(playerlocation, target)
		return distance


	def get_goal_direction(packet: GameTickPacket, team, playerdirection):
		info = packet.get_field_info()
		for i in range(info.num_goals):
			goal = info.goals[i]
			if goal.team_num == team:
				target = goal.direction
		direction = Vec3.ang_to(playerlocation, target)
		return direction

	def middle_of_goal(team):
		if team == 0:
			middle = Vec3(0, -5120, 642.775//2)
		elif team == 1:
			middle = Vec3(0, 5120, 642.775//2)
		return middle

    