# Built-ins
import io
import os

# Google Libs
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import enums
from google.cloud.vision import types


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

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return parse_face_emotions(response.face_annotations)


def batch_detect_faces_uri(image_uris = []):
    """Batch detections of faces via iamge uri"""

    if not image_uris:
        return []

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    features = [
        # types.Feature(type=enums.Feature.Type.LABEL_DETECTION),
        types.Feature(type=enums.Feature.Type.FACE_DETECTION),
    ]

    requests = []

    for image_uri in image_uris:
        image = types.Image()
        image.source.image_uri = image_uri
        request = types.AnnotateImageRequest(image=image, features=features)
        requests.append(request)

    response = client.batch_annotate_images(requests)

    face_index = 0
    faces_batched = []
    for _response in response.responses:
        item_date = dict()
        item_date['face_request'] = face_index
        item_date['from_url'] = image_uris[face_index]
        item_date['faces_emotions'] = parse_face_emotions(_response.face_annotations)
        faces_batched.append(item_date)
        face_index += 1

    return faces_batched


def parse_face_emotions(face_annotations):
    """Parse google annotation reponse into readable dict format"""

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    faces_emotions = []
    face_index = 0
    for face in face_annotations:
        face_emotion = dict()
        face_emotion['face_number'] = face_index
        face_emotion['joy_likelihood'] = likelihood_name[face.joy_likelihood]
        face_emotion['sorrow_likelihood'] = likelihood_name[face.sorrow_likelihood]
        face_emotion['anger_likelihood'] = likelihood_name[face.anger_likelihood]
        face_emotion['surprise_likelihood'] = likelihood_name[face.surprise_likelihood]
        face_emotion['under_exposed_likelihood'] = likelihood_name[face.under_exposed_likelihood]
        face_emotion['blurred_likelihood'] = likelihood_name[face.blurred_likelihood]
        face_emotion['headwear_likelihood'] = likelihood_name[face.blurred_likelihood]
        face_index += 1
        faces_emotions.append(face_emotion)

        # Not deleting this might come handy next time
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

    return faces_emotions