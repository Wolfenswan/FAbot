# -*- coding: utf-8 -*-
import logging
import discord
from commands import commandregex, commands
from event_manager import event_manager


class Client(discord.Client):
    def __init__(self):
        super(Client, self)
        self.channel_whitelist = []
        self.announcement_channels = []
        self.send_welcome_pm = false
        self.make_join_announcment = false
        self.make_leave_announcment = false

main_client = discord.Client()


@main_client.event
def on_ready():
    print('Connected!')
    print('Username: ' + main_client.user.name)
    print('ID: ' + main_client.user.id)
    logging.info("Connected to Discord as %s (ID: %s)", main_client.user.name, main_client.user.id)


@main_client.event
def on_message(message):
    if message.content[0] == "!":
        if len(main_client.channel_whitelist) > 0 and message.channel.id not in main_client.channel_whitelist:
            return

        logging.info("#%s (%s) : %s", message.channel.name, message.author.name, message.content)
        event_manager.handle_message(main_client)
        cmdline = commandregex.search(message.content.lower())
        logging.debug("Command : %s(%s)", cmdline.group('command'), cmdline.group('args'))
        if cmdline.group('command') in commands:
            msg = commands[cmdline.group('command')](message, cmdline.group('args'))
            if msg is not None:
                main_client.send_message(message.channel, msg)

@main_client.event
def on_member_join(member):
    if main_client.send_welcome_pm:
        welcome_pm = open('welcome_pm.txt')
        main_client.send_message(member, welcome_pm.read())
    if main_client.make_join_announcment:
        for channel in main_client.announcement_channels:
            main_client.send_message(main_client.get_channel(channel), member.name + " joined the server")

@main_client.event
def on_member_remove(member):
    if main_client.make_leave_announcment:
        for channel in main_client.announcement_channels:
            main_client.send_message(main_client.get_channel(channel), member.name + " left the server")
