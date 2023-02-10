from util.vec import Vec3


	

#Returns distance from player to target as a vector, can be a flat 2d vector
def get_target_distance(playerlocation, target, flat):
		distance = Vec3.dist(playerlocation, target)
		if flat == True:
			flatdistance1 = Vec3.flat(playerlocation)
			flatdistance2 = Vec3.flat(target)
			flatdistanceval = Vec3.dist(flatdistance1, flatdistance2)
			return flatdistanceval
		else:
			return distance

#Returns direction from player to target as a vector, can be a flat 2d vector
def get_target_direction(playerlocation, target, flat):
		direction = Vec3.ang_to(playerlocation, target)
		if flat == True:
			flatdirection1 = Vec3.flat(playerlocation)
			flatdirection2 = Vec3.flat(target)
			flatdirectionang = Vec3.ang_to(flatdirection1, flatdirection2)
			return flatdirectionang
		else:
			return direction

#returns the exact centre of the goal
def middle_of_goal(team):
	if team == 0:
		middle = Vec3(0, -5120, 642.775//2) #blue
		return middle
	elif team == 1:
		middle = Vec3(0, 5120, 642.775//2) #orange
		return middle