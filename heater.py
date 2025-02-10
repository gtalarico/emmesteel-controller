# WIP

import asyncio
import websockets
from websockets.sync.client import connect
from pprint import pprint

# TODO: add code to detect/verify we are connecting successfully
# e.g. can load the captive portal HTML by checking content or redirect

AP_IP = "192.168.1.1"
WEBSOCKET_ADDR = f"ws://{AP_IP}/ws"

CMD_ON_OFF = "on-off"
CMD_POWER_UP = "power-up"
CMD_POWER_DN = "power-dn"
CMD_CRONO = "crono-off-on"
# CMD_TEMP_SLIDER = websocket.send('tempSlider'+element);

#  0: display button ON/OFF status
#  1: display chronothermostat status
#  2: display power level
#  3: display desired temperature setpoint
#  4: display probe value (0-255)
#  5: enable probe
#  6: enable chronothermostat function
#  7: display TIMER ON/OFF status
#  8: display timer hours
#  9: display timer minutes
#  10: display timer seconds
#  11: display heating ON/OFF status
KEY_MAP = {
     '0': "ON_OFF",
     '1': "LED_ON_OFF",
     '2': "LEVEL", # f"LIVELLO-{valore}.png"
     '3': "TEMP_SLIDER", 
     # elements["tempValue"] = f"{(valore - 20) / 2} °C"
     # elements["tempValueF"] = f"{(((valore - 20) / 2) * 9 / 5) + 32:.1f} °F"#
     '4': "TEMP",
     '5': "termoregolazione",
     '6': "switch2",
     '7': "switch1",
     '8': "HOUR",
     # elements["ore"] = f"{valore:'02d'} : " if elements.get("switch1", False) else "- "
     '9': "MINUTE",
     '10': "SECOND",
     '11': "CASA_ON_OFF",
}

async def send_cmd(addr, cmd):
    async with websockets.connect(addr) as websocket:
        await websocket.send(cmd)
        response = await websocket.recv()
        parse_response(str(response))

def parse_response(response: str):
    data = response[3:]
    parameters = data.split("P")[1:]
    print(parameters)
    values = {}
    for param in parameters:
        print(param)
        key, value = param.split("=")
        readable_key = KEY_MAP[key]
        values[readable_key] = value
    pprint(values)

# Tests
asyncio.run(send_cmd(WEBSOCKET_ADDR, CMD_ON_OFF))
# asyncio.run(send_cmd(WEBSOCKET_ADDR, CMD_POWER_UP))
# asyncio.run(send_cmd(WEBSOCKET_ADDR, CMD_POWER_DN))
