import twilio
from twilio.rest import Client

def textmyself(message):
    try:
        accountSID='ACe918691d54c1e409788f5df9d2******'
        authToken='f21e9c24acabbf70aae4874f7c******'
        myNumber='+8618516******'
        twilioNumber='+1203*******'

        twilioCli = Client(accountSID,authToken)
        # python2
        # twilioCli.api.account.messages.create(body=message,from_=twilioNumber,to=myNumber)
        twilioCli.messages.create(body=message,from_=twilioNumber,to=myNumber)
        return 0
    except:
        return -1