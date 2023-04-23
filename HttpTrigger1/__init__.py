import datetime
import pytz
import logging
import azure.functions as func
import json

locations = {
    'Bangkok': 'Asia/Bangkok',
    'Dubai': 'Asia/Dubai',
    'Mumbai': 'Asia/Kolkata',
    'Shanghai': 'Asia/Shanghai',
    'Tokyo': 'Asia/Tokyo',
    'Chicago': 'America/Chicago',
    'Los Angeles': 'America/Los_Angeles',
    'Mexico City': 'America/Mexico_City',
    'New York': 'America/New_York',
    'Toronto': 'America/Toronto',
    'Vancouver': 'America/Vancouver',
    'Sydney': 'Australia/Sydney',
    'Athens': 'Europe/Athens',
    'Berlin': 'Europe/Berlin',
    'London': 'Europe/London',
    'Paris': 'Europe/Paris',
    'Rome': 'Europe/Rome',
    'Auckland': 'Pacific/Auckland'
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('A request has been received.')
    city = req.params.get('city')
    if not city:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            city = req_body.get('city')

    if city not in locations:
        return func.HttpResponse(
            json.dumps({'error': 'Invalid city name'}),
            status_code=400
        )

    timezone = pytz.timezone(locations[city])
    current_time = datetime.datetime.now(tz=timezone)
    current_date = current_time.date()

    result = {'city': city,
              'time': current_time.strftime('%I:%M %p'),
              'date': current_date.strftime('%d-%m-%Y')}
    
    return func.HttpResponse(
        json.dumps(result),
        status_code=200,
        mimetype="application/json"
    )
