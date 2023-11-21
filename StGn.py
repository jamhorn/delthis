import random #used to generate a random number
import os
import requests #used to make webrequests AKA to send a message
import configparser #used to load date from a config file
import time
import validators
import datetime

def WriteToLogFile(data):
    print(data)
    today = datetime.datetime.now() #get the current datetime
    today = today.strftime("%m/%d/%Y, %H:%M:%S") #convert the current datetime to a string

    f = open("StGnLogfile.txt", "a") #open/create a file and append to it
    f.write(today + " | " + data + "\n") #write the datetime and the data on a new line
    f.close() #close the file

def WaitUntilNextMorning():
    #Wait until tomorrow 00:00 am
    t = time.localtime()
    t = time.mktime(t[:3] + (0,0,0) + t[6:])
    secondsUntilMidnight = t + 24*3600 - time.time()
    secondsUntilMidnight += 60
    WriteToLogFile("Pausing the bot until the next day (pausing for this long: '" + str(datetime.timedelta(seconds=secondsUntilMidnight)) + "')")
    time.sleep(secondsUntilMidnight)



#check if the config file exists
if not os.path.isfile('config.ini'):
    WriteToLogFile("ERROR - The config file 'config.ini' doesn't exist. Please make sure the config file is in the same directory from which you are running this script.")
    raise ValueError("The config file 'config.ini' doesn't exist. Please make sure the config file is in the same directory from which you are running this script.")




config = configparser.ConfigParser()
config.read('config.ini') #load the config file

#load the values from the config file
requestUrl = os.environ.get('REQUESTURL', '')
textMessages = config['config']['textMessage']

textMessages = list(textMessages.split("|")) #convert to a list

userToken = os.environ.get('TOKEN', '')
timeToSend = config['config']['timeToSend']

timeToSend = list(timeToSend.split("|")) #convert to a list

repeat = config['config']['repeat']


dateLastSent = ""


# error handling

print("1")

if 'discord' not in requestUrl or not validators.url(requestUrl):
    WriteToLogFile("ERROR - Please enter a valid url.")
    raise ValueError('Please enter a valid url.')
print("2")

if userToken == "":
    WriteToLogFile("ERROR - Please enter a Discord token in the config file")
    raise ValueError('Please enter a Discord token in the config file')
print("3")

if not textMessages[0]:
    WriteToLogFile("ERROR - Please enter at least one message for the bot to send.")
    raise ValueError('Please enter at least one message for the bot to send.')
print("4")

for message in textMessages:
    if message == "":
        WriteToLogFile("ERROR - Please make sure that each textmessage in the config file is at least one character long.")
        raise ValueError('Please make sure that each textmessage in the config file is at least one character long.')
print("5")

try:
    repeat = int(repeat)
except:
    WriteToLogFile("ERROR - Please enter a numerical value greater than or equal to -1, that isn\'t 0 as the repeat value.")
    raise ValueError('Please enter a numerical value greater than or equal to -1, that isn\'t 0 as the repeat value.')
print("6")

if repeat < -1 or repeat == 0:
    WriteToLogFile("ERROR - Please enter a numerical value greater than or equal to -1, that isn\'t 0 as the repeat value.")
    raise ValueError('Please enter a numerical value greater than or equal to -1, that isn\'t 0 as the repeat value.')
print("7")

if not timeToSend[0]:
    WriteToLogFile("ERROR - Please enter at least one timestamp in the config file")
    raise ValueError('Please enter at least one timestamp in the config file')
print("8")

if len(timeToSend) > 2:
    WriteToLogFile("ERROR - Please only enter a maximum of 2 timestamps in the config file")
    raise ValueError('Please only enter a maximum of 2 timestamps in the config file')
print("9")

# for timestamp in timeToSend:
#         try:
#             time.strptime(timestamp, '%H:%M:%S')
#         except:
#             WriteToLogFile("ERROR - Please make sure that all timestamps are in the following format: hh:mm:ss")
#             raise ValueError('Please make sure that all timestamps are in the following format: hh:mm:ss')



#         h, m, s = timestamp.split(':')
#         timeToSendSeconds = (int(h) * 3600 + int(m) * 60 + int(s)) #the time in the config file, converted to seconds

#         h, m, s = time.ctime()[11:19].split(':')
#         currentTime = (int(h) * 3600 + int(m) * 60 + int(s)) #the current time, converted to seconds
                
#         timeToSendSeconds -= currentTime #amount of seconds until we need to send the message
        
#         if timeToSendSeconds - 5 <= 0:
#             WriteToLogFile("WARNING - One of the timestamps (" + timestamp + ") occured before the current time (" + time.ctime()[11:19] + "). Therefore, the bot will sleep until the next day before sending a message.")
#             WaitUntilNextMorning()
#             break




# print("kaas")




# # while repeat <= -1 or repeat > 0:

# if dateLastSent == datetime.datetime.today().strftime('%Y-%m-%d'):
#     WaitUntilNextMorning()
    

# textToSend = random.choice(textMessages) #select a random text message


# if len(timeToSend) == 1: #if there is just one timestamp given, calculate the amount of seconds until when the bot should send the message
#     h, m, s = timeToSend[0].split(':')
#     timeToSendSeconds = (int(h) * 3600 + int(m) * 60 + int(s)) #the time in the config file, converted to seconds

#     h, m, s = time.ctime()[11:19].split(':')
#     currentTime = (int(h) * 3600 + int(m) * 60 + int(s)) #the current time, converted to seconds

#     timeToSendSeconds -= currentTime #amount of seconds until we need to send the message

# elif len(timeToSend) == 2: #There are 2 timestamps, so we will select a random time between the two
#     h, m, s = timeToSend[0].split(':')
#     timeStampOne = (int(h) * 3600 + int(m) * 60 + int(s)) #the first timestamp in the config file, converted to seconds

#     h, m, s = timeToSend[1].split(':')
#     timeStampTwo = (int(h) * 3600 + int(m) * 60 + int(s)) #the second timestamp in the config file, converted to seconds

#     h, m, s = time.ctime()[11:19].split(':')
#     currentTime = (int(h) * 3600 + int(m) * 60 + int(s)) #the current time, converted to seconds

#     if timeStampOne <= timeStampTwo:
#         timeToSendSeconds = random.randrange(timeStampOne, timeStampTwo) #select a random time, between the two timestamps from the config file
#     else:
#         timeToSendSeconds = random.randrange(timeStampTwo, timeStampOne)

#     timeToSendSeconds -= currentTime #amount of seconds until we need to send the message



# WriteToLogFile("'" + textToSend + "' will be send at: " + str(datetime.timedelta(seconds=timeToSendSeconds + currentTime)))
# time.sleep(timeToSendSeconds) #hiberante/pause the program, until it can send the message


# payload = {
#     'content': textToSend
# }

# header = {
#     'authorization': userToken
# }

# r = requests.post(requestUrl, data=payload, headers=header) #make a webrequest AKA send the message
# WriteToLogFile("Message sent")
# dateLastSent = datetime.datetime.today().strftime('%Y-%m-%d')

# repeat -= 1


# WriteToLogFile("Closing the bot")