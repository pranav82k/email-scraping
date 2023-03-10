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

    def insertion(self, sender_email_address, subject, email_body, summary):
        sql = "INSERT INTO records (sender_email_address, subject, email_body, summary) VALUES (%s, %s, %s, %s)"
        val = [sender_email_address, subject, email_body, summary]
        self.cursor.execute(sql, val)
        self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()