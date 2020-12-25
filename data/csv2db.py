import time
import pandas as pd
import sqlite3
# https://buttercoconut.xyz/74/
# time_pd = pd.DataFrame(0., columns=col, index=time_range)
# time_pd.to_csv("filename.csv", mode='w')
start = time.time()
bookdf = pd.read_csv("./goodbooks-10k/books.csv")
# bookdf = pd.read_csv("./books.csv")
print('bookdf:', bookdf.values.tolist())
print(time.time()-start)


# conn = sqlite3.connect("../db.sqlite3")
# bookdf.to_sql('api_googlebook', conn, schema=None, if_exists='append', index=False, index_label=None, chunksize=1000, dtype=None)
