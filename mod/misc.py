# REQUIRE file bin/sysinfo

import config
import common
import random
import handlers

from common import *

async def ping(self, chan, src, msg):
    """
    :name: ping
    :hook: cmd
    :help: check if I'm responding
    :args:
    """
    res = random.choice(
        ["you rang?", "yes?", "pong!", "what?", "hmmm?", "want coffee?"]
    )
    await self.msg("ping", chan, [f"{src}: {res}"])

async def whoami(self, chan, src, msg):
    """
    :name: who
    :hook: cmd
    :help: get information about my owner
    :args:
    """
    response = ""

    owner = common.nohighlight(config.botmaster)
    response += f"I'm {self.nickname}! | owner: {owner} "

    if not config.upstream == None:
        source = "".join([common.nohighlight(i) for i in config.upstream])
        response += f"| source: {source} "

    email = common.nohighlight(config.email[0]) + "‍＠‍" + config.email[1]
    response += f"| contact: {email} | usage: try {config.prefix}help"
    await self.msg("who", chan, [response])

async def init(self):
    handlers.register(self, "ping", ping)
    handlers.register(self, "meta", whoami)
