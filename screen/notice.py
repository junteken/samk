from screen.featurebase import FeatureBase

from PIL import Image


class Notice(FeatureBase):

    def __init__(self):
        ref_image_name= "./rsrc/state_img/공지.jpg"
        sample_text_file="./rsrc/state_img/공지.txt"

        super().__init__(ref_image_name ,sample_text_file)

    def print_notice(self):
        super()._print_text()



