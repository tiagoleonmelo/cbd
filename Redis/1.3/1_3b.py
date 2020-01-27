import redis

## SimplePost Class
#
#  A class that allows basic interaction as a Redis Client

class SimplePost_Set:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host, port, db)
        self.USERS = "users" # Key set for users' names

    def saveUser(self, name):
        self.r.sadd(self.USERS, name)

    def getUser(self):
        return self.r.smembers(self.USERS)

    def getAllKeys(self):
        return self.r.keys()

class SimplePost_List:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host, port, db)
        self.USERS = "users_list" 

    def saveUser(self, name):
        self.r.lpush(self.USERS, name)

    def getUser(self):
        return self.r.lrange(self.USERS, 0, -1)

    def getAllKeys(self):
        return self.r.keys()

class SimplePost_HashMap:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host, port, db)
        self.USERS = "users_hmap" 

    def saveUser(self, name):
        self.r.hset(self.USERS, name, name)

    def getUser(self):
        return self.r.hgetall(self.USERS)

    def getAllKeys(self):
        return self.r.keys()

def main():
    # board = SimplePost_Set()
    # board = SimplePost_List()
    board = SimplePost_HashMap()
    users = {"Ana", "Pedro", "Maria", "Luís"}
    for user in users:
        board.saveUser(user)

    for u in board.getAllKeys():
        print(u.decode(), end=' ')

    print("")

    for u in board.getUser():
        print(u.decode(), end=' ')

    print("")


# Driver code to test the above class and call main

if __name__ == "__main__":
    main()

