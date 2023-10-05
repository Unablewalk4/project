import mysql.connector as mcon
import re
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import myfuncs

my_con = mcon.connect(
            host='localhost',
            user='root',
            password='hello@123',
            database='hospital')
mysql = my_con.cursor()
myfuncs.admnpnl_func()