from cassandra.cluster import Cluster


class CassandraInstance:
    def __init__(self, keyspace):
        self.cluster = Cluster()
        self.session = self.cluster.connect(keyspace)

    def query(self, query):
        return self.session.execute(query)

    def insert_user(self, username, email, nome, time_stamp):
        s = 'INSERT INTO users (username, email, nome, time_stamp) ' + 'VALUES( \'' + username + '\',\'' + email + '\',\'' + nome + '\',\'' + time_stamp + '\')'
        self.query(s)
        print(s)

    def insert_event(self, username, video_id, time_stamp, event, time_passed):
        s = 'INSERT INTO events (user, video_id, time_stamp, event, segundos_passados) ' + 'VALUES( \'' + username + '\',' + video_id + ',\'' + time_stamp + '\',\'' + event + '\', ' + time_passed + ')'
        self.query(s)
        print(s)

    def insert_video(self, video_id, vid_publish_time, vid_author, vid_caption, vid_name, vid_tags):
        ## Must insert in all the tables
        temp_set = '{'
        for t in vid_tags:
            temp_set += '\''
            temp_set += t
            temp_set += '\''
            temp_set += ','
        temp_set = temp_set[:-1]
        temp_set += '}'


        ## Insert the video
        s1 = 'INSERT INTO videos (id, vid_publish_time, vid_author, vid_caption, vid_name, vid_tags ) VALUES ( %d, \'%s\', \'%s\', \'%s\', \'%s\', %s)' % (video_id, vid_publish_time, vid_author, vid_caption, vid_name, temp_set)

        ## Update video tags
        #s2 = str.format('INSERT INTO videos_by_tag ( tag, ids ) VALUES ')

        ## DISCLAIMER: Este driver não ceritifca a consistencia na tabela video_tags
        # INSERT INTO videos_by_tag ( tag, ids ) VALUES ( 'Tag' , {1,2,3,4});

        ## Update the videos_by_author table
        s3 = 'INSERT INTO videos_by_author ( vid_author, id, vid_caption, vid_name, vid_publish_time, vid_tags )\
                                VALUES ( \'%s\', %d, \'%s\', \'%s\', \'%s\', %s)' % ( vid_author, video_id, vid_caption, vid_name, vid_publish_time, temp_set)

        ## Ratings (0, 0)
        # INSERT INTO ratings (video_id, count, rating) VALUES (1, 23, 100);
        s4 = 'INSERT INTO ratings (video_id, count, rating )\
                            VALUES (%d, %d, %d)' % (video_id, 0, 0)

        ## Video_followers
        
        # INSERT INTO video_followers ( video_id, followers ) VALUES ( 1, {'cenas', 'nao'});
        s5 = 'INSERT INTO video_followers ( video_id, followers ) VALUES \
                                ( %d, {})' % video_id

        self.query(s1)
        print(s1)
        self.query(s3)
        print(s3)
        self.query(s4)
        print(s4)
        self.query(s5)
        print(s5)

    def update_user(self, username, field, value):
        query = 'UPDATE users SET %s=\'%s\' WHERE username=\'%s\'' % (field, value, username)
        self.query(query)
        print(query)

    def delete_user(self, username):
        query = 'DELETE FROM users WHERE username=\'%s\'' % username
        self.query(query)
        print(query)

    ## Returns a dicionary where key = table_name and value is a set of rows from that table
    def get_video_data(self, video_id):
        
        aggregated_data = dict()

        aggregated_data['videos'] = self.query('SELECT * FROM videos WHERE id='+str(video_id))
        aggregated_data['ratings'] = self.query('SELECT * FROM ratings WHERE video_id='+str(video_id))
        aggregated_data['video_followers'] = self.query('SELECT * FROM video_followers WHERE video_id='+str(video_id))

        return aggregated_data


    ## 3.02 1)
    def get_3comments_by_vid(self, video_id):
        query = 'select * from comments_by_vid where video_id = %d limit 3' % video_id
        return self.query(query)
    
    ## 3.02 7)
    def get_video_followers(self, video_id):
        query = 'select * from video_followers where video_id=%d' % video_id
        return self.query(query)

    ## 3.02 8)
    def get_user_comments(self, username):
        query = 'select comments from following where user=\'%s\'' % username
        return self.query(query)

    ## 3.02 11)
    def get_number_of_videos_by_tag(self, tag_name):
        query = 'select * from vid_tag_num'
        return self.query(query)


cass = CassandraInstance('cbd')

## INSERTING DATA
cass.insert_user('bom_nome', 'cenas@ua.pt', 'eu', '2019-11-21 12:35:14')
cass.insert_event('bom_nome', '1', '2019-11-21 12:35:14', 'VOLUME_DOWN', '129')
cass.insert_video(5, '2019-11-21 12:35:14', 'beta', 'Enjoy :)', 'Python Tutorial', ['Tag_1', 'Tag_2'])

## UPDATING DATA
cass.update_user('bom_nome', 'nome', 'Patrick Shyu')

## DELETING DATA
cass.delete_user('bom_nome')

## READING DATA
print(cass.get_video_data(1))