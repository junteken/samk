import easyocr
from screen import world

reader= easyocr.Reader(['ko', 'en'], gpu= False)

# result= reader.readtext('./rsrc/state_img/notice.jpg', detail=0)
#result= reader.readtext(u'./rsrc/state_img/공지.jpg', detail=0)
#result= reader.readtext('./공지.jpg', detail=0)
result= reader.readtext('./rsrc/state_img/world.jpg', detail=0)




print(result)

