import easyocr
import io



g_reader = easyocr.Reader(['ko', 'en'], gpu=False)

accountList={
    "창천" : "BlueStacks",
    "초월" : "",
    "은선" : "",
    "백호" : "",
    "주작" : "",
    "진룡" : "",
    "봉무" : "",
    "정련" : "",
}


def scan(bsimage):
    img_byte = io.BytesIO()
    bsimage.save(img_byte, format='PNG')
    img_byte = img_byte.getvalue()

    result = g_reader.readtext(img_byte, detail=1)

    print(result)

    return result

def search_word(ocr_result, keyword, debug=False):
    found = [v for _, v in enumerate(ocr_result) if keyword in v[1]]

    if debug:
        if found is None:
            print('단어를 찾지 못했습니다.')
        else:
            for w in found:
                print('단어를 찾았습니다.')

    return found
