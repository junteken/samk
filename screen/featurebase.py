import os
from common import commons


class FeatureBase(object):

    def __init__(self):
        self.name = None
        self.feature_texts = None 
        self.img = None

    # feature_texts의 모든 문자들이 target_texts(ocr로 인식되어져 나온)이 존재하는지
    # 확인하는 함수
    def check(self, feature_texts, target_texts):
        return all(item in target_texts for item in self.feature_texts)
    
    # # 상속 받는 하위 class들은 함수를 반드시 구현해야함
    # def check_state(target_texts):
    #     pass

    # 다른 state의 image에 
    def cross_check(self, chk_img):
        recog_dict = commons.g_reader.readtext(chk_img)
        result = all(any(s in value for s in self.feature_texts) for _, value in enumerate(recog_dict))

        return result



        



   



