from rekognition_objects import (
    RekognitionFace as Rf, RekognitionCelebrity as Rc,
    RekognitionText as Rt)


class RekognitionImage:
    """
    Encapsulates an Amazon Rekognition image. This class is a thin wrapper
    around parts of the Boto3 Amazon Rekognition API.
    """

    def __init__(self, image, image_name, rekognition_client):
        """
        Initializes the image object.

        :param image: Data that defines the image, either the image bytes or
                      an Amazon S3 bucket and object key.
        :param image_name: The name of the image.
        :param rekognition_client: A Boto3 Rekognition client.
        """
        self.image = image
        self.image_name = image_name
        self.rekognition_client = rekognition_client

    @classmethod
    def from_file(cls, image_file_name, rekognition_client, image_name=None):
        """
        Creates a RekognitionImage object from a local file.

        :param image_file_name: The file name of the image. The file is opened and its
                                bytes are read.
        :param rekognition_client: A Boto3 Rekognition client.
        :param image_name: The name of the image. If this is not specified, the
                           file name is used as the image name.
        :return: The RekognitionImage object, initialized with image bytes from the
                 file.
        """
        with open(image_file_name, 'rb') as img_file:
            image = {'Bytes': img_file.read()}

        name = image_file_name if image_name is None else image_name
        return cls(image, name, rekognition_client)

    def detect_faces(self):
        """
        Detects faces in the image.

        :return: The list of faces found in the image.
        """

        response = self.rekognition_client.detect_faces(Image=self.image, Attributes=['ALL'])
        faces = [Rf.RekognitionFace(face) for face in response['FaceDetails']]

        return faces

    def detect_text(self):
        """
        Detects text in the image.

        :return The list of text elements found in the image.
        """
        response = self.rekognition_client.detect_text(Image=self.image)
        texts = [Rt.RekognitionText(text) for text in response['TextDetections']]

        return texts

    def recognize_celebrities(self):
        """
        Detects celebrities in the image.

        :return: A tuple. The first element is the list of celebrities found in
                 the image. The second element is the list of faces that were
                 detected but did not match any known celebrities.
        """

        response = self.rekognition_client.recognize_celebrities(Image=self.image)
        celebrities = [Rc.RekognitionCelebrity(celeb) for celeb in response['CelebrityFaces']]
        other_faces = [Rf.RekognitionFace(face) for face in response['UnrecognizedFaces']]

        return celebrities, other_faces

