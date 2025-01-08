
class Database():
    def __init__(self,url,username,password,namespace,database):
        self.username = username
        self.password = password
        self.namespace = namespace
        self.database = database
        self.url = url
