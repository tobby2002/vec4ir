import re
import string

itext = '우리나라 대한민국. - 111 222 america is AMD  5G 5g'
# remove korean

itext = itext.lower()
otext = re.sub("[^a-z0-9|ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+", " ", itext)
print(otext)
# remove_number = re.sub("^\d$", " ", remove_korean)
# print(remove_number)
