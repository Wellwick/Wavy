from __future__ import absolute_import
import sopel.module
import unicodedata
#import spreadsheetAccess

# Welcomes new users to chat
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



# Goal is to provide an anonymous way to talk to moderators
@sopel.module.commands('report','~report')
def report(bot, trigger):
		if not bot.memory.contains('reports'):
				initaliseReporting(bot)
		
		if not trigger.group(2):
				bot.say("Please specify something to report")
		else:
				bot.msg(trigger.nick, "Thanks for reporting and making the community a better place! Make sure to include pastebins/timestamps where possible to make moderating as quick as possible.")
				if trigger.hostmask in bot.memory['blacklist']:
						addBlacklistReport(bot,trigger)
						return
				bot.msg("#moderation", "Anonymous Report from ID #" + getUser(bot,trigger) + " '" + trigger.group(2) + "' ")
				addReport(bot,trigger)


# Gets the user ID from the list
def getUser(bot,trigger):
	if not trigger.hostmask in bot.memory['reports']:
		#need to add the user
		bot.memory['reports'][trigger.hostmask] = [str(bot.memory['reporterCount']), []]
		bot.memory['reporterCount'] += 1
	
	return bot.memory['reports'][trigger.hostmask][0]
		

# Adds the report to the bots report memory
def addReport(bot,trigger):
	bot.memory['reports'][trigger.hostmask][1].append(trigger.group(2))

# Adds a blacklist report
def addBlacklistReport(bot, trigger):
	bot.memory['blacklistReports'].append(trigger.group(2))
	bot.memory['missedReports'] += 1

	
# Provide information on usable commands
@sopel.module.commands('help','~help')
def help(bot, trigger):
		if not trigger.group(2):
				bot.msg(trigger.nick, "List of commands: welcome, report, help")
				bot.msg(trigger.nick, "To get description of a command, use ~help <command>")
		else:
				options = {	'welcome' 	: "Use ~welcome <username> to welcome a new user",
							'report'	: "Use ~report <moderation request>. This will alert the mods anonymously. If possible, please log the incident using pastebin or the like. If not, please give a timestamp so the mods can go through the logs for it.",
							'help'		: "Use ~help <command> to get information on a commands usage"
						  }
				if trigger.group(2) in options:
						bot.msg(trigger.nick, options[trigger.group(2)])
				else:
						bot.msg(trigger.nick, trigger.group(2) + " is not a recognised command")
				

# Blacklist an id so a nickname can no longer report
@sopel.module.commands('blacklist','~blacklist')
def blacklist(bot, trigger):
		if trigger.sender == "#moderation" and trigger.group(2) and trigger.admin:
				for hostname, user in bot.memory['reports'].items():
						if str(user[0]) == trigger.group(2):
								bot.memory['blacklist'].append(hostname)
								bot.say("User ID #" + str(user[0]) + " successfully blacklisted. All reports they make will go to ~missedReports.")
				


# Shows 3 most recent reports from <ID>
@sopel.module.commands('recentReports','~recentReports')
def recentReports(bot,trigger):
		if not bot.memory.contains('reports'):
				initaliseReporting(bot)
		
		if trigger.sender == "#moderation" and trigger.group(2) and trigger.admin:
				for hostname, user in bot.memory['reports'].items():
						if str(user[0]) == trigger.group(2):
								bot.say("User " + str(user[0]) + " has reported " + str(user[1][-3:]))
								return
				
				bot.say("Can not find user with ID " + trigger.group(2))



# Returns missed reports from blacklisted users
@sopel.module.commands('missedReports','~missedReports')
def missedReports(bot,trigger):
		if not bot.memory.contains('reports'):
				initaliseReporting(bot)
		
		if trigger.sender == "#moderation" and trigger.admin:
			if trigger.group(2):
				if is_number(trigger.group(2)):
					if unicodedata.numeric(trigger.group(2)) > 0:
						bot.say(str(bot.memory['blacklistReports'][-unicodedata.numeric(trigger.group(2)):]))
					else:
						bot.say("Please specify a value greater than 0")
				else:
					if trigger.group(2) == "ALL":
						bot.say("Showing all missed reports: " + str(bot.memory['blacklistReports']))
					else:
						bot.say("Specify how many recent reports you want to collect")
			else:
				if bot.memory['missedReports'] == 0:
					bot.say("There are no missed reports")
				else:
					bot.say("Recently missed reports: " + str(bot.memory['blacklistReports'][-(bot.memory['missedReports']):]))
					bot.memory['missedReports'] = 0

# Method to initialise reporting functionality
def initaliseReporting(bot):
		bot.memory['reporterCount'] = 1
		bot.memory['reports'] = { "NullTest" : [str(bot.memory['reporterCount']), ["Report 1", "Report 2"]] }
		bot.memory['reporterCount'] += 1
		bot.memory['blacklist'] = []
		bot.memory['blacklistReports'] = []
		bot.memory['missedReports'] = 0
		
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		pass
 
	try:
		import unicodedata
		unicodedata.numeric(s)
		return True
	except (TypeError, ValueError):
		pass
 
	return False

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

