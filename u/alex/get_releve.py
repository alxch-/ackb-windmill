import os
import wmill
from homeassistant_api import Client

# You can import any PyPi package. 
# See here for more info: https://www.windmill.dev/docs/advanced/dependencies_in_python

# you can use typed resources by doing a type alias to dict
#postgresql = dict

def main() -> int:
    client = Client("http://host.docker.internal:8123/api", wmill.get_variable("u/alex/hass_api_key"))
    zlinky_energie = client.get_entity(entity_id="sensor.zlinky_easf01")
    state = zlinky_energie.get_state() 
    releve = int(float(state.state))
    return releve
