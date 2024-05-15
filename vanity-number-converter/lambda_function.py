import boto3
import itertools

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VanityNumbers')

def phone_to_vanity(phone_number):
    letters = {
        '2': 'ABC', '3': 'DEF', '4': 'GHI',
        '5': 'JKL', '6': 'MNO', '7': 'PQRS',
        '8': 'TUV', '9': 'WXYZ'
    }

    vanity_numbers = []
    for num in phone_number:
        if num in letters:
            vanity_numbers.append(letters[num])
        else:
            vanity_numbers.append(num)
    
    return ["".join(combo) for combo in itertools.product(*vanity_numbers)]

def lambda_handler(event, context):
    phone_number = event['Details']['ContactData']['CustomerEndpoint']['Address']
    vanity_numbers = phone_to_vanity(phone_number)
    
    best_vanity_numbers = vanity_numbers[:5]
    
    table.put_item(
        Item={
            'PhoneNumber': phone_number,
            'VanityNumbers': best_vanity_numbers
        }
    )
    
    return best_vanity_numbers
