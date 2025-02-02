import face_recognition
import cv2
import numpy as np
import os
from django.conf import settings

def detec():
    path = os.path.join(settings.MEDIA_URL, "head.jpg").replace("\\", "/")
    print(f'path inside detec {path}')

    img = cv2.imread(path[1:])

    # Load a sample picture and learn how to recognize it.
    # for i in dataset:    
    obama_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Dylan.png")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    biden_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Jesse.jpg")
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    Sisiya_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Sisiya.jpg")
    Sisiya_face_encoding = face_recognition.face_encodings(Sisiya_image)[0]

    Simmon_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Simmon.jpg")
    Simmon_face_encoding = face_recognition.face_encodings(Simmon_image)[0]

    unknown_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/unknown.jpg")
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

    Garry_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Garry.jpg")
    Garry_face_encoding = face_recognition.face_encodings(Garry_image)[0]

    Wells_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Wells.png")
    Wells_face_encoding = face_recognition.face_encodings(Wells_image)[0]

    Keith_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Keith.jpg")
    Keith_face_encoding = face_recognition.face_encodings(Keith_image)[0]

    YiNing_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Yi_Ning.jpg")
    YiNing_face_encoding = face_recognition.face_encodings(YiNing_image)[0]

    Dealia_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Dealia.jpg")
    Dealia_face_encoding = face_recognition.face_encodings(Dealia_image)[0]

    Sisiya_image = face_recognition.load_image_file("upload/static/upload/pictures_of_people_i_know/Sisiya.jpg")
    Sisiya_face_encoding = face_recognition.face_encodings(Sisiya_image)[0]

    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding,
        Sisiya_face_encoding,
        Simmon_face_encoding,
        unknown_face_encoding,
        Garry_face_encoding,
        Wells_face_encoding,
        Keith_face_encoding,
        YiNing_face_encoding,
        Dealia_face_encoding,
        Sisiya_face_encoding
    ]
    known_face_names = [
        "Dylan",
        "Jesse",
        "Sisiya",
        "Simon",
        "Jerry",
        "Garry",
        "Wells",
        "Keith",
        "Yi-Ning",
        "Dealia",
        "Sisiya"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]


    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample = 2)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.4)
        # print(matches)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
            # first_match_index = matches.index(True)
            # name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # # Display the resulting image
    # cv2.imshow('',rgb_small_frame)
    out_path = os.path.join(settings.MEDIA_URL, "out_face.jpg").replace("\\", "/")
    cv2.imwrite(out_path[1:], img)
    if len(face_names) > 0:
        return face_names[0]
    else:
        return 'Unknown'

    # if cv2.waitKey(1) & 0xFF == ord('p'):
    #     cv2.imwrite('./output.jpg', frame)
        
    # # Hit 'q' on the keyboard to quit!
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    # # Release handle to the webcam
    # video_capture.release()
    # cv2.destroyAllWindows()
