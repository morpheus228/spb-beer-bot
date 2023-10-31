import datetime
from aiogram.types import Message


encode_event_attrs = {
    'message': {
        'message_id': lambda x: x,
        'text': lambda x: x,
        'location': lambda x: [x.latitude, x.longitude]},
}

def encode_user_message(mesage: Message) -> dict:
    log = {
        "_id": mesage.message_id,
        "user_id": mesage.from_user.id,
        "created_at": datetime.datetime.now(),
        'event_type': 'message',
        'message': {}
    }

    for attr in encode_event_attrs[log['event_type']].keys():
        attr_value = mesage.__getattribute__(attr)
        if attr_value is not None:
            log[log['event_type']][attr] = encode_event_attrs[log['event_type']][attr](attr_value)
        
    return log
