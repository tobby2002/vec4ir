import ir.text_preprocessing as textcleaning
txtclean = textcleaning.TextPreprocessing()
source_doc_stem = txtclean.lemmatize_raw_text(txtclean.preprocess_raw_text('trees tree and ok bolt nult'))
print('source_doc_stem:%s' % source_doc_stem)