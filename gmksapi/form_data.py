import requests


PHONE_NUMBER_FIELD_ID = 'J8aHZ7DEtoNe'
DISTRICT_FIELD_ID = 'b63Vewm8kk97'
def _get_responses():
    response = requests.get('https://api.typeform.com/forms/JuGMw6wE/responses', headers={
        'Authorization': 'Bearer tfp_ERk6Z1iRTEyeHqtw6tRMmsVkPkr5U6gM2N9ub3deygMa_dKt58Dvjm6LP'}).json()

    respones = []
    for item in response['items']:
        phone_number = None
        district = None
        for answer in item['answers']:
            if answer['field']['id'] == PHONE_NUMBER_FIELD_ID:
                phone_number = answer['phone_number']
            elif answer['field']['id'] == DISTRICT_FIELD_ID:
                district = answer['text']
        respones.append({'phone_number': phone_number, 'district': district})





def get_phone_numbers(district=None):
    answers = _get_responses()
    if district is not None and district != 'General':
        answers = [x for x in answers if x['district'] == district]
    phone_numbers = [x['phone_number'] for x in answers]



    if district:
        return [x.phone_number for x in Profile.objects.filter(district=district)]
    else:
        return [x.phone_number for x in Profile.objects.all()]
