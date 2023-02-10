from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket,FieldInfoPacket
from util.ball_prediction_analysis import find_slice_at_time
from util.boost_pad_tracker import BoostPadTracker
from util.drive import steer_toward_target
from util.sequence import Sequence, ControlStep
from util.vec import Vec3
from util.target_tracker import middle_of_goal, get_target_direction, get_target_distance
from util.car_flips import begin_front_flip, begin_half_flip, begin_speed_flip
from behaviours import set_behaviour

class WeeNanner(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.active_sequence: Sequence = None
        self.boost_pad_tracker = BoostPadTracker()
    def initialize_agent(self):
        # Set up information about the boost pads now that the game is active and the info is available
        self.boost_pad_tracker.initialize_boosts(self.get_field_info())
        self.initial_gametime = 0
        self.behaviour = "chase_ball" #start chasing ball
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Keep our boost pad info updated with which pads are currently active
        self.boost_pad_tracker.update_boost_status(packet)
        # This is good to keep at the beginning of get_output. It will allow you to continue
        # any sequences that you may have started during a previous call to get_output.
        if self.active_sequence is not None and not self.active_sequence.done:
            controls = self.active_sequence.tick(packet)
            if controls is not None:
                return controls
        ball_prediction = self.get_ball_prediction_struct() 
        #get car
        my_car = packet.game_cars[self.index]
        
        # Check Vector of our teams goal
        my_team = my_car.team
        my_goal = middle_of_goal(my_team)
        enemy_goal = middle_of_goal(1)
        
        #variables
        car_location = Vec3(my_car.physics.location)
        car_velocity = Vec3(my_car.physics.velocity)
        ball_location = Vec3(packet.game_ball.physics.location)
        distance_to_ball = get_target_distance(car_location, ball_location, flat=False) - 92.75
        curr_gametime = int(packet.game_info.seconds_elapsed)
        map_centre = Vec3(0, 0 ,0)
        offside = Vec3.is_closer_to_goal_than(car_location, ball_location, 1)
        target_location = set_behaviour(packet, self.behaviour, car_location, ball_location, my_goal, ball_prediction)
        kickoff = self.kickoff_check(packet)
        
        # Draw some things to help Debug
        self.renderer.draw_string_2d(50, 50, 1, 1,f'Player Co-ords:{car_location}', self.renderer.white())
        self.renderer.draw_string_2d(50, 70, 1, 1, f'Speed: {car_velocity.length():.1f}', self.renderer.white())
        self.renderer.draw_string_2d(50,90, 1, 1, f'Dist. to ball: {distance_to_ball:.1f}', self.renderer.white())
        self.renderer.draw_string_2d(50,110, 1, 1, f'Behaviour: {self.behaviour}', self.renderer.white())
        #self.renderer.draw_string_2d(50,130, 1, 1, f'Ang_to_ball_True: {self.get_target_direction(car_location, ball_location, flat=True)}', self.renderer.white())

        #Draw line to target location and rect on target location
        self.renderer.draw_line_3d(car_location, target_location, self.renderer.white())
        self.renderer.draw_rect_3d(target_location, 8, 8, True, self.renderer.cyan(), centered=True)

        #Draw Goal Locations
        self.renderer.draw_line_3d(car_location, enemy_goal, self.renderer.orange())
        self.renderer.draw_line_3d(car_location, my_goal, self.renderer.blue())
        

        controls = SimpleControllerState()
        controls.steer = steer_toward_target(my_car, set_behaviour(packet, self.behaviour, car_location, ball_location, my_goal, ball_prediction))
        controls.throttle = 1.0


        if packet.game_cars[self.index].boost != 0:
            controls.boost = True

        #INITIATE KICKOFF
        if kickoff == True:
            controls.boost = True
            if 550 < car_velocity.length() < 650:
                begin_speed_flip(packet)    
            if distance_to_ball < 460:
                controls.boost = False
                begin_front_flip(packet)
        

        #FRONT FLIP COOLDOWN TIMER 
        if car_location.dist(ball_location) <= 460 or 750 < car_velocity.length() < 800:
            if car_location[2] < 18.50:   
                if curr_gametime - self.initial_gametime >= 4 :
                    begin_front_flip(packet)
                    self.initial_gametime = curr_gametime

        #do we need to powerslide to turn towards the ball

        #Figure out where the ball is going if we are far away
        elif distance_to_ball >= 1500:
            # self.attack_from_far(packet)
            self.behaviour = "ball_in_future"

        #check if on wall, needs fixed dosent change target location to the cnetre, keeps staying on wall
        elif self.on_wall(car_location) == True:
            self.behaviour = "get_off_wall"
        
        elif Vec3.is_closer_to_goal_than(car_location, ball_location, 1) == True:
            self.behaviour = "defense"

        else:
            self.behaviour = "chase_ball"
        #dont know how else to do a behaviour check in python 3.7 any better, in 3.10 there is a case match statement which would make this 100x quicker.


        return controls #KEEP AT END OF GET_OUTPUT FUNCTION <-- DONT SHOUT AT ME ZEETO <-- SORRY MATE

    def on_wall(self, point):
    #determines if a point is on the wall
        point = Vec3(abs(point[0]),abs(point[1]),abs(point[2]))
        if point[2] > 300:
            if point[0] > 3600 and 4000 > point[1]:
                return True
            elif 900 < point[0] < 3000 and point[1] > 4900:
                return True
            elif point[0] > 2900 and point[1] > 3800 and 7500 < point[0] + point[1] < 8500:
                return True
            else:
                return False
        else:
            return False

    def kickoff_check(self, packet):
            if packet.game_info.is_round_active:
                if packet.game_info.is_kickoff_pause:
                    return True
                else:
                    return False