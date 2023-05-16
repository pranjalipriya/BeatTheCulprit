import requests
import json


def send_text_to_authority(name):
    myobj = {
        'Body': "CRIMINAL DETECTED : {} ".format(name),
        'From': '+18155818608',
        'To': 'your contact',

    }
    requests.post('https://api.twilio.com'
                  '.json',
                  auth=('secretkey', 'key'),
                  data=myobj)


def azure_detect(image):
    url = 'https://westus.api.cognitive.microsoft.com'
    headers = {"Content-Type": "application/octet-stream",
               "Ocp-Apim-Subscription-Key": 'key_value'}

    response = requests.post(url=url, headers=headers, data=image)
    dict_obj = json.loads(response.text)
    detected_face_id = dict_obj[0]['faceId']
    print('azure detected a face , temproary id provided to it :' + detected_face_id)
    return dict_obj[0]['faceId']


def azure_identify(detected_face_id):
    url = 'https://westus.api.cognitive.microsoft.com'
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': 'key_value'}
    request_body = {"faceIds": [
        detected_face_id
    ],
        "personGroupId": "criminal_group",

        "maxNumOfCandidatesReturned": 1,
        "confidenceThreshold": 0.45}

    response = requests.post(url=url, headers=headers, data=json.dumps(request_body))
    dict_obj = json.loads(response.text)
    azure_face_id = ""
    if not dict_obj[0]['candidates']:
        azure_face_id = "not found"
    else:
        azure_face_id = dict_obj[0]['candidates'][0]['personId']
        confidence = dict_obj[0]['candidates'][0]['confidence']
        print("criminal has been identified  with face id: " + azure_face_id)
        print("and confidence : " + str(confidence))
    return azure_face_id


def firebase_user_sign_in():
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword' \
          'sdfghj'

    data = {'email': 'ouremail@email.com', 'password': 'email_password', 'returnSecureToken': 'true'}
    response = requests.post(url=url, data=data)
    dict_obj = json.loads(response.text)
    id_token = dict_obj['idToken']
    return id_token


def get_name_from_id(azure_face_id, id_token):
    url = 'https://firestore.googleapis.com/v1/projects/beattheculprit/databases/(default)/documents/criminals/' + \
          azure_face_id
    headers = {'Authorization': 'Bearer ' + id_token}
    response = requests.get(url=url, headers=headers)
    dict_obj = json.loads(response.text)
    name = dict_obj['fields']['name']['stringValue']
    return name
