from __future__ import absolute_import
import sopel.module
import spreadsheetAccess

@sopel.module.commands('welcome','~welcome')
def welcome(bot, trigger):
		if not bot.memory.contains('localStore'):
				bot.memory['localStore'] = [""]
		
		if not trigger.group(2):
				bot.say("No user specified for welcome")
		else:
				if (trigger.group(2) not in bot.memory['localStore']):
						bot.msg(""+trigger.group(2),"Welcome to the parahumans IRC server! #parahumans is the general chat for Wildbow related works. Don't forget to type /rules and check through them!")
						bot.memory['localStore'].append(trigger.group(2))
				else:
						bot.say(trigger.group(2) + " has already been welcomed")
				
'''
@sopel.module.commands('refresh','~refresh')
def refresh(bot, trigger):
        temp = spreadsheetAccess.pullDatabase()
        if temp == 'No data found!':
                bot.say(temp)
        else:
                bot.say("Refresh complete!")
                bot.memory['localStore'] = temp

def getAuthorStories(bot, author):
        string_of_values = author + " has written "
        latestFind = False
        count = 0
        for row in bot.memory['localStore']:
                # Print columns A and B, which correspond to indices 0 and 1.
                if author.lower() == row[0].lower():
                        string_of_values += row[1] + ", "
                        latestFind = row[2]
                        count += 1
        
        string_of_values = string_of_values[:-2] + "."
        
        if count == 0:
                return author + " has authored no fics."
        elif count == 1:
                return string_of_values[:-1] + ": " + latestFind
        return string_of_values         

# Need to make sure there are not reoccurances of the same fic!
def getStoryLink(bot, name):
        line = ""
        
        for row in bot.memory['localStore']:
                # Print columns A and B, which correspond to indices 0 and 1.
                if name.lower() == row[1].lower() and line == "":
                        line = row[1] + " by " + row[0] + ": " + row[2]
                elif name.lower() == row[1].lower() and line != "":
                        bot.say(line)
                        line = row[1] + " by " + row[0] + ": " + row[2]
                        

        if line == "":
                return "Could not find " + name
        else:
                return line
                
@sopel.module.commands('cred')
def cred(bot, trigger):
        if not trigger.group(2):
                bot.say("Please input with name")
        else:
                if not bot.memory.contains('localStore'):
                        refresh(bot,trigger)
                        if not bot.memory.contains('localStore'): return
                bot.say(getAuthorStories(bot, trigger.group(2)))

@sopel.module.commands('link')
def link(bot, trigger):
        if not trigger.group(2):
                bot.say("Please specify fic name")
        else:
                if not bot.memory.contains('localStore'):
                        refresh(bot,trigger)
                if not bot.memory.contains('localStore'): return

                bot.say(getStoryLink(bot, trigger.group(2)))


@sopel.module.commands('sheet')
@sopel.module.commands('credSheet')
def credSheet(bot, trigger):
        bot.say("https://docs.google.com/spreadsheets/d/1I2CTe18qgVsXkO2AS_1i18s7xaDqqVZfwYXbo99UwHY/edit?usp=sharing")

@sopel.module.commands('help')                
def help(bot, trigger):
        bot.say(" ~cred - list an authors fanfics. If there are any missing, " +
                "add them to the sheet (access with ~credSheet).")
        bot.say(" ~link - get the link for a specific fanfiction.")
        bot.say(" ~refresh - get a fresh pull from the spreadsheet.")
'''

