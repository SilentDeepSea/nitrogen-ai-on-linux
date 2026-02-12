import time
import psutil
import mss
import pywinctl as pwc
import vgamepad as vg
from gymnasium import Env
from gymnasium.spaces import Box, Dict, Discrete
from PIL import Image

class GamepadEnv(Env):
    def __init__(self, game, image_height=1440, image_width=2560, controller_type="xbox", env_fps=10, **kwargs):
        super().__init__()
        self.os_name = "linux"
        self.image_height, self.image_width, self.env_fps = int(image_height), int(image_width), env_fps
        self.gamepad_emulator = vg.VX360Gamepad() if controller_type == "xbox" else vg.VDS4Gamepad()
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]
        
        self.observation_space = Box(low=0, high=255, shape=(self.image_height, self.image_width, 3), dtype="uint8")
        self.action_space = Dict({"SOUTH": Discrete(2), "AXIS_LEFTX": Box(low=-32768, high=32767, shape=(1,))})

    def pause(self): pass
    def unpause(self): pass

    def step(self, action):
        self.gamepad_emulator.reset()
        if "SOUTH" in action and action["SOUTH"] > 0.5:
            self.gamepad_emulator.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        if "AXIS_LEFTX" in action:
            self.gamepad_emulator.left_joystick(x_value=int(action["AXIS_LEFTX"][0]), y_value=0)
        self.gamepad_emulator.update()
        time.sleep(1.0 / self.env_fps)
        return self.render(), 0.0, False, False, {}

    def render(self):
        sct_img = self.sct.grab(self.monitor)
        # BGRX to RGB conversion is vital for model accuracy
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img.resize((self.image_width, self.image_height))

    def reset(self, seed=None, options=None):
        self.gamepad_emulator.reset()
        return self.render(), {}
