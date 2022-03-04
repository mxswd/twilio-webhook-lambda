from __future__ import print_function
import json
import os
import urllib
import boto3
from twilio.twiml.voice_response import *
from twilio.request_validator import RequestValidator

def lambda_handler(event, context):
    print(event)
    # Example call Body payload
    # AccountSid=ACaaaaaaaa...
    # &ApiVersion=2010-04-01
    # &CallSid=CAaaaaaa....
    # &CallStatus=ringing
    # &CallToken=...
    # &Called=%2B15555555555
    # &CalledCity=
    # &CalledCountry=NZ
    # &CalledState=
    # &CalledZip=
    # &Caller=%2B15555555555
    # &CallerCity=
    # &CallerCountry=NZ
    # &CallerState=
    # &CallerZip=
    # &Direction=inbound
    # &From=%2B15555555555
    # &FromCity=
    # &FromCountry=NZ
    # &FromState=
    # &FromZip=
    # &To=%2B15555555555
    # &ToCity=
    # &ToCountry=NZ
    # &ToState=
    # &ToZip=
    
    params = dict(urllib.parse.parse_qsl(event['body'], keep_blank_values=True))
    url = "https://%s%s" % (event['requestContext']['domainName'], event['requestContext']['path'])
    validator = RequestValidator(os.environ['AUTH_TOKEN'])
    request_valid = validator.validate(
        url,
        params,
        event['headers']['X-Twilio-Signature']
    )
    
    # print(event['headers']['X-Twilio-Signature'])
    # print(validator.compute_signature(url, params))

    if request_valid:
        
        s3 = boto3.client('s3')
        
        # resp = VoiceResponse()
        # resp.dial("+15555555555")
        
        key = f"twiml/{params['Called']}.xml"
        print(key)
        resp = s3.get_object(Bucket=os.environ['TWIML_BUCKET'], Key=key)['Body'].read().decode('utf-8')
        return {
            "statusCode": 200,
            "body": resp,
            "headers": {
                "content-type": "application/xml"
            }
        }

    else:
        
        return {
            "statusCode": 401,
            "body": json.dumps({
                "message": "unauthorized"
            }),
        }
