import sqlite3


class DbObject():
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()

        # create tables...
        cmd = """CREATE TABLE IF NOT EXISTS tbl_users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR NOT NULL,
            name VARCHAR NOT NULL,
            email VARCHAR,
            passwd VARCHAR NOT NULL,
            active INTEGER NOT NULL)"""
        self.curs.execute(cmd)
        self.conn.commit()
        # self.conn.close()

        cmd = """CREATE TABLE IF NOT EXISTS tbl_curr_user(
            currid INTEGER,
            active INTEGER NOT NULL)"""
        self.curs.execute(cmd)
        self.conn.commit()
        self.conn.close()

        # reset tbl_curr_user to null (truncate)..
        self.trc_tbl('tbl_curr_user')

        # check if admin login already created...
        if(self.chk_login_pwd('admin', 'admin123') == 0):
            # insert default admin login
            self.ins_tbl_users('admin', 'Administrator',
                               'admin@myappdomain.com', 'admin123', 1)

    # insert into table tbl_B...
    def ins_tbl_users(self, login, name, email, passwd, active):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = """INSERT INTO tbl_users(login, name, email, passwd, active)
                    VALUES(?,?,?,?,?)"""
        data_tuple = (login, name, email, passwd, active)
        self.curs.execute(sqltext, data_tuple)
        self.conn.commit()
        self.conn.close()

    def viw_tbl_users(self):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = "SELECT * FROM tbl_users"
        self.curs.execute(sqltext)
        rows = self.curs.fetchall()
        self.conn.close()
        return rows

    def chk_login_pwd(self, login, pwd):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = "SELECT EXISTS(SELECT 1 FROM tbl_users WHERE login='{}' AND passwd='{}' LIMIT 1)".format(
            login, pwd)
        self.curs.execute(sqltext)
        row = self.curs.fetchone()
        self.conn.close()
        return row[0]

    def chk_exist_user(self, login):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = "SELECT EXISTS(SELECT 1 FROM tbl_users WHERE login='{}' LIMIT 1)".format(
            login)
        self.curs.execute(sqltext)
        row = self.curs.fetchone()
        self.conn.close()
        return row[0]

    def get_user_id(self, login):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = "SELECT id FROM tbl_users WHERE login='{}' LIMIT 1".format(
            login)
        self.curs.execute(sqltext)
        row = self.curs.fetchone()
        self.conn.close()
        return row[0]

    def get_user_name(self, id):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = "SELECT name FROM tbl_users WHERE id='{}' LIMIT 1".format(
            id)
        self.curs.execute(sqltext)
        row = self.curs.fetchone()
        self.conn.close()
        return row[0]

    def get_user_email(self, id):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = "SELECT email FROM tbl_users WHERE id='{}' LIMIT 1".format(
            id)
        self.curs.execute(sqltext)
        row = self.curs.fetchone()
        self.conn.close()
        return row[0]

    def get_user_pswd(self, id):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = "SELECT passwd FROM tbl_users WHERE id='{}' LIMIT 1".format(
            id)
        self.curs.execute(sqltext)
        row = self.curs.fetchone()
        self.conn.close()
        return row[0]

    def upd_curr_user(self, id):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = """INSERT INTO tbl_curr_user(currid,active)
                    VALUES(?,?)"""
        data_tuple = (id, 1)
        self.curs.execute(sqltext, data_tuple)
        self.conn.commit()
        self.conn.close()

    def upd_user_passwd(self, id, nupwd):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = """UPDATE tbl_users SET passwd = '{}' WHERE id = {}""".format(
            nupwd, id)
        print(sqltext)
        self.curs.execute(sqltext)
        self.conn.commit()
        self.conn.close()

    def trc_tbl(self, tbl_name):
        self.conn = sqlite3.connect(self.dbname)
        self.curs = self.conn.cursor()
        sqltext = "DELETE FROM "+tbl_name
        self.curs.execute(sqltext)
        self.conn.commit()
        self.conn.close()
        # return 1
