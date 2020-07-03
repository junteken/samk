# API KEY= AIzaSyDYlo8D1iXnRfkersRQCszm_PnwmGcBf7w

import os
import io

class google_vision(object):

    def __init__(self):
        self.api_key= "AIzaSyDYlo8D1iXnRfkersRQCszm_PnwmGcBf7w"
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.json_credential

    def detect_text(self, content):
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()

        imageio= io.BytesIO()
        content.save(imageio, format="PNG")
        image = vision.types.Image(content=imageio.getvalue())
        response = client.text_detection(image=image)
        texts = response.text_annotations

        print('Texts:')

        for text in texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

        return texts

        return texts

    def detect_text_jpg(self, content):
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        imageio=None

        with open(content, 'rb') as f:
            imageio = f.read()

        image = vision.types.Image(content=imageio)
        response = client.text_detection(image=image)
        texts = response.text_annotations







