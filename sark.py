# -*- coding: utf-8 -*-
"""Sark - Discord Chat Bot

To install prerequisite packages try this::
    $ python3 -m pip install discord.py --user

You can run this bot by supplying a token on the command line or through a
file.
"""
import discord


def setup_client():
    """Initialize the Discord client API and setup triggers"""

    discord_client = discord.Client()

    @discord_client.event
    async def on_ready():  # pylint: disable=unused-variable
        """Once connected you should get a nice debug message"""
        print('We\'re in as')
        print(discord_client.user.name)
        print(discord_client.user.id)
        print(', sweet!')

    @discord_client.event
    async def on_message(message):  # pylint: disable=unused-variable
        """Main trigger entry point. We have a message, now deal with it.

        Args:
            message (str): The message recieved from Discord
        """
        if message.content.startswith('!osticket'):
            await discord_client.send_message(
                message.channel,
                'https://osticket.at.freegeekarkansas.org/')
        elif message.content.startswith('!wiki'):
            await discord_client.send_message(
                message.channel,
                'https://wiki.at.freegeekarkansas.org/')

    return discord_client


def run_sark(discord_client, secret_token):
    """Once initialized and ready for action, run Sark and use the bot.

    Args:
        discord_client = Opaque Discord.Client() object
        secret_token (str) = Secret communications token for the bot

    """
    discord_client.run(secret_token)


def parse_args():
    """Parse the commandline arguments and prepare to chat in Disc!"""
    parser = argparse.ArgumentParser(description='Discord Chat Bot')
    parser.add_argument('-f', '--file',
                        metavar='FILE',
                        help='Configuration file name',
                        default='sark.conf',
                        dest='file')

    parser.add_argument('-t', '--token',
                        metavar='TOKEN',
                        help='API Token (insecure)',
                        default='',
                        dest='token')

    parser.add_argument('-o', '--offline',
                        action='store_true',
                        help='Do not try to connect',
                        default=False,
                        dest='offline')

    parser.add_argument('-l', '--log',
                        metavar='LOGFILE',
                        help='Log file name',
                        default="sark.log",
                        dest='logfile')

    parser.add_argument('-ll', '--loglevel',
                        metavar='LOGLEVEL',
                        help=('Logging level to use valid entries are: '
                              'ERROR, WARNING, [INFO], DEBUG'),
                        default='INFO',
                        dest='loglevel')

    parser.add_argument('-d', '--debug',
                        help='Sets the logging level to DEBUG',
                        action='store_const',
                        const='DEBUG',
                        dest='loglevel')

    args = parser.parse_args()
    args.decodedloglevel = decode_loglevel(args.loglevel)
    return args


def decode_loglevel(string_level):
    """Take an alpha version of the loglevel and return a numeric version.

    Args:
        string_level (str): Hopefully one of the following
            [CRITICAL, ERROR, WARNING, INFO, DEBUG]

    Returns:
        int: Returns a number 1-100 with 1 being the most chatty
    """
    int_level = 0
    folded_str = string_level.casefold()
    if folded_str == 'critical':
        int_level = 50
    elif folded_str == 'error':
        int_level = 40
    elif folded_str == 'warning':
        int_level = 30
    elif folded_str == 'info':
        int_level = 20
    elif folded_str == 'debug':
        int_level = 10
    else:
        int_level = 20  # Default to INFO level

    return int_level


def config_from_file(conf_file):
    """Read the configuration from disk

    Args:
        conf_file (str): configuration file name

    Returns:
        dict: dictionary of configuration items
    """
    import configparser
    config = configparser.ConfigParser()
    config.read(conf_file)
    return config


if __name__ == '__main__':
    import argparse
    import logging
    ARGS = parse_args()
    LOGGER = logging.getLogger('discord')
    LOGGER.setLevel(ARGS.decodedloglevel)
    LOGHANDLER = logging.FileHandler(filename=ARGS.logfile,
                                     encoding='utf-8',
                                     mode='w')

    TOKEN = ARGS.token.strip()
    CLIENT = setup_client()

    if not TOKEN:
        CONFDATA = config_from_file(ARGS.file.strip())
        TOKEN = CONFDATA['DEFAULT']['Token']

    if TOKEN:
        if not ARGS.offline:
            run_sark(CLIENT, TOKEN)
        else:
            print('Token provided, but offline mode was forced.')
    else:
        print('No token provided, try --token or --file to supply one.')
