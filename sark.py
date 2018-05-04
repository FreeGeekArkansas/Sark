# -*- coding: utf-8 -*-
"""Sark - Discord Chat Bot

To install prerequisite packages try this::
    $ python3 -m pip install discord.py --user

You can run this bot by supplying a token on the command line or through a
file.
"""
import random
from functools import reduce
import discord
from discord.ext import commands


def fold_sum(xs):  # pylint: disable=invalid-name
    """Sum up the elements in the list xs.

    Args:
        xs (list): The items we are about to sum up
    """
    return reduce(lambda x, y: x+y, xs)


def calculate_checksum(bare_code):
    """Calculate the checksum digit for UPC-A and stuff"""
    odds = [bare_code[x] for x in range(1, len(bare_code) - 1, 2)]
    evens = [bare_code[x] for x in range(0, len(bare_code) - 1, 2)]
    odd_sum = fold_sum(odds)
    even_sum = fold_sum(evens)
    spec = ((3 * odd_sum) + even_sum) % 10
    if spec == 0:
        return 0

    return 10 - spec


def gen_barcode_digit(engine):
    """Pick a random number between 0 and 9"""
    return int(engine.triangular(0, 9))


def generate_random_barcode_digits():
    """Generate a set of digits"""
    rand_engine = random.SystemRandom()
    digits = [4, 0, 0, 0, 0, 0]
    for i in range(5):  # pylint: disable=unused-variable
        digits.append(gen_barcode_digit(rand_engine))

    digits.append(calculate_checksum(digits[0:10]))
    return '{}{}{}{}{}{}{}{}{}{}{}{}'.format(
        digits[0], digits[1], digits[2], digits[3],
        digits[4], digits[5], digits[6], digits[7],
        digits[8], digits[9], digits[10], digits[11])


def setup_client(cmd_prefix):
    """Initialize the Discord client API and setup triggers"""

    bot = commands.Bot(command_prefix=cmd_prefix,
                       description='Sark, the (sometimes)helpful bot')

    @bot.event
    async def on_ready():  # pylint: disable=unused-variable
        """Once connected you should get a nice debug message"""
        print('We\'re in as ' + bot.user.name
              + ' id ' + bot.user.id + ', sweet!')

    @bot.command()
    async def wiki():  # pylint: disable=unused-variable
        """Send the URL for the wiki at Free Geek Arkansas."""
        await bot.say(
            embed=discord.Embed(title='Free Geek Arkansas Wiki - Edit Today!',
                                url='https://wiki.at.freegeekarkansas.org')
            )

    @bot.command()
    async def osticket():  # pylint: disable=unused-variable
        """Send the URL for osticket at Free Geek Arkansas."""
        await bot.say(
            embed=discord.Embed(title='Free Geek Arkansas TODO List',
                                url='https://osticket.at.freegeekarkansas.org')
            )

    @bot.command()
    async def barcode():  # pylint: disable=unused-variable
        """Generate a random barcode starting with 400000"""
        await bot.say(generate_random_barcode_digits())

    @bot.command()
    async def info():  # pylint: disable=unused-variable
        """Embed details about this bot into the channel"""
        embed = discord.Embed(title="Sark is a helpful bot",
                              description="Being helpful with no breaks")
        embed.add_field(name="Author", value="Zac Slade")
        embed.add_field(name="GitHub Organization", value="Free Geek Arkansas")
        embed.add_field(name="GitHub Team", value="Dev Heads")
        await bot.say(embed=embed)

    return bot


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
    CONFDATA = config_from_file(ARGS.file.strip())
    CLIENT = setup_client(CONFDATA['DEFAULT']['CmdPrefix'])

    if not TOKEN:
        TOKEN = CONFDATA['DEFAULT']['Token']

    if TOKEN:
        if not ARGS.offline:
            run_sark(CLIENT, TOKEN)
        else:
            print('Token provided, but offline mode was forced.')
    else:
        print('No token provided, try --token or --file to supply one.')
