from face_detection_recognisation import detect_face
from configure_clients import firebase_user_sign_in
import time


def welcome_message():
    print("Welcome to Beat The Culprits ")
    print("")
    time.sleep(1)
    print("This application uses your computer's webcam and internet connection . \n"
          "Make sure you have a functioning webcam and active internet connection")
    print("")
    time.sleep(4)
    print("To close the application , simply close the console window")
    time.sleep(2)
    print("")
    print("Beat The Culprits brought to you by TEAM DOMINATORS")
    time.sleep(2)
    print("")
    print("Criminal detection and recognition is starting in ")
    print("")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("starting...")


def start_process():
    welcome_message()
    try:
        firebase_id_token = firebase_user_sign_in()
        detect_face(firebase_id_token)
    except Exception as e:
        print("ERROR OCCURRED while starting the face detection and recognition process"+str(e))


start_process()
