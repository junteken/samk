import os
from common import commons


class FeatureBase(object):

    def __init__(self, ref_img, text_file):
        self.ref_image_name= ref_img
        self.sample_text_file= text_file
        self.texts=None
        self.ocrtexts=[]

        try:
            self._make_text()

        except Exception as ex:
            print("feature text를 읽어오는데 실패했습니다.", ex)



    def _make_text(self):
        if not os.path.isfile(self.sample_text_file):
            print("파일 " + self.sample_text_file + " 이 존재하지 않습니다. 생성합니다.")
            # 여기서는 레퍼런스 이미지 기반으로 OCR을 돌리고 결과를 파일로 저장한다. 이유는 개발중 매번 OCR을 돌리면
            # 클라우드 비용이 증가하고 개발속도도 느리기때문이다.
            if os.path.isfile(self.ref_image_name):
                #im = Image.open(self.ref_image_name)  # 이미지 불러오기
                self.texts = self.runOCR(self.ref_image_name)
                self._save_text()
            else:
                print("이미지 파일조차 없습니다.")
        else:
            self._load_text()


    #OCR을 따로 빼놓은 이유는 개발시 OCR만 돌릴 필요가 있는 경우가 많아서이다.
    def runOCR(self, image_name):
        return commons.gcv.detect_text_jpg(image_name)

    def _load_text(self):
        f = open(self.sample_text_file, 'r')
        description=None

        while True:
            line = f.readline()
            if not line: break

            description= line

            if "bounds" in description:
                ocr_item.setBound(description)
            else:
                ocr_item.setText(line)
                while True:
                    innerline= f.readLine()


            print(line)
        f.close()

    def _save_text(self):
        text_file = open(self.sample_text_file, "w")
        for text in self.texts:
            text_file.write('\n{}'.format(text.description))

            vertices = (['{},{}'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            text_file.write('bounds = {}'.format(':'.join(vertices)))

        text_file.close()

    def _print_text(self):
        print('Texts:')

        for text in self.texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))



