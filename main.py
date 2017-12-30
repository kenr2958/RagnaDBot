#!/usr/bin/env python3
import yaml
import logging
import sys
import discord
import asyncio
import getopt
from lib import load
from lib import tests

# Some ascii art
_welcome ="""
 __  ____      _______    _______             _ version 0.1
|  \/  \ \    / /  __ \  |__   __|           | |
| \  / |\ \  / /| |__) |    | |_ __ __ _  ___| | _____ _ __
| |\/| | \ \/ / |  ___/     | | '__/ _` |/ __| |/ / _ \ '__|
| |  | |  \  /  | |         | | | | (_| | (__|   <  __/ |
|_|  |_|   \/   |_|         |_|_|  \__,_|\___|_|\_\___|_|
By Normynator                           for Ragnarok Online"""

# Config
_log_level = logging.DEBUG
logging.basicConfig(format='%(levelname)s:%(message)s',
                          level=_log_level)
logging.info(" ".join(["Config logging is enabled and set to:",
                         str(_log_level)]))
# Path to the config file
_config = "config.yml"
_client = discord.Client()
_settings = load.load_settings(_config)
_mvp_list = load.parse_mvp_list(_settings['mvp_list'])
# move all loads to other module so it can be used like discord.Client


def parse_mvp_list(path):
    with open(path) as f:
        mvp_list = f.read()
        mvp_list = list(yaml.load_all(mvp_list))
        logging.debug(mvp_list)
        logging.debug(", ".join(str([mvp.name, mvp.info]) for mvp in mvp_list))
    return mvp_list


def parse_args(args):
    opts, args = getopt.getopt(args[1:], "hl:t:")
    for opt, arg in opts:
        if opt == '-h':
            print("MVP Tracker: -h [shows this message], -l <debug, info, warning> [sets the log level]")
            sys.exit(2)
        elif opt == '-l':
            log_type = logging.WARNING
            if arg == 'debug':
                log_type = logging.DEBUG
            elif arg == 'info':
                log_type = logging.INFO
            elif arg == 'warning':
                log_type = logging.WARNING
            logging.basicConfig(format='%(levelname)s:%(message)s', level=log_type)
        elif opt == "-t":
            logging.basicConfig(format='%(levelname)s:%(message)s',
                          level=logging.DEBUG)
            if arg == "mvps":
                logging.debug("Running test: mvps")
                test_mvps()


def get_mvps():
    return ", ".join(str(mvp.name) for mvp in _mvp_list)


@_client.event
async def on_ready():
    logging.debug(" ".join(['Logged in as', _client.user.name,
                            str(_client.user.id)]))


@_client.event
async def on_message(message):
    if message.content.startswith('!echo'):
        await _client.send_message(message.channel, message.content)


def main():
    print(_welcome)
    parse_args(sys.argv)
    #_client.run(settings['token'])


if __name__ == "__main__":
    main()
