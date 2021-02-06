#!/usr/bin/python
# -*- coding: utf-8 -*-


# 설치법 https://lovablebaby1015.wordpress.com/2018/09/24/mecab-macos-설치-삽질-후기-작성중/
# 사용법 https://mr-doosun.tistory.com/22
import MeCab
import sys
import string
sentence = "무궁화꽃이피었습니다."

try:
    print(MeCab.VERSION)

    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic')
    print(t.parse(sentence))

    m = t.parseToNode(sentence)
    while m:
        print(m.surface, "\t", m.feature)
        m = m.next
    print("EOS")

    lattice = MeCab.Lattice()
    t.parse(lattice)
    lattice.set_sentence(sentence)
    len = lattice.size()
    for i in range(len + 1):
        b = lattice.begin_nodes(i)
        e = lattice.end_nodes(i)
        while b:
            print("B[%d] %s\t%s" % (i, b.surface, b.feature))
            b = b.bnext 
        while e:
            print("E[%d] %s\t%s" % (i, e.surface, e.feature))
            e = e.bnext 
    print("EOS")

    d = t.dictionary_info()
    while d:
        print("filename: %s" % d.filename)
        print("charset: %s" %  d.charset)
        print("size: %d" %  d.size)
        print("type: %d" %  d.type)
        print("lsize: %d" %  d.lsize)
        print("rsize: %d" %  d.rsize)
        print("version: %d" %  d.version)
        d = d.next

    from konlpy.tag import Mecab
    mecab = Mecab()
    nouns = mecab.nouns("고양이가 냐 하고 울면 나는 녜 하고 울어야지")
    print(nouns)
    # ['고양이', '나', '녜']

    # 빛 아래 유령
    poem = """
    ... 흘러내린 머리카락이 흐린 호박빛 아래 빛난다.
    ... 유영하며.
    ... 저건가보다.
    ... 세월의 힘을 이겨낸 마지막 하나 남은 가로등.
    ... 미래의 색, 역겨운 청록색으로 창백하게 바뀔 마지막 가로등
    ... 난 유영한다. 차분하게 과거에 살면서 현재의 공기를 마신다.
    ... 가로등이 깜빡인다.
    ...
    ... 나도 깜빡여준다.
    ... """
    morphs = mecab.morphs(poem)  # 형태소 단위로 나누기
    print(morphs)
    # ['흘러내린', '머리카락', '이', '흐린', '호박', '빛', '아래', '빛난다', '.', '유영', '하', '며', '.', '저건가', '보', '다', '.', '세월', '의', '힘', '을', '이겨', '낸', '마지막', '하나', '남', '은', '가로등', '.', '미래', '의', '색', ',', ' 역겨운', '청록색', '으로', '창백', '하', '게', '바뀔', '마지막', '가로등', '난', '유영', '한다', '.', '차분', '하', '게', '과거', '에', '살', '면서', '현재', '의', '공기', '를', '마신다', '.', '가로등', '이', '깜빡인다', '.', '나', '도', ' 깜빡', '여', '준다', '.']

    pos = mecab.pos("다람쥐 헌 쳇바퀴에 타고 파")
    print(pos)
    # [('다람쥐', 'NNG'), ('헌', 'XSV+ETM'), ('쳇바퀴', 'NNG'), ('에', 'JKB'), ('타', 'VV'), ('고', 'EC'), ('파', 'VX+EC')]


except RuntimeError as e:
    print("RuntimeError:", e)
