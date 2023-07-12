from screen.featurebase import FeatureBase

class GameQuit(FeatureBase):
    # 게임올 나가시켓습니까? 취소 확인

    def __init__(self):
        self.name = '게임종료'
        self.feature_texts=['게임올', '취소', '확인']
        self.img_file_path = './rsrc/state_img/game_quit.png'

