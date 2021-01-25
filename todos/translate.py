import os
import json

import boto3
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')

def detectTextLanguage(text):
    response = comprehend.detect_dominant_languaje(Text=text)
    
    return response
    
def translateText(text, source, target):
    
    response = translate.translate_text(
        Text = text,
        SourceLanguageCode = source,
        TargetLanguageCode = target
    )
    
    return response


def getTranslate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    text = result['Item']['text']
    
    ##sourceResult = detectTextLanguage(text)
    ##source = sourceResult['Languages'][0]['LanguageCode']
    
    target = event['pathParameters']['language']
    
    taskTranslated = translateText(
        text,
        'en',
        target
    )
    
    result['Item']['text'] = taskTranslated['TranslatedText']
    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response