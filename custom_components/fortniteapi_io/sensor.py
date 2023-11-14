"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.const import CONF_API_KEY, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .fortniteapi_io_python.base import FortniteAPI_IO
from .fortniteapi_io_python.domain import Languages, Mode, Input
from .fortniteapi_io_python.exceptions import UnauthorizedError, UnknownPlayerError

_LOGGER = logging.getLogger(__name__)

DOMAIN = "sensor"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required("player_id"): cv.string,
        vol.Required("game_mode"): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    _LOGGER.info("init sensor")
    name = config.get(CONF_NAME)
    api_key = config.get(CONF_API_KEY)
    player_id = config.get("player_id")
    game_mode = config.get("game_mode")

    fn = FortniteData(name, api_key, player_id, game_mode)

    if not fn:
        _LOGGER.error("Unable to create the fortniteapi.io sensor")
        return

    add_entities([FortniteSensor(hass, fn)], True)


class FortniteSensor(Entity):
    def __init__(self, hass, fn):
        self._hass = hass
        self.data = fn

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{}".format(self.data.name)

    @property
    def state(self):
        """Return the state of the device."""
        return self.data.attr["kills"]

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.data.attr

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "Eliminations"

    def update(self):
        self.data.update_stats()


class FortniteData:
    def __init__(self, name, api_key, player, mode):
        self.name = name
        self.api_key = api_key
        self.player = player
        self.mode = Mode[mode]
        self.stats = None
        self.attr = {}

        try:
            # create the fortnite object
            self.game = FortniteAPI_IO(self.api_key)
            self.fplayer = self.game.player(self.player)
            self.update_stats()
        except:
            pass

    def update_stats(self):
        self.stats = self.fplayer.get_stats(self.mode)
        # _LOGGER.info(self.stats)
        # transform stats into a dict
        self.attr["level"] = self.fplayer.level
        self.attr["name"] = self.fplayer.name
        self.attr["season"] = self.fplayer.season
        self.attr["placetop1"] = self.stats.placetop1
        self.attr["placetop3"] = self.stats.placetop3
        self.attr["placetop5"] = self.stats.placetop5
        self.attr["placetop6"] = self.stats.placetop6
        self.attr["placetop10"] = self.stats.placetop10
        self.attr["placetop12"] = self.stats.placetop12
        self.attr["placetop25"] = self.stats.placetop25
        self.attr["winrate"] = self.stats.winrate
        self.attr["matchesplayed"] = self.stats.matchesplayed
        self.attr["kills"] = self.stats.kills
        self.attr["kd"] = self.stats.kd
        self.attr["minutesplayed"] = self.stats.minutesplayed
        self.attr["playersoutlived"] = self.stats.playersoutlived
        self.attr["score"] = self.stats.score
        self.attr["lastmodified"] = self.stats.lastmodified
        self.attr["id"] = self.player
        self.attr["map"] = self.game.get_current_map()

        self.attr["levelhistory"]["muh"] = "maeh"

    def print_stats(self):
        print(self.stats)
