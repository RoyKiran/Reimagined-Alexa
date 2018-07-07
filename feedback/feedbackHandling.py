# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 23:15:23 2018

@author: WorkIsFun@ Kiran Roy
"""

import datetime, boto3

client = boto3.resource('dynamodb')        #Initialize DynamoDb

#-------------- Create Questions, Options and Answers -------------------

questions = ["Please tell me the last 4 digits of your bill number","Please let us know your age","How would you rate the ambience?","Please rate the food between 1-5 with 1 as poor and 5 as Great", "Please rate the service as " , "Would you recommend this place to your friends?","Should we improvement in food "]

options = ["","","Good, Average, Bad","","Good,Average,Bad","Yes, No","Quality, Quantity, Variety or Nothing"]




#######----------- Helpers that build all of the responses ---------------########

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

###### ---------- Handle Pause & Resume task --------#
# Todo: Update what u retrieve / store on pause in diff table
'''def pause_check(session):
    table = client.Table('skill')      # DynamoDB Table
    user= session['user']['userId']    # get the userId of the current user
    print("Userid = "+user)
     
    user=user[18:]                     # we need the string after the 19th character.    

    try:
       response = table.get_item(Key={ 'account': user })
       paused_question = response['Item']['paused_question']
       retrievedScore=response['Item']['score']

    except:
       count=0

    return ({'paused_question':paused_question, 'score':retrievedScore })
'''         
    
def pause_feedback(intent,session):
    card_title="Pause"
    user= session['user']['userId'][18:]                     # get the userId of the current user. we need the string after the 19th character.
    sessionId = session['sessionId']                         # get the sessionId of the current session    
    
    paused_question= session["attributes"]["currentQuestion"]    
    #saveScore= session['attributes']['score']
    
    data = {'account':user,'sessionID':sessionId, 'paused_question':paused_question}
    data.update(session["attributes"])
    data.update({"score":session['attributes']["score"]})
   

    table = client.Table('skill')                            # DynamoDB Table Name is 'skill' 
    capacity= table.put_item(Item = data , ReturnConsumedCapacity='TOTAL')
    
    print ("capacity" + capacity)                            # test
   
    should_end_session=True

    speech_output="Your progress was saved! Come back and resume any time!"
    reprompt_text=None
    
    session_attributes=""
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def resume_feedback(intent,session):        
    session_attributes = session["attributes"] # add a database entry for score

    speech_output="Welcome back! Here's where you left at, "   + get_question(session["attributes"]["currentQuestion"])    
    reprompt_text = None
    
    should_end_session=False

    return build_response(session_attributes, build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))
        

    
##### ---------- On Session end -----######
#reset the pause counter to 0
def reset(session):
    sessionId = session['sessionId']                         # get the sessionId of the current session    
    user = session['user']['userId'][18:]                    # get the userId of the current user. We need the string after the 19th character.
    
    data = {'account':user,'sessionID':sessionId}
    data.update(session["attributes"])
    #data.update({"score":session["attributes"]["score"]})
    
    table = client.Table('skill')                            # DynamoDB Table Name
    table.put_item(Item=data)                                # Add data to table


def handle_session_end_request(session):
    card_title = "Session Ended"
    speech_output = "Thanks for your valuable feedback. See you again! "
    
    reset(session)    
    should_end_session = True                                # Setting this to true ends the session and exits the skill.
    
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


######## ----------- Functions that control the skill's behavior -----------#########

def get_question(num):
    return(questions[num] + options[num])

def get_welcome_response(session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    #session_attributes = {}
    card_title = "Welcome"                          # this will be displayed on phone/web

    speech_output = "Welcome to the Feedback with me. Before we start, "+ get_question(0)
    reprompt_text = "I didn't get that . "+ get_question(0)
    
    
    '''response=check_paused_step(session)
    paused_check=int(response['count'])
    retrievedScore=int(response['savedScore'])

    if paused_check==0:
        speech_output = "Welcome to the Feedback with me. Before we start, "+get_question(0)
        reprompt_text = "I didn't get that . "+ get_question(0)

    else:
        speech_output= "Welcome to the Feedback with me. You have a saved Feedback. If you want to resume the saved session, say Resume or Restart"
        reprompt_text = "I didn't get that. Would you like to Resume the saved feedback or restart a new feedback? ."
        session_attributes = {"paused_check":paused_check , "retrievedScore":retrievedScore}
    '''
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.

    should_end_session = False
    
    return build_response(session["attributes"], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def start_feedback(intent, session):
    
    card_title = intent['name']
    session_attributes = session["attributes"]
    
    
    """ Check if slot exists & Check which slot is answered """        
    if "slots" in intent.keys():
        if (session_attributes['currentQuestion'] == 0 and "numCode" in intent["slots"].keys()) :               # Bill no. Answer     
            session_attributes["billNo"] = intent["slots"]["numCode"]["value"]
            session_attributes['currentQuestion'] += 1
            
        elif session_attributes['currentQuestion'] == 1 and "numOpt" in intent["slots"].keys():                 # Get Age
            session_attributes["age"] = intent["slots"]["numOpt"]["value"]
            session_attributes['currentQuestion'] += 1
            
    speech_output= get_question(session_attributes['currentQuestion'])
    reprompt_text = "Sorry, I didn't get that. " + get_question(session_attributes['currentQuestion'])
    
    should_end_session=False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def answer_question(intent, session):
    
    card_title = intent['name']
    session_attributes = session["attributes"]   
    choice = ""
    

    if "slots" in intent.keys():
        if (session_attributes['currentQuestion'] == 2 or session_attributes['currentQuestion'] == 4) and "optionA" in intent["slots"].keys() :     # Good-Avg-Bad Answer                
            #choice = intent["slots"]["optionA"]["value"]
            choice = intent["slots"]["optionA"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["name"]
            session_attributes['currentQuestion'] += 1
            session_attributes["result"].append(choice)
            
            if choice.lower() == "good":   
                session_attributes['score']+=10                       
    
            elif choice.lower() == "average":
                session_attributes['score']+=5       
    
            elif choice.lower() == "bad":
                session_attributes['score']+=0            
        
        elif session_attributes['currentQuestion'] == 3 and "optionD" in intent["slots"].keys():            #1-5 slot
            choice = intent["slots"]["optionD"]["value"]
            session_attributes['currentQuestion'] += 1
            session_attributes["result"].append(choice)
            session_attributes["score"] += int(choice)        
        
        elif session_attributes['currentQuestion'] == 5 and "optionB" in intent["slots"].keys():            # yes no quest
            choice = intent["slots"]["optionB"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["name"]
            session_attributes['currentQuestion'] += 1
            session_attributes["result"].append(choice.lower())
    
            if choice.lower() == "yes":
                session_attributes['score']+= 1
            else:
                session_attributes['score']+= 0            
            
        
        elif session_attributes['currentQuestion'] == 6 and "optionC" in intent["slots"].keys():            #improvement question
            choice = intent["slots"]["optionC"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["name"]
            session_attributes["result"].append(choice.lower())            
            session_attributes['currentQuestion'] += 1
    
    if session_attributes['currentQuestion'] <= len(questions)-1:
        if choice == "":
            speech_output = "Sorry, I didn't get that. " + get_question(session_attributes['currentQuestion'])
            reprompt_text = ""
        else:
            speech_output = "Next Question. " + get_question(session_attributes['currentQuestion'])                
            reprompt_text = ""
        
        should_end_session = False
            
    else :                   
        #should_end_session = True
        return handle_session_end_request(session)

    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#######------- Events -------########

# ----------- New Session ---------------
def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])
    
    session['attributes'] = {"currentQuestion":0, "score":0, "date":datetime.datetime.now().strftime("%B-%d-%Y  %I:%M%p"), "billNo":"", "age":"", "result":[]}
                                                            



#------------ On launch -------------------
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want
    """
    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    
    # Dispatch to your skill's launch
    return get_welcome_response(session)


# --------------- Other intents --------------
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "StartIntent":      
        '''if "attributes" in session.keys():
            return answer_question(intent,session)
        '''
        return start_feedback(intent, session)
        
    elif intent_name == "AnswerIntent":
        return answer_question(intent, session)
       
    elif intent_name == "AMAZON.ResumeIntent":
        return resume_feedback(intent, session)
    
    elif intent_name == "AMAZON.PauseIntent":
        return pause_feedback(intent, session)
    
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
        
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request(session)
        
    else:
        raise ValueError("Invalid intent")


# ------------- Session ends ----------------
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
    
    # Todo: add cleanup logic here
 


#######-------- Main function -------#########

def lambda_handler(event, context):
    
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    
    if event['session']['new']:                                                  # if its a new session, go to on_session_started() funtion
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    
