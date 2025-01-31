
class Database():
    def __init__(self,url,username,password,namespace,database):
        self.username = username
        self.password = password
        self.namespace = namespace
        self.database = database
        self.url = url

    @staticmethod
    def ParseResponseForErrors(outcome):
      if "result" in outcome:
        for item in outcome["result"]:
            if item["status"]=="ERR":
                raise SystemError("Step action error: {0}".format(item["result"])) 
      return outcome
