from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.structures.game_data_struct import GameTickPacket,FieldInfoPacket
import time

from util.ball_prediction_analysis import find_slice_at_time
from util.boost_pad_tracker import BoostPadTracker
from util.drive import steer_toward_target
from util.sequence import Sequence, ControlStep
from util.vec import Vec3


class WeeNanner(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.active_sequence: Sequence = None
        self.boost_pad_tracker = BoostPadTracker()
    def initialize_agent(self):
        # Set up information about the boost pads now that the game is active and the info is available
        self.boost_pad_tracker.initialize_boosts(self.get_field_info())
        self.initial_gametime = 0
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Keep our boost pad info updated with which pads are currently active
        self.boost_pad_tracker.update_boost_status(packet)
        # This is good to keep at the beginning of get_output. It will allow you to continue
        # any sequences that you may have started during a previous call to get_output.
        if self.active_sequence is not None and not self.active_sequence.done:
            controls = self.active_sequence.tick(packet)
            if controls is not None:
                return controls

        #get car
        my_car = packet.game_cars[self.index]
        
        # Check Vector of our teams goal
        my_team = my_car.team
        if my_team == 0:
            my_goal = Vec3(0, -5120, 642.775//2)
            foe_goal =Vec3(0, 5120, 642.775//2)
        elif my_team == 1:
            my_goal =Vec3(0, 5120, 642.775//2)
            foe_goal = Vec3(0, -5120, 642.775//2)
        
        #variables
        car_location = Vec3(my_car.physics.location)
        car_velocity = Vec3(my_car.physics.velocity)
        ball_location = Vec3(packet.game_ball.physics.location)
        distance_to_ball = self.get_target_distance(car_location, ball_location, flat=False) - 92.75
        distance_to_ball_flat = self.get_target_distance(car_location, ball_location, flat=True) - 92.75
        curr_gametime = int(packet.game_info.seconds_elapsed)
        map_centre = Vec3(0, 0 ,0)


        # By default we will chase the ball
        target_location = ball_location
        if car_location.dist(ball_location) > 1500:
            # self.attack_from_far(packet)
            # We're far away from the ball, let's try to lead it a little bit
            ball_prediction = self.get_ball_prediction_struct()  # This can predict bounces, etc
            ball_in_future = find_slice_at_time(ball_prediction, packet.game_info.seconds_elapsed + 2)

            # ball_in_future might be None if we don't have an adequate ball prediction right now, like during
            # replays, so check it to avoid errors.
            if ball_in_future is not None:
                target_location = Vec3(ball_in_future.physics.location)
                self.renderer.draw_line_3d(ball_location, target_location, self.renderer.cyan())
        
        # Draw some things to help understand what the bot is thinking
        self.renderer.draw_line_3d(car_location, target_location, self.renderer.white())
        self.renderer.draw_string_2d(50, 50, 1, 1,f'Player Co-ords:{car_location}', self.renderer.white())
        self.renderer.draw_string_2d(50, 70, 1, 1, f'Speed: {car_velocity.length():.1f}', self.renderer.white())
        self.renderer.draw_string_2d(50,90, 1, 1, f'Dist. to ball: {distance_to_ball:.1f}', self.renderer.white())
        self.renderer.draw_rect_3d(target_location, 8, 8, True, self.renderer.cyan(), centered=True)

        self.renderer.draw_line_3d(car_location, foe_goal, self.renderer.orange())
        self.renderer.draw_line_3d(car_location, my_goal, self.renderer.blue())
        
        if 750 < car_velocity.length() < 800:
            return self.begin_front_flip(packet)

        controls = SimpleControllerState()
        controls.steer = steer_toward_target(my_car, target_location)
        controls.throttle = 1.0


        if packet.game_cars[self.index].boost != 0:
            controls.boost = True

        #INITIATE KICKOFF
        if packet.game_info.is_round_active:
            if packet.game_info.is_kickoff_pause:
                controls.boost = True
                if 550 < car_velocity.length() < 650:
                    return self.begin_speed_flip(packet)
                if distance_to_ball < 460:
                    controls.boost = False
                    return self.begin_front_flip(packet)
        
        #check if on wall, needs fixed dosent change target location to the cnetre, keeps staying on wall
        if car_location[0] >= 4000 or car_location[0] <= -4000:
            target_location = map_centre
            print("onwall", curr_gametime)
        elif car_location[1] >= 5080 or car_location[1] <= -5080:
            target_location = map_centre
            print("onwall", curr_gametime)
        else:
            target_location = ball_location

        #FRONT FLIP COOLDOWN TIMER
        if car_location.dist(ball_location) <= 460:
            if curr_gametime - self.initial_gametime >= 4 :
               self.begin_front_flip(packet)
               self.initial_gametime = curr_gametime


        
        return controls #KEEP AT END OF GET_OUTPUT FUNCTION <-- DONT SHOUT AT ME ZEETO
    	
        
    def get_target_distance(self, playerlocation, target, flat):
        #Returns distance from player to target as a vector, can be a flat 2d vector
            distance = Vec3.dist(playerlocation, target)
            if flat == True:
                flatdistance1 = Vec3.flat(playerlocation)
                flatdistance2 = Vec3.flat(target)
                flatdistanceval = Vec3.dist(flatdistance1, flatdistance2)
                return flatdistanceval
            else:
                return distance
    def get_target_direction(self, playerlocation, target, flat):
        #Returns direction from player to target as a vector, can be a flat 2d vector
            direction = Vec3.ang_to(playerlocation, target)
            if flat == True:
                flatdirection1 = Vec3.flat(playerlocation)
                flatdirection2 = Vec3.flat(target)
                flatdirectionang = Vec3.ang_to(flatdirection1, flatdirection2)
                return flatdirectionang
            else:
                return direction

    def begin_front_flip(self, packet):

        # Send some quickchat just for fun
        # Do a front flip. We will be committed to this for a few seconds and the bot will ignore other
        # logic during that time because we are setting the active_sequence.
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, pitch=-1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        # Return the controls associated with the beginning of the sequence so we can start right away.
        return self.active_sequence.tick(packet)  
    def begin_half_flip(self, packet):
        self.active_sequence = Sequence([
            ControlStep(duration=0.12, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.0001, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.09, controls=SimpleControllerState(jump=True, pitch=1)), #backflip
            ControlStep(duration=0.4, controls=SimpleControllerState(jump=False, pitch=-1)), #cancel flip
            #Adjust duration so it lands well
            ControlStep(duration=1.4, controls=SimpleControllerState(jump=False, roll=1, boost=True)), #airrollround
            ControlStep(duration=0.5, controls=SimpleControllerState(boost=True)),

            ControlStep(duration=0.8, controls=SimpleControllerState()),

        ])
        return self.active_sequence.tick(packet)
    def begin_speed_flip(self, packet):  
        self.active_sequence = Sequence([
            ControlStep(duration=0.15, controls=SimpleControllerState(steer=1, boost=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True, boost=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False, boost=True, handbrake=True)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, roll=-1, boost=True, handbrake=True)),
            ControlStep(duration=0.15, controls=SimpleControllerState(jump=False, boost=True, handbrake=True)),
            ControlStep(duration=0.40, controls=SimpleControllerState(boost=True, handbrake=True, yaw=-1)),
        ])

        return self.active_sequence.tick(packet)