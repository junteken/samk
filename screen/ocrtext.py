#구글 ocr result결과 string을 de-serialization하는 코드

class OcrText(object):
    def __init__(self):
        self.text=None
        self.left=None
        self.top= None
        self.right=None
        self.bottom=None

    def setText(self, t):
        self.text= t

    def appendText(self, t):
        self.text += t

    def setBound(self, b):
        points= b.split(sep=':')

        temp= points[1].split(sep=',')
        self.left= int(temp[0])
        self.top= int(temp[2])

        temp= points[2].split(sep=',')
        self.right=int(temp[0])
        self.bottom=int(temp[2])

        print("google vision bounds {}".format(b))
        print("읽어낸 좌표는 left={}, top={}, right={}, bottom={}".format(self.left, self.top, self.right, self.bottom))









