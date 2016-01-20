import MySQLdb

# 1. import the mode: import MySQLdb.cursor
class MySQLClient:
    def __init__(self, host, port, user, password, database):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database

    def __enter__(self):
        print 'Get in __enter__'
        # 2. when connecting to the database, change the cursor class to 'cursorclass = MySQLdb.cursors.DictCursor'
        # 3. the query operation will return result like ret=('col1':'val1','col2':'val2')
        # 4. dict(ret) will convert the result to dict
        self.conn=MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, port=self.port)
        self.conn.select_db(self.database)
        self.cursor=self.conn.cursor()
        print 'Leave __enter__'
        return self
    
    def __exit__(self, type, value, trace):
        print 'Get in __exit__'
        self.cursor.close()
        self.conn.close()
        print 'Leave __exit__'

    def open(self):
        self.conn=MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, port=self.port)
        self.conn.select_db(self.database)
        self.cursor=self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close() 

    def queryOne(self, query, param=None):
        print 'Get in query...'
        rowList=[]
        if not param:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, param)
            
        result=self.cursor.fetchone()
        return result
    
    def queryList(self, query, param=None):
        print 'Get in query...'
        rowList=[]
        if not param:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, param)
            
        result=self.cursor.fetchall()
        for row in result: 
            rowList.append(row)
        return rowList

    def update(self, sql, param=None):
        if not param:
            return self.cursor.execute(sql, param)
        else:
            return self.cursor.execute(sql)
        self.conn.commit()

if __name__ == '__main__':
    import sys
    print sys.path
    with MySQLClient('10.100.141.39', 3306, 'pay_trade', 'pay_trade@123', 'pay_trade') as client:
        rowList=client.queryList('select * from pay_acct limit 3')
        print rowList
