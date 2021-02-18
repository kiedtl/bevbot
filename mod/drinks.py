import dataset
import datetime
import handlers
import random
import out
from common import nohighlight

modname = "drinks"
drinkdb = dataset.connect("sqlite:///dat/drinks.db")

SINGLE_WAVE_LEN = 8
WAVES = "・゜゜・。。・゜゜・。。・゜゜・。。・゜゜・。。"


def bubbles():
    index = round(random.uniform(0, (len(WAVES) - SINGLE_WAVE_LEN) - 1))
    return WAVES[index : (index + SINGLE_WAVE_LEN)]


def modinfo(ch):
    if ch == "#coffee":
        return ("coffee", "c[~]", ["coffee!", "latte!", "espresso!"])
    elif ch == "#tea":
        return ("tea", "[_]b", ["tea!", "chai!", "matcha!"])

    return ("drinks", "c[~]", ["drinks!"])


def _modname(ch):
    return modinfo(ch)[0]


def triggers(ch):
    return modinfo(ch)[2]


def response(ch):
    return bubbles() + " " + modinfo(ch)[1] + " " + modinfo(ch)[0].upper() + " UP!"


async def record_interaction(ch, usrinfo, nick, msg):
    drinkdb[ch[1:]].insert(
        dict(
            nickname=nick,
            message=msg,
            account=usrinfo["account"],
            username=usrinfo["username"],
            identified=usrinfo["identified"],
            datetime=datetime.datetime.now().timestamp(),
        )
    )


async def show_drinks(self, ch, src, msg, args, opts):
    """
    :name: drinks
    :hook: cmd
    :help: list commands or show help on command
    :args: @beverage:str
    :aliases: stats
    """
    chan = ch
    if len(msg) > 0:
        chan = msg.split()[0]
    if chan[0] == "#":
        chan = chan[1:]

    query = modinfo(f"#{chan}")[0]
    total = 0
    stats = {}
    for item in list(drinkdb[chan].find()):
        # use account, falling back to nickname
        # if the user wasn't registered
        identifier = item["account"] or item["nickname"]

        if not identifier in stats:
            stats[identifier] = 0
        stats[identifier] += 1
        total += 1

    output = ""
    ctr = 0
    until = 8
    for i in sorted(stats.items(), key=lambda i: i[1], reverse=True):
        if ctr == until:
            break
        percentage = (i[1] * 100) / total
        output += "{} (×{}, {:.0f}%), ".format(nohighlight(i[0]), i[1], percentage)
        ctr += 1

    output = output[:-2]  # trim ', '
    await out.msg(self, _modname(ch), ch, [f"top {query} drinkers: {output}"])


async def beverages_up(self, ch, src, msg):
    """
    :name: beverages_up
    :hook: raw
    """

    msg = msg.lower()
    has_trigger = False
    _triggers = triggers(ch)
    for trigger in _triggers:
        if trigger in msg:
            has_trigger = True
    if not has_trigger:
        return

    # don't interact, balun already exists!
    # await out.msg(self, _modname(ch), ch, [response(ch)])
    await record_interaction(ch, self.users[src], src, msg)


async def init(self):
    handlers.register(self, modname, show_drinks)
    handlers.register(self, modname, beverages_up)
