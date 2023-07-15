from screen.featurebase import FeatureBase

class Unknown(FeatureBase):
    # 이름설정같은 화면의 경우 ocr인식이 안되어서 
    def __init__(self):
        self.name = '알수없음'
        self.feature_texts=['향후 ocr인식이 잘되면 고쳐야함']
        self.img_file_path = './rsrc/state_img/naming.png'

