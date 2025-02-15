""" Emmesteel API Controller"""

import asyncio
import websockets
import logging
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional, Dict

from .constants import CMD_EMPTY, CMD_ON_OFF,  CMD_POWER_DN, CMD_POWER_UP
from .constants import STATE_LEVEL, STATE_ON_OFF
from .constants import KEY_MAP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class State:
    """ State of the Emmesteel Device"""
    is_on: Optional[bool] = None
    level: Optional[int] = None
    _raw: Optional[str] = None
    _state: Optional[Dict] = None

    def __init__(self, raw_state:str=''):
        self._raw = raw_state
        self._state = {}
        if raw_state:
            self._state = state_dict = self.parse_response(raw_state)
            self.is_on = bool(int(state_dict[STATE_ON_OFF]))
            self.level = int(state_dict[STATE_LEVEL])
            

    @staticmethod
    def parse_response(raw_state: str) -> "dict[str, str]":
        # e.g. DT:P0=0P1=0P2=0P3=160P4=20P5=0P6=1P7=0P8=0P9=0P10=0P11=0	
        data = raw_state[3:]
        parameters = data.split("P")[1:]
        values = {}
        for param in parameters:
            key, value = param.split("=")
            readable_key = KEY_MAP.get(key, key)
            values[readable_key] = value
        # e.g. {"ON_OFF": "1"}
        return values
    
    def is_empty(self):
        return self._raw == ""
        
class EmmesteelApi:
    """ Emmesteel Api"""
    def __init__(self, host):
        self.host = host
        self.ui = f"http://{host}"
        self._websocket_addr = f"ws://{host}/ws"
    
    async def get_state(self) -> 'State':
        return await self.send_cmd(CMD_EMPTY)

    async def send_cmd(self, cmd) -> 'State':
        async with websockets.connect(self._websocket_addr) as websocket:
            await websocket.send(cmd)
            response = str(await websocket.recv())
            logging.info(f"command '{cmd}' > {response}")
            if response.startswith('DT:'):
                return State(response)
            logger.error(f"unexpected response: {response}")
            return State()

# TODO - delete
async def test():
    PI_PROXY = "192.168.50.100"
    AP_IP = PI_PROXY
    controller = EmmesteelApi(AP_IP)
    CMD = CMD_POWER_UP
    CMD = CMD_ON_OFF
    # response = await controller.send_cmd(CMD)
    response = await controller.get_state()
    logger.info(f"response={response}")

asyncio.run(test())
