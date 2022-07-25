def handler(event, context):
    print('Incoming event: ', event)
    
    for record in event['Records']:
        print(record)
        
    return {}