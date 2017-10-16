import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect('seasons.db')

df = pd.read_sql(sql = 'select * from season', con = conn)

# преобразовать команды в двоичные числа - степени 2

print (df)

# multiple regression {y,w} = K + x1*w1 + x2*w2 ... xn*w2
# dependent variable

#