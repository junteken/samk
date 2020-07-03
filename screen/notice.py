from screen.featurebase import FeatureBase
import os
import commons
from PIL import Image


class Notice(FeatureBase):

    def __init__(self):
        
        self.ref_image_name = "./state_img/공지.jpg"
        self.sample_text_file = "./state_img/공지.txt"

        print(os.getcwd())



        if not os.path.isfile(self.sample_text_file):
            print("파일 " + self.sample_text_file + " 이 존재하지 않습니다. 생성합니다.")
            # 여기서는 레퍼런스 이미지 기반으로 OCR을 돌리고 결과를 파일로 저장한다. 이유는 개발중 매번 OCR을 돌리면
            # 클라우드 비용이 증가하고 개발속도도 느리기때문이다.
            if os.path.isfile(self.ref_image_name):
                #im = Image.open(self.ref_image_name)  # 이미지 불러오기
                self.texts = commons.gcv.detect_text_jpg(self.ref_image_name)
                self.save_text(self.texts)

            else:
                print("이미지 파일조차 없습니다.")

    def _save_text(self, texts):
        text_file = open(self.sample_text_file, "w")
        for text in texts:
            text_file.write('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])

            text_file.write('bounds: {}'.format(','.join(vertices)))

        text_file.close()