import mysql.connector


class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def insertion(self, summary):
        sql = "INSERT INTO records (summary) VALUES (%s)"
        val = [summary]
        self.cursor.execute(sql, val)
        self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    #
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="",
    #     database="email_scrapping",
    #     connect_timeout=60
    # )

    # Check if the connection is valid
    # if mydb.is_connected():
    #     print("MySQL connection is valid")
    #     if mydb.ping():
    #         print("Ping successful")
    #     else:
    #         print("Ping failed")
    # else:
    #     print("MySQL connection is not valid")
#
#     mycursor = mydb.cursor()
#
#
# def insertion(summary):
#     # sql = "INSERT INTO email_scrapping (name, address) VALUES (%s, %s)"
#     sql = "INSERT INTO records (summary) VALUES (%s)"
#     # val = ("John", "Highway 21")
#     val = [summary]
#     mycursor.execute(sql, val)
#
#     mydb.commit()
#
# mydb.close()
