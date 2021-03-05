
h_text = '우리나라 대한민국'
h_tag_pre = '<span>'
h_tag_post = '</span>'
h_word_list = ['민국']
h_snippets = 4
h_maxlength = 50


def trim_text(intext, first=False):
    intext_l = intext.split()
    if first:
        del intext_l[0]
    del intext_l[-1]
    print(intext_l)
    r_text = ' '.join(intext_l)
    return r_text


def highlight_list(h_text, h_word_list, h_tag_pre, h_tag_post, h_snippets, h_maxlength):
    h_words = list()
    highlighted_text = h_text
    snippets = list()
    if h_word_list:
        for h_word in h_word_list:
            replace_word = h_tag_pre + h_word + h_tag_post

            highlighted_text = highlighted_text.replace(h_word, replace_word)
            h_words.append(replace_word)
            print(highlighted_text)
        remain_text = highlighted_text

        if len(highlighted_text) <= h_maxlength:
            snippets.append(highlighted_text)
            return snippets

        if h_words:
            while len(snippets) < h_snippets:
                for h_w in h_words:
                    max_idx = round(h_maxlength) + len(h_w)
                    p_idx = remain_text.find(h_w)
                    if p_idx <= max_idx:
                        cut_text = remain_text[:max_idx - 1]
                        cut_text = trim_text(cut_text)
                        remain_text = remain_text[len(cut_text):]
                        snippets.append(cut_text)
                    elif p_idx > max_idx:
                        e_idx = p_idx + (round(h_maxlength / 2)) + len(h_w)
                        if e_idx <= len(remain_text):
                            cut_text = remain_text[p_idx - (round(h_maxlength/2) + len(h_w)):e_idx]
                            remain_text = remain_text[len(cut_text):]
                        else:
                            cut_text = remain_text[p_idx - (round(h_maxlength/2) + len(h_w)):len(remain_text)]
                            cut_text = trim_text(cut_text)
                            cut_idx = remain_text.find(cut_text)
                            remain_text = remain_text[:cut_idx] \
                                          + remain_text[cut_idx + len(cut_text):]
                        snippets.append(cut_text)
    return snippets
s = highlight_list(h_text, h_word_list,  h_tag_pre, h_tag_post, h_snippets, h_maxlength)
print(s)


# yourString = 'Hello'
# yourIndexToReplace = 1 #e letter
# newLetter = 'x'
# yourStringNew = ''.join((yourString[:yourIndexToReplace],newLetter,yourString[yourIndexToReplace+1:]))
# print(yourStringNew)
