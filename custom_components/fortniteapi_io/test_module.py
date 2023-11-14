import os

from fortniteapi_io_python.base import FortniteAPI_IO
from fortniteapi_io_python.domain import Languages, Mode, Input
from fortniteapi_io_python.exceptions import UnauthorizedError, UnknownPlayerError

fortnite = FortniteAPI_IO('c4ed8289-490ff90a-8a1df2ab-2a5e05f6')

account_id = fortnite.get_account_id('ᴾᵒᵗᶻᵇˡⁱᵗᶻ')
# account_id = fortnite.get_account_id('PleasantMat988')
# account_id = fortnite.get_account_id('1Helmut2')
# account_id = fortnite.get_account_id('elli.prdl')
player = fortnite.player(account_id)
print("Account ID: %s" % account_id)
print("Name: %s" % (player.name))
# print(player.muh)
print("Level: %d" % (player.level))
print(player.get_stats(mode=Mode.SQUAD))
print(player.get_level_history())
# print(fortnite.get_current_map(poi=True))