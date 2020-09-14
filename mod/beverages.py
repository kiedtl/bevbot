import dataset
import datetime
import handlers
import out
from common import nohighlight

modname = "beverages"
drinkdb = dataset.connect("sqlite:///dat/drinks.db")


def bubbles():
    return "・゜゜・。。・゜゜"


def modinfo(ch):
    if ch == "#coffee":
        return ("coffee", "c[~]")
    elif ch == "#tea":
        return ("tea", "[_]b")

    return ("beverages", "c[=]")


def _modname(ch):
    return modinfo(ch)[0]


def trigger(ch):
    return modinfo(ch)[0] + "!"


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
        if not item["nickname"] in stats:
            stats[item["nickname"]] = 0
        stats[item["nickname"]] += 1
        total += 1

    output = ""
    ctr = 0
    until = 7
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
    if not trigger(ch) in msg:
        return

    # don't interact, balun already exists!
    # await out.msg(self, _modname(ch), ch, [response(ch)])
    await record_interaction(ch, self.users[src], src, msg)


async def init(self):
    handlers.register(self, modname, show_drinks)
    handlers.register(self, modname, beverages_up)
