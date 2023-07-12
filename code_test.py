from common import commons

result = commons.g_reader.readtext('./rsrc/state_img/bluestack.png')

for item in result:
    if '삼국지K' in item[1] :
        print('삼국지k 찾음')