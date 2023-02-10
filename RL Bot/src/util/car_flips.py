from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket,FieldInfoPacket
from util.sequence import Sequence, ControlStep

def begin_front_flip(packet):

        # Send some quickchat just for fun
        # Do a front flip. We will be committed to this for a few seconds and the bot will ignore other
        # logic during that time because we are setting the active_sequence.
    active_sequence = Sequence([
        ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
        ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
        ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, pitch=-1)),
        ControlStep(duration=0.8, controls=SimpleControllerState()),
    ])

    # Return the controls associated with the beginning of the sequence so we can start right away.
    return active_sequence.tick(packet)  

def begin_half_flip(packet):
    active_sequence = Sequence([
        ControlStep(duration=0.12, controls=SimpleControllerState(jump=True)),
        ControlStep(duration=0.0001, controls=SimpleControllerState(jump=False)),
        ControlStep(duration=0.09, controls=SimpleControllerState(jump=True, pitch=1)), #backflip
        ControlStep(duration=0.4, controls=SimpleControllerState(jump=False, pitch=-1)), #cancel flip
        #Adjust duration so it lands well
        ControlStep(duration=1.4, controls=SimpleControllerState(jump=False, roll=1, boost=True)), #airrollround
        ControlStep(duration=0.5, controls=SimpleControllerState(boost=True)),

        ControlStep(duration=0.8, controls=SimpleControllerState()),

    ])
    return active_sequence.tick(packet)

def begin_speed_flip(packet):  
    active_sequence = Sequence([
        ControlStep(duration=0.15, controls=SimpleControllerState(steer=1, boost=True)),
        ControlStep(duration=0.05, controls=SimpleControllerState(jump=True, boost=True)),
        ControlStep(duration=0.05, controls=SimpleControllerState(jump=False, boost=True, handbrake=True)),
        ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, roll=-1, boost=True, handbrake=True)),
        ControlStep(duration=0.15, controls=SimpleControllerState(jump=False, boost=True, handbrake=True)),
        ControlStep(duration=0.40, controls=SimpleControllerState(boost=True, handbrake=True, yaw=-1)),
    ])

    return active_sequence.tick(packet)