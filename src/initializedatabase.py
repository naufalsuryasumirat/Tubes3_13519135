import sqlite3
import loginQueries as lq
import requestQueries as rq

if __name__ == "__main__":
    lq.createUserDatabase()
    rq.createDeadlineDatabase()
    lq.addUserEntry('naufalalexs', 'naufalalexs@gmail.com', 'naufal')