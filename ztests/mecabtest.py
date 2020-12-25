from konlpy.tag import Mecab
mecab = Mecab()
mc = mecab.pos('5G휴대폰에 대해서 설명해줘。')
print(mc)
mc = mecab.pos('ＮＥＣが二位、東芝がモトローラを抜いて二年ぶりに三位になる。')
print(mc)

#
# from konlpy.tag import Kkma
# Kkma_pos = Kkma()
# K_nouns = Kkma_pos.nouns('지금부터 코엔엘파이 한국어 형태소 분석기 설치를 확인')
# print(K_nouns)

