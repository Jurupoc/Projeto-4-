from main import RekognitionImage
import boto3

from rekognition_objects import (show_bounding_boxes, show_polygons)


class Controller:
    def __init__(self):

        # Creates a connection with amazon services

        self.connection = boto3.client('rekognition',
                                       region_name='us-east-1',
                                       aws_access_key_id='ASIA4TZYRJ7NNTSHYSKR',
                                       aws_secret_access_key='G15rPS86cqIVoHSQuLrb+XSfPHDJ7DdEKDlvxs8i',
                                       aws_session_token='FwoGZXIvYXdzECUaDGPROD8mW8Vhd0QPRyLOAVdWBi+6CP+QveB7WrK7ZN4'
                                                         '5u+JiZzLd4qjieEYBzxh8u7VokSqUkmsefVYaPKAIwdFf6w+2sKw0l+n0by'
                                                         'ozilI3PBygQoNftU7FnNKRDvyQ1FIiIW/SC6WgDwXUTic+x8mApZ6E6i3i/'
                                                         'ASn1hAGeKgPaK+gly3mMuBkH6hbzFfgF6aXIcYhy79L8JoX2bmfTl0p6JhN'
                                                         'MgQ9A1QXRSh6v/eRZLYoeCzI8pXU8CA/DL3CM+cMHXxmKKYiWDh7WUrW/az'
                                                         '/3pxOW+wqTMwHoHsIKKfhlI0GMi1GgmT7Lc18pP5e2tDN6Vlk/+UPaPR04D'
                                                         '6e5QYEHE9ps5PvRJ723kwDOO8p33s=')

    def recognize_face(self, file_path):
        image = RekognitionImage.from_file(file_path, self.connection)
        faces = image.detect_faces()

        if len(faces) != 0:
            show_bounding_boxes(image.image['Bytes'],
                                file_path.split('/')[-1],
                                [[face.bounding_box for face in faces]],
                                ['red'])
        return len(faces)

    def recognize_celebrity(self, file_path):
        image = RekognitionImage.from_file(file_path, self.connection)
        celebs, others = image.recognize_celebrities()

        if len(celebs) != 0:
            show_bounding_boxes(
                image.image['Bytes'],
                file_path.split('/')[-1],
                [[celeb.face.bounding_box for celeb in celebs]],
                ['aqua'])
        return len(celebs)

    def text_recognizer(self, file_path):
        image = RekognitionImage.from_file(file_path, self.connection)
        texts = image.detect_text()

        show_polygons(
            image.image['Bytes'],
            file_path.split('/')[-1],
            [text.geometry['Polygon'] for text in texts],
            'green')

        return len(texts)




