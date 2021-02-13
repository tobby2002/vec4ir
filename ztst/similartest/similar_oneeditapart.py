def one_edit_apart(s1,s2):
    if len(s1) < len(s2):
        for x in range(len(s2)):
            if s2[:x]+s2[x+1:] == s1:
                return True
    elif len(s1) == len(s2):
        for x in range(len(s1)):
            if s1[x] != s2[x] and s1[:x]+s1[x+1:] == s2[:x]+s2[x+1:]:
                return True
    else:
        for x in range(len(s1)):
            if s1[:x] + s1[x+1:] == s2:
                return True
    return False

print(one_edit_apart('cat', 'dog'))
print(one_edit_apart('cat', 'cats'))
print(one_edit_apart('cat', 'cut'))
print(one_edit_apart('cat', 'cast'))
print(one_edit_apart('cat', 'at'))
print(one_edit_apart('cat', 'acts'))
print(one_edit_apart('휴대픈', '휴대폰'))
print(one_edit_apart('g대폰', '휴대폰'))
print(one_edit_apart('흐대폰', '휴대폰을'))
print(one_edit_apart('휴대', '휴디'))
print(one_edit_apart('후대', '휴대'))
print(one_edit_apart('휴대', '휴대폰'))
print(one_edit_apart('휴대폰', '휴대폰을'))

def get_similar_words(wordlist, q):
    ls = list(map(lambda x: str(x) if one_edit_apart(x, q) else None, wordlist))
    rs = list(filter(None, ls))
    return rs
