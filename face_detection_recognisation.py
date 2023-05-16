import pathlib
import cv2  # Used for detecting face only frames
import winsound  # Used for playing alarm after recognizing of criminal
import time  # Used for fetching the current system time
from azure_recognisation import azure_recognisation
from configure_clients import send_text_to_authority
from configure_clients import get_name_from_id

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)


# Defining detectFace() method for capturing photo frames containing face

def detect_face(firebase_id_token):
    while True:
        flag = False

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        k = cv2.waitKey(1)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the face

        for (x, y, w, h) in faces:

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if frame.any():
                flag = True

        # Display the resulting frame
        cv2.imshow("Beat The Culprits", frame)
        if flag:
            when_flag_is_true(frame, firebase_id_token)


def when_flag_is_true(frame, firebase_id_token):
    time_stamp = time.time()
    cv2.imwrite(filename=str(time_stamp) + '.jpg', img=frame)
    image = open(str(time_stamp) + '.jpg', 'r+b')
    response = azure_recognisation(image)
    if response == "not found":
        print("Not a criminal")
        try:
            image.close()
            delete_image(time_stamp)
        except Exception as e:
            print("Error while deleting the file" + str(e))
    elif response == "error":
        print("error occurred while recognising the face")
        try:
            image.close()
            delete_image(time_stamp)
        except Exception as e:
            print("Error while deleting the file" + str(e))
    else:
        try:
            criminal_name = get_name_from_id(response, firebase_id_token)
            print("Criminal has been successful identified ! ")
            print("Name : " + criminal_name)
            print("")
            send_text_to_authority(criminal_name)
            winsound.PlaySound('SirenNoise.wav', winsound.SND_FILENAME)
            time.sleep(5)
        except:
            print("Error while sending the message ")


def delete_image(time_stamp):
    file_to_rem = pathlib.Path(str(time_stamp) + '.jpg')
    file_to_rem.unlink()
