# WIP

import asyncio
import websockets
import requests
import logging
from pprint import pprint
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

AP_IP = "192.168.1.1"
UI_ADDR = f"http://{AP_IP}"
WEBSOCKET_ADDR = f"ws://{AP_IP}/ws"

CMD_EMPTY = "on-off"
CMD_ON_OFF = "on-off"
CMD_POWER_UP = "power-up"
CMD_POWER_DN = "power-dn"
CMD_TIMER_ON_OFF = "crono-off-on"

STATE_ON_OFF = "ON_OFF"
#  0: ON/OFF status
STATE_LED_ON_OFF = "LED_ON_OFF"
#  1: Thermostate LED status
STATE_LEVEL = "LEVEL"
#  2: Power Level
STATE_THERMO_DESIRED_TEMPERATURE_C = "THERMO_DESIRED_TEMPERATURE_C"
#  3: Desired Temperature Set Point
STATE_THERMOSTAT_TEMPERATURE_C = "THERMOSTAT_TEMPERATURE_C"
#  4: Display probe value (0-255)
STATE_THERMOSTAT_ON_OFF = "THERMOSTAT_ON_OFF"
#  5: Enable probe/thermostatat
STATE_SWITCH_THERMOSTAT_ENABLED = "SWITCH_THERMOSTAT_ENABLED"
#  6: enable thermostate - when enabled, manual level contro is disabled
STATE_SWITCH_TIMER_ENABLED = "SWITCH_TIMER_ENABLED"
#  7: TIMER ON/OFF status
STATE_TIMER_REMAINING_HOURS = "TIMER_REMAINING_HOURS"
#  8: Timer Hours
STATE_TIMER_REMAINING_MINUTES = "TIMER_REMAINING_MINUTES"
#  9: Timer Minutes
STATE_TIMER_REMAINING_SECONDS = "TIMER_REMAINING_SECONDS"
#  10: TImer Seconds
STATE_CASA_ON_OFF = "CASA_ON_OFF"
#  11: Heating ON/OFF Status

KEY_MAP = {
     '0': STATE_ON_OFF,
     '1': STATE_LED_ON_OFF,
     '2': STATE_LEVEL, # f"LIVELLO-{valore}.png"
     '3': STATE_THERMO_DESIRED_TEMPERATURE_C, 
     '4': STATE_THERMOSTAT_TEMPERATURE_C,
     '5': STATE_THERMOSTAT_ON_OFF,
     '6': STATE_SWITCH_THERMOSTAT_ENABLED, 
     '7': STATE_SWITCH_TIMER_ENABLED, 
     '8': STATE_TIMER_REMAINING_HOURS,
     '9': STATE_TIMER_REMAINING_MINUTES,
     '10': STATE_TIMER_REMAINING_SECONDS,
     '11': STATE_CASA_ON_OFF,
}

@dataclass
class HeaterState:
    is_on: bool
    level: int

    def __init__(self, parsed_response):
        self.is_on = bool(parsed_response[STATE_ON_OFF])
        self.level = int(parsed_response[STATE_LEVEL])
        

async def get_state(addr) -> HeaterState:
    return await send_cmd(addr, CMD_EMPTY)

async def send_cmd(addr, cmd) -> HeaterState:
    async with websockets.connect(addr) as websocket:
        await websocket.send(cmd)
        response = str(await websocket.recv())
        logging.info(f"command '{cmd}' > {response}")
        if response.startswith('DT:'):
            parsed_response = parse_response(response)
            state =  HeaterState(parsed_response)
            return state
        logger.error(f"unexpected response: {response}")

def parse_response(response: str) -> "dict[str, str]":
    # e.g. DT:P0=0P1=0P2=0P3=160P4=20P5=0P6=1P7=0P8=0P9=0P10=0P11=0	
    data = response[3:]
    parameters = data.split("P")[1:]
    values = {}
    for param in parameters:
        key, value = param.split("=")
        readable_key = KEY_MAP.get(key, key)
        updated_value = process_response_value(key, value)
        values[readable_key] = updated_value
    # e.g. {"ON_OFF": "1"}
    return values

def process_response_value(key, value):
    if key == "THERMOSTAT_TEMPERATURE_C" or key == "THERMO_DESIRED_TEMPERATURE_C":
        # tempValueF = f"{(((valore - 20) / 2) * 9 / 5) + 32:.1f} °F"#
        return (value - 20) / 2
    
    return value

async def run():
    CMD = CMD_ON_OFF
    CMD = CMD_POWER_DN
    CMD = CMD_POWER_UP
    CMD = ""
    response = await send_cmd(WEBSOCKET_ADDR, CMD)
    # response = await get_state(WEBSOCKET_ADDR)
    logger.info(f"response={response}")


asyncio.run(run())
