
class Database():
    def __init__(self,url,username,password,namespace,database):
        self.username = username
        self.password = password
        self.namespace = namespace
        self.database = database
        self.url = url

    @staticmethod
    def ParseResponseForErrors(outcome):
      """
        Parses a SurrealDB response and raises an exception if an error is present.

        Args:
            outcome (dict): The SurrealDB response to parse.

        Returns:
            dict: The parsed response, or None if the outcome is None.

        Raises:
            SystemError: If an error is found in the response.
        """
      if outcome:
        if "result" in outcome:
            for item in outcome["result"]:
                if item["status"]=="ERR":
                    raise SystemError("Error in results: {0}".format(item["result"])) 
        
        if "error" in outcome:
            raise SystemError("Error in outcome: {0}".format(outcome["error"])) 

        return outcome
      else:
        return None
    
