import handlers
import out
import random
from common import nohighlight

modname = "coffee"

ACTION = ["hands", "gives", "passes", "serves"]
ESPRESSO = ["mocha", "latte", "macchiato", "breve", "americano", "cubano", "cappuccino"]
SIZES = ["small", "medium", "short", "tall", "large", "grande", "venti"]
FLAVORS = [
    "hazelnut",
    "white chocolate",
    "dark chocolate",
    "caramel",
    "vanilla",
    "cinnamon",
]
HEAT = ["iced", "cold", "lukewarm", "warm", "hot", "boiling hot", "scalding"]


def _espresso():
    size = random.choice(SIZES)
    heat = random.choice(HEAT)
    flavor = random.choice(FLAVORS)
    coffee = random.choice(ESPRESSO)
    shots = round(random.uniform(1, 3))

    if shots == 1:
        shots_str = "shot"
    else:
        shots_str = "shots"

    espresso = nohighlight("espresso")
    return f"{size} {heat} {flavor} {coffee} with {shots} {shots_str} of {espresso}"


async def serve(self, ch, src, msg, args, opts):
    """
    :name: coffee
    :hook: cmd
    :help: serve some coffee!
    :args: @user:str
    """
    recipient = src
    if len(msg) > 0 and len(msg.split()) > 0:
        recipient = msg.split()[0]

    espresso = _espresso()
    action = random.choice(ACTION)

    await self.ctcp(ch, "ACTION", f"{action} {recipient} a {espresso}!")


async def init(self):
    handlers.register(self, modname, serve)
