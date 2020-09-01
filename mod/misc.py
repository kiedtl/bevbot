import common
import config
import out
import random


async def list_mods(self, chan, src, msg):
    mods = ", ".join(sorted(list(self.modules.keys())))
    await out.msg(self, "modules", chan, [f"loaded: {mods}"])


async def ping(self, chan, src, msg):
    res = random.choice(
        ["you rang?", "yes?", "pong!", "what?", "hmmm?", "at your service!"]
    )
    await out.msg(self, "ping", chan, [f"{src}: {res}"])


async def whoami(self, chan, src, msg):
    await out.msg(self, "who", chan, [f"I'm {self.nickname}, kiedtl's bot."])
    await out.msg(self, "who", chan, ["https://github.com/kiedtl/bevbot"])
    await out.msg(self, "who", chan, ["raves and rants: kiedtl‍＠‍tilde.team"])
    await out.msg(self, "who", chan, [f"for usage info, try {config.prefix}help"])


async def init(self):
    self.handle_cmd["modules"] = list_mods
    self.handle_cmd["ping"] = ping
    self.handle_cmd["who"] = whoami

    self.help["modules"] = ["modules - list loaded modules"]
    self.help["ping"] = ["ping - check if I'm responding"]
    self.help["who"] = ["who - get information about my owner"]
