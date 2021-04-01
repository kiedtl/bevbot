import dataclasses
import handlers
import out
import random

from common import nohighlight
from typing import *

modname = "tea"

def _flatten(src):
    return [item for sublist in src for item in sublist]


CHANCE_OF_TEA_ADJ = 25
CHANCE_OF_VESSEL_SIZE = 90
CHANCE_OF_VESSEL_ADJ = 85

ACTION = ["hands", "gives", "passes", "serves"]


# some teas can only be in a certain set of containers.
# for instance, hohins will only hold some kind of green tea.
#
# also, some adjectives only fit certain teas.
# example: Kangra => green tea, Irish => black tea
#
# Some teas are only good at a certain temperature (cold butter
# tea is disgusting, to say the least).
#
# because of that, we can't just choose a random tea, adjective,
# and vessel; we need to choose the tea first, then the vessel
# and adjective based on what tea was chosen.
#
# this structure keeps track of what vessels/adjectives can be
# used for each tea.
@dataclasses.dataclass
class Tea:
    name: str
    vessels: List[str]
    adjs: List[str]
    heats: List[List[str]]


# fmt: off

# tea adjectives. brands, places, etc.
#
# Kangra is a location in India where some kinds of green
# tea are produced.
NEWMANS   = "Newman's Own"
EARL      = "Earl Grey"
FAIRTRADE = "fair trade"
ORGANIC   = "organic"
HOMEMADE  = "homemade"
HOMEBREWN = "home-brewn"
KANGRA    = "Kangra"
IRISH     = "Irish-breakfast"
ENGLISH   = "English-breakfast"
DARJEEL   = "Darjeeling"
VANILLA   = "vanilla"
LEMONGRSS = "lemongrass"
HIBISCUS  = "hibiscus"

# Temperature of tea.
COLD = ["iced", "cold", "chilled", "ice cold"]
WARM = ["lukewarm", "warm", "warmish", "room temperature"]
HOT  = ["boiling", "scalding", "steaming", "sweltering", "toasty hot"]
ALL  = _flatten([COLD, WARM, HOT])

# Vessels for tea.
TEAPOT  = ["teapot",  ["vintage", "silver", "English", "antique silver", "jasperware"]]
MUG     = ["mug",     ["stoneware", "porcelain", "jasperware", "wooden", "Indian-made clay mug"]]
BOWL    = ["bowl",    ["burl wood-and-silver tea", "Tibetan tea", "Tibetan silver tea"]]
SAMOVAR = ["samovar", ["antique", "vintage", "brass", "silver"]]
TEACUP  = ["teacup",  ["porcelain"]]
HOHIN   = ["hohin",   []]
GAIWAN  = ["gaiwan",  ["porcelain", "Ruyao"]]
SHIBOR_ = ["shiboridashi",  ["porcelain", "red clay"]]

SIZES = ["large", "small", "medium", "tall", "wide", "big", "100ml",
        "giant", "tiny"]

TEA = "tea" #nohighlight("tea")

TEAS = [
    Tea(f"black {TEA}",                  [SAMOVAR, TEAPOT, MUG, TEACUP],
        [IRISH, ENGLISH, NEWMANS, EARL, DARJEEL], [ALL]),
    Tea(f"green {TEA}",                  [TEAPOT, MUG, HOHIN], [KANGRA], [ALL]),
    Tea(f"matcha green {TEA}",           [HOHIN, TEAPOT, MUG, TEACUP], [], [ALL]),
    Tea(f"sencha green {TEA}",           [SHIBOR_, HOHIN, TEAPOT, MUG, TEACUP], [], [ALL]),
    Tea(f"white {TEA}",                  [TEAPOT, MUG, TEACUP], [EARL], [ALL]),
    Tea(f"oolong {TEA}",                 [TEAPOT, MUG, TEACUP], [], [WARM, HOT]),
    Tea(f"pu'er",                        [SHIBOR_, TEAPOT, MUG, TEACUP], [], [ALL]),
    Tea(f"chai",                         [TEAPOT, MUG, TEACUP], [HOMEMADE], [WARM, HOT]),
    Tea(f"butter {TEA}",                 [TEAPOT, MUG, BOWL, TEACUP], [HOMEMADE], [HOT]),
    Tea(f"christmas {TEA}",              [TEAPOT, MUG, TEACUP], [HOMEMADE], [ALL]),
    Tea(f"rooibos {TEA}",                [TEAPOT, MUG, TEACUP], [], [ALL]),
    Tea(f"tulsi {TEA}",                  [TEAPOT, MUG, TEACUP], [FAIRTRADE], [COLD, HOT]),
    Tea(f"lemonbalm and tulsi {TEA}",    [TEAPOT, MUG, TEACUP], [FAIRTRADE], [COLD, HOT]),
    Tea(f"spearmint {TEA}",              [TEAPOT, MUG], [HOMEMADE], [COLD]),
    Tea(f"peppermint {TEA}",             [TEAPOT, MUG], [HOMEMADE], [COLD]),
    Tea(f"chocolate mint {TEA}",         [TEAPOT, MUG], [HOMEMADE], [COLD]),
    Tea(f"mullein {TEA}",                [MUG], [HOMEMADE], [ALL]),
    Tea(f"lamb's ears {TEA}",            [MUG], [HOMEMADE], [ALL]),
    Tea(f"tumeric ginger {TEA}",         [TEAPOT, MUG, TEACUP], [NEWMANS],  [ALL]),
    Tea(f"lemongrass-verbena {TEA}",     [MUG, TEACUP], [HOMEMADE], [COLD]),
    Tea(f"lemongrass {TEA}",             [MUG, TEACUP], [HOMEMADE], [COLD]),
    Tea(f"black currant hibiscus {TEA}", [MUG, TEACUP], [], [ALL]),
    Tea(f"roasted dandelion root {TEA}", [TEAPOT, MUG, TEACUP], [ORGANIC, HOMEMADE], [ALL]),
    Tea(f"dandelion leaf-and-root {TEA}", [TEAPOT, MUG, TEACUP], [HOMEMADE], [ALL]),
    Tea(f"lavender {TEA}",               [TEAPOT, MUG, TEACUP], [HOMEMADE], [ALL]),
    Tea(f"cinnamon-apple herbal {TEA}",  [TEAPOT, MUG, TEACUP], [ORGANIC], [ALL]),
]

# fmt: on


def _tea():
    tea = random.choice(TEAS)

    heat = random.choice(_flatten(tea.heats))
    vessel_type = random.choice(tea.vessels)
    vessel = vessel_type[0]

    vessel_str = ""
    if random.uniform(0, 100) < CHANCE_OF_VESSEL_ADJ and len(vessel_type[1]) > 0:
        size = ""
        if random.uniform(0, 100) < CHANCE_OF_VESSEL_SIZE:
            size = random.choice(SIZES) + " "

        vessel_adj = random.choice(vessel_type[1])
        vessel_str = f"{size}{vessel_adj} {vessel}"
    else:
        vessel_str = f"{vessel}"

    tea_str = ""
    if random.uniform(0, 100) < CHANCE_OF_TEA_ADJ and len(tea.adjs) > 0:
        tea_adj = random.choice(tea.adjs)
        tea_str = f"{tea_adj} {tea.name}"
    else:
        tea_str = f"{tea.name}"

    filled_with = random.choice(["filled with", "of", "stuffed with",
        "full of", "brimming with"])
    return f"{vessel_str} {filled_with} {heat} {tea_str}"


async def serve(self, ch, src, msg, args, opts):
    """
    :name: tea
    :hook: cmd
    :help: serve some tea!
    :args: @user:str
    """
    recipient = src
    if len(msg) > 0 and len(msg.split()) > 0:
        recipient = msg.split()[0]

    tea = _tea()
    action = random.choice(ACTION)

    await self.ctcp(ch, "ACTION", f"{action} {recipient} a {tea}!")


async def init(self):
    handlers.register(self, modname, serve)
