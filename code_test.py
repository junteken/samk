def check_substring(str1, str2):
    str1_len = len(str1)
    str2_len = len(str2)
    threshold = str1_len * 0.5

    for i in range(str2_len - str1_len + 1):
        # matching_count = sum(1 for a, b in zip(str1, str2[i:i+str1_len]) if a == b)
        matching_count = 0        
        for a, b in zip(str1, str2[i:i+str1_len]):
            if b == ' ':
                continue
            if a == b:
                matching_count += 1
        # print(f'matching count = {matching_count}')
        if matching_count >= threshold:
            # print(f'찾을문자열 = {str1}, 대상문자열 = {str2[i:i+str1_len]} 찾음')
            return True
    return False

str1 = "S 145"
str2 = "[처게이보 1카5"

if check_substring(str1, str2):
    print("str1 exists in str2.")
else:
    print("str1 does not exist in str2.")
