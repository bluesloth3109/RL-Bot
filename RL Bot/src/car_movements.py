from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.structures.game_data_struct import GameTickPacket
from util.ball_prediction_analysis import find_slice_at_time
from util.boost_pad_tracker import BoostPadTracker
from util.drive import steer_toward_target
from util.sequence import Sequence, ControlStep
from util.vec import Vec3
    
    
def begin_front_flip(self, packet):
        # Send some quickchat just for fun
        self.send_quick_chat(team_only=False, quick_chat=QuickChatSelection.Information_IGotIt)

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

# Back flip code
def begin_back_flip(self, packet):
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            # FIXME 
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, pitch=1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        return self.active_sequence.tick(packet)

# Side flip left 
def begin_side_flip_left(self, packet):
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, roll=-1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        return self.active_sequence.tick(packet)

# Side flip right 
def begin_side_flip_right(self, packet):
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, roll=1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        return self.active_sequence.tick(packet)

# Diagonal flip forward right
def begin_diagonal_flip_forwards_right(self, packet):
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, roll=1, pitch = -1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        return self.active_sequence.tick(packet)

# Diagonal flip forward left
def begin_diagonal_flip_forwards_left(self, packet):
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, roll=-1, pitch = -1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        return self.active_sequence.tick(packet)

# Diagonal flip backwards right
def begin_diagonal_flip_backwards_right(self, packet):
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, roll=1, pitch = 1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        return self.active_sequence.tick(packet)

# Diagonal flip backwards left
def begin_diagonal_flip_backwards_left(self, packet):
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, roll=-1, pitch = 1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        return self.active_sequence.tick(packet)
