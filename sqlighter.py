import sqlite3


def new_user(nid, nname):
    con = sqlite3.connect('DB/battle_users.db')
    cur = con.cursor()
    res = cur.execute('''SELECT id FROM users''').fetchall()
    lst = []
    if res:
        for i in res:
            for j in i:
                lst.append(j)
    if nid not in lst:
        count = cur.execute('''INSERT INTO users
                          (id, name, wins, loses, friends)
                          VALUES
                          (?, ?, 0, 0, 0);''', (nid, nname))
        con.commit()
        con.close()
