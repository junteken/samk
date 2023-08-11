import difflib
import hgtk
# ' 무장 다 오기 출전무장 전체 다 유수 레벌\] 
# [} 휴식슬못 조합\] 병력: 1400 {급속: 560}
# 출전무장글리 {+전: 48790} 훈진기능 조합2 
# 휴식슬못 휴식슬못 출전무장글렉 출전무장글렉 조합3 Iii\]
#  순진기능 순진기능 + 휴식슬못 휴식슬못 출전무장클렉
#  출전무장클렉 출진기능 출진기능 + 휴식슬못 {슬릇 미오문} 
# 출전무장클렉 {캐릭터4이레벌 오른} 손진기능 n'
# 비교할 두 문자열 생성
str1 = "출진가능"
str2 = "손진기능"

# 문자열을 자모음 단위로 분리합니다.
str1_jamo = hgtk.text.decompose(str1)
str2_jamo = hgtk.text.decompose(str2)

# SequenceMatcher 객체 생성
seq_matcher = difflib.SequenceMatcher(None, str1_jamo, str2_jamo)

# 두 문자열 사이의 유사도를 계산합니다.
similarity = seq_matcher.ratio()

print("두 문자열의 유사도: {:.2%}".format(similarity))