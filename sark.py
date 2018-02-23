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
    parser.add_argument('--file')
    parser.add_argument('--token')
    parser.add_argument('--offline')
    return parser.parse_args()


if __name__ == '__main__':
    import argparse
    ARGS = parse_args()
    TOKEN = ARGS.token.strip()
    CLIENT = setup_client()

    if not TOKEN:
        TOKEN = ARGS.file.strip()

    if TOKEN:
        if not ARGS.offline:
            run_sark(CLIENT, TOKEN)
        else:
            print('Token provided, but offline mode was forced.')
    else:
        print('No token provided, try --token or --file to supply one.')
