import sqlite3
import time

with sqlite3.connect('database.db') as db:
    cur = db.cursor()

    def newuser(userid):
        cur.execute(" INSERT INTO base (userid, admin, milk, state, drink, size) VALUES(?, ?, ?, ?, ?, ?) ", (userid, 0, 0, 0, "", 1))
        return db.commit()

    def check(userid):
        user = cur.execute(" SELECT * FROM base WHERE userid=? ", (userid,)).fetchall()
        return bool(len(user))
    
    def getstate(userid):
        state = cur.execute(" SELECT state FROM base WHERE userid=? ", (userid,)).fetchone()
        return state[0]
    
    def setstate(userid, state):
        cur.execute(" UPDATE base SET state=? WHERE userid=?", (state, userid))
        return db.commit()
    
    def getdrink(userid):
        drink = cur.execute(" SELECT drink FROM base WHERE userid=? ", (userid,)).fetchone()
        return drink[0]
    
    def setdrink(userid, drink):
        cur.execute(" UPDATE base SET drink=? WHERE userid=?", (drink, userid))
        return db.commit()
    
    def getsize(userid):
        size = cur.execute(" SELECT size FROM base WHERE userid=? ", (userid,)).fetchone()
        return size[0]
    
    def setsize(userid, size):
        cur.execute(" UPDATE base SET size=? WHERE userid=?", (size, userid))
        return db.commit()
    
    def getmilk(userid):
        milk = cur.execute(" SELECT milk FROM base WHERE userid=? ", (userid,)).fetchone()
        return milk[0]
    
    def setmilk(userid, milk):
        cur.execute(" UPDATE base SET milk=? WHERE userid=?", (milk, userid))
        return db.commit()
        
    def getadmin(userid):
        admin = cur.execute(" SELECT admin FROM base WHERE userid=? ", (userid,)).fetchone()
        return admin[0]

    def getbase():
        #cur.
        pass
