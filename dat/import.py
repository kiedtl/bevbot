#!/usr/bin/env python3

import datetime
import dataset
import re
import json

drinks = ['tea', 'coffee']

with open('../dump.users.json') as f:
    users = json.load(f)
db = dataset.connect("sqlite:///drinks.db")

for drink in drinks:
    failure = 0
    success = 0

    print(f'importing {drink}...')

    db.begin()

    contents = ""
    with open(f"/home/kiedtl/etc/weechat/logs/irc.tilde.#{drink}.weechatlog") as f:
        contents = f.read()

    for line in contents.split('\n'):
        if len(line.strip()) < 1:
            continue

        message    = re.split('[\ \t]+', line, 3)[-1]
        date, time = (line.split()[0], line.split()[1])
        _datetime  = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
        nickname   = re.split('[\ \t]+', line)[2]

        if f'{drink}!' in message:
            if not nickname in users:
                failure += 1
                continue
            else:
                success += 1

            db[f'{drink}'].insert(
                dict(
                    nickname=nickname,
                    message=message,
                    username=users[nickname]["username"],
                    identified=users[nickname]["identified"],
                    account=users[nickname]["account"],
                    datetime=_datetime.timestamp()
                )
            )
    db.commit()
    print(f'{success} successes, {failure} failures')
