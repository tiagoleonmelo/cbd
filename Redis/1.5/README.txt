Structures Used

Set used for the users of our Message App, since there can never be two users with the same name
Set used for the followers of each user, as well as what users a given user follows
List used for the messages of each user, to enable having them sorted by time and indexed

Users are stored in				msg_app:users
Each user has its set of followers stored in 	msg_app:users:USERNAME:followers
The set of users they follow is in 		msg_app:users:USERNAME:follows
Each user's messages are stored in		msg_app:users:USERNAME:msgs
