import io
import os

# Imports the Google Cloud client library
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import enums
from google.cloud.vision import types


def test_google_vision():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath('resources/face_surprise.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)

    print()

def detect_faces(path = None):
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()

    # use default for now
    if path is None:
        path = os.path.abspath('resources/face_surprise.jpg')

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def detect_faces_uri(uri = None):
    """Detects faces in the file located in Google Cloud Storage or the web."""

    if uri is None:
        uri = "https://storage.googleapis.com/cloud-vision-codelab/face_surprise.jpg"

    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    faces_emotions = []

    for face in faces:
        face_emotion = dict()
        face_emotion['anger_likelihood'] = likelihood_name[face.anger_likelihood]
        face_emotion['joy_likelihood'] = likelihood_name[face.joy_likelihood]
        face_emotion['surprise_likelihood'] = likelihood_name[face.surprise_likelihood]
        face_emotion['sorrow_likelihood'] = likelihood_name[face.sorrow_likelihood]

        faces_emotions.append(face_emotion)

        # Not deleting this might come handy next time
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return faces_emotions

def load_crendential_from_file(path = None):

    credentials = service_account.Credentials.from_service_account_file(
        os.path.abspath(os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    return credentials

def detect_faces_uri_multple(uri = None):

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    features = [
        # types.Feature(type=enums.Feature.Type.LABEL_DETECTION),
        types.Feature(type=enums.Feature.Type.FACE_DETECTION),
    ]

    requests = []

    if uri is None:
        uri = "https://storage.googleapis.com/cloud-vision-codelab/face_surprise.jpg"

    image_uris = []
    image_uris.append("https://storage.googleapis.com/cloud-vision-codelab/face_surprise.jpg")
    image_uris.append("https://codelabs.developers.google.com/codelabs/cloud-vision-intro/img/e0600f08ea3d5c8a.jpeg")


    for image_uri in image_uris:
        image = types.Image()
        image.source.image_uri = image_uri
        request = types.AnnotateImageRequest(image=image, features=features)
        requests.append(request)

    response = client.batch_annotate_images(requests)

    face_index = 0
    faces_batched = []
    for annotation_response in response.responses:
        item_date = dict()
        item_date['face_request'] = face_index
        item_date['from_url'] = image_uris[face_index]
        item_date['faces_emotions'] = parse_face_emotions(annotation_response.face_annotations)
        faces_batched.append(item_date)
        print(face_index)
        face_index += 1


    return faces_batched

def parse_face_emotions(face_annotations):

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    faces_emotions = []

    face_index = 0
    for face in face_annotations:
        face_emotion = dict()
        face_emotion['face_number'] = face_index
        face_emotion['anger_likelihood'] = likelihood_name[face.anger_likelihood]
        face_emotion['joy_likelihood'] = likelihood_name[face.joy_likelihood]
        face_emotion['surprise_likelihood'] = likelihood_name[face.surprise_likelihood]
        face_emotion['sorrow_likelihood'] = likelihood_name[face.sorrow_likelihood]
        face_index += 1

        faces_emotions.append(face_emotion)

    return faces_emotions