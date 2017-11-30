import sopel.module

@sopel.module.commands('TestMessage')
def TestMessage(bot, trigger):
    bot.say('test message')
