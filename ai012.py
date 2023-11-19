# Face Recognition/Identification
import cv2 as cv
import face_recognition as fr
import os

# training data
knownFaces = [
    {
        "file": "JoeBiden.jpg", 
        "name": "Joe Biden",
        "code": None,
    },
    {
        "file": "FumioKishida.jpg", 
        "name": "Fumio Kishida",
        "code": None,
    },
    {
        "file": "XiJinPing.jpg", 
        "name": "Xi Dada",
        "code": None,
    },
    {
        "file": "JustinTrudeau.jpg", 
        "name": "Justin Trudeau",
        "code": None,
    },
]

# return the encoding of the face detected in the image file
def train(face):
    # img is using "RGB" color
    img = fr.load_image_file("face-images/known/" + face["file"])
    faceLocations = fr.face_locations(img)
    faceCodes = fr.face_encodings(img, faceLocations)

    if len(faceLocations) > 0:
        top, right, bottom, left = faceLocations[0]
        frame = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        cv.rectangle(frame, (left, top), (right, bottom), (255,0,0), 2)
    cv.imshow(face['name'],frame) 

    if len(faceCodes) > 0:
        return faceCodes[0]
    else:
        return None


def recognize(filePath):
    img = fr.load_image_file(filePath)
    frame = cv.cvtColor(img, cv.COLOR_RGB2BGR)

    locations = fr.face_locations(img)
    codes = fr.face_encodings(img, locations)

    knownCodes = [face['code'] for face in knownFaces]

    for loc, code in zip(locations, codes):
        top, right, bottom, left = loc
        # draw face border
        cv.rectangle(frame, (left,top), (right,bottom), (255,0,0), 2)

        # draw face name
        matches = fr.compare_faces(knownCodes, code, tolerance=0.5)
        name = "unknown"
        for i in range(len(matches)):
            if matches[i] == True:
                name = knownFaces[i]['name']
                break
        cv.putText(frame, name, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    cv.imshow('face recog', frame)


# train by known faces
for face in knownFaces:
    face['code'] = train(face)
    #print(face)

# recognize unknow faces
recognize("face-images/unknown/u003.jpg")

cv.waitKey(0)