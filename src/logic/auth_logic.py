from utils.dal import DAL

class AuthLogic:

    def __init__(self):
        self.dal = DAL()

    def is_email_taken(self, email):
        sql = "SELECT EXISTS(SELECT * FROM users WHERE email = %s) AS is_taken" # returns 1 if exists or 0 if does'nt exist
        result = self.dal.get_scalar(sql, (email, ))
        return result["is_taken"] == 1

    def add_user(self, user):
        sql = "INSERT INTO users VALUES(DEFAULT, %s, %s, %s, %s, %s)"
        params = (user.first_name, user.last_name, user.email, user.password, user.role_id)
        self.dal.insert(sql, params)

    def get_user(self, credentials):
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        user = self.dal.get_scalar(sql, (credentials.email, credentials.password))
        return user 

    def close(self):
        self.dal.close()

        