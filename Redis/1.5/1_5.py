import redis

## Class that will act as a client of our msg app
# the structure essentially follows a directory scheme
# being the root msg_app

class Messenger:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)


    ## Adds a user to the system with the name passed as argument (acts as key and value to ease searching)
    def add_user(self, name):
        self.r.sadd("msg_app:users", name)


    ## Allows user_b to follow user_a, updates both "directories"
    def follow(self, user_a, user_b):
        if user_a.encode() not in self.r.smembers("msg_app:users") or user_b.encode() not in self.r.smembers("msg_app:users"):
            print("ERROR: Invalid parameters")
            return

        self.r.sadd("msg_app:users:"+user_a+":followers", user_b)
        self.r.sadd("msg_app:users:"+user_b+":follows", user_a)


    ## The user passed as argument sends a message msg to the system
    def store_msg(self, user, msg):
        if user.encode() not in self.r.smembers("msg_app:users"):
            print("ERROR: User does not exist")
            return

        self.r.lpush("msg_app:users:"+user+":msgs", msg)


    ## Called when user_a wants to read messages sent by user_b
    def read_msg(self, user_a, user_b):
        if user_a.encode() not in self.r.smembers("msg_app:users") or user_b.encode() not in self.r.smembers("msg_app:users"):
            print("ERROR: Invalid parameters")
            return

        if self.r.sismember("msg_app:users:"+user_a+":follows", user_b ):
            print(user_b + "'s messages: ", end="")
            s = self.r.lrange("msg_app:users:"+user_b+":msgs",0,-1)
            for m in s:
                print(m.decode(), end="; ")

            print("")
        else:
            print(user_a + " does not have permission to access " + user_b + "'s messages. Try following " + user_b + " first.")


    def get_followers(self, user):
        if user.encode() not in self.r.smembers("msg_app:users"):
            print("ERROR: User does not exist")
            return

        s = self.r.smembers("msg_app:users:"+user+":followers")
        print(user + "'s followers: ", end="")
        for m in s:
            print(m.decode(), end="; ")

        print("")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

m = Messenger()

## STATIC INTERACTION

# # Create users
# m.add_user("Tiago")
# m.add_user("TechLead")

# # Have the TechLead present himself
# m.store_msg("TechLead", "Hey, I'm the TechLead.")

# # Attempt to read TechLead's messages as Tiago and failing
# m.read_msg("Tiago", "TechLead")

# # Follow the TechLead as Tiago
# m.follow("TechLead", "Tiago") 

# # Attempt to read TechLead's messages as Tiago again
# m.read_msg("Tiago", "TechLead")

# # Checking out TechLead's Follower Set
# m.get_followers("TechLead")

op = -1

while op != 0:
    print("0 - Exit\n1 - Add user\n2 - Follow\n3 - Publish\n4 - Read messages\n5 - Show followers")
    op = int(input("Choose an option: "))

    if op == 1:
        name = input("What's the name of the user you want to add? ")
        m.add_user(name)

    elif op == 2:
        client = input("Who are you? ")
        influencer = input("Who do you want to follow? ")
        m.follow(influencer, client)

    elif op == 3:
        client = input("Who are you? ")
        msg = input("Insert your message ")
        m.store_msg(client, msg)

    elif op == 4:
        client = input("Who are you?")
        influencer = input("Whose messages do you want to read? ")
        m.read_msg(client, influencer)

    elif op == 5:
        client = input("Show whose followers? ")
        m.get_followers(client)
