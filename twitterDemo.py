import tweepy
from tweepy import OAuthHandler
import _json
from tweepy.streaming import StreamListener
from tweepy import Stream
import csv
import numpy
import time
import pandas

file_output = open("output.txt",'w')
file_input = open("input.csv", "r")
class MyListener(StreamListener):
    # def on_data(self, data):
    #     try:
    #         with open("python.json","a") as f:
    #             f.write(data)
    #             return True
    #     except BaseException as e:
    #         print("Error on_data: %s" % str(e))
    #     return True
    def on_status(self,status):
        with open("output.txt","w") as f:
            writer = csv.writer(f)
            writer.writerow()

    # def on_error(self,status):
    #     print(status)
    #     return True



consumer_key = "0bOX47RdpzHaAi1D2PLeTJGJK"
consumer_secret = "18b5TY18STAcHIpA7wOc4K6A4Nqmwr9Xm91RDJZYEaH54mSMJd"
access_token = "1722598579-JU3jnYq5XpYDmgW1DI7IAKkVkRKZGxuVGz7dW66"
access_token_secret = "FdUgaDzVyDvl0HcXuz5ndm7RWn2bxd36phYeUn71D6b0l"





if __name__ == '__main__':

    myDataFrame = pandas.DataFrame(columns = ["movie_name","created_time","author","content"])
    input = []
    # row = pandas.DataFrame(["111","222","333","444"],["movie_name","created_time","author","content"])
    # myDataFrame = myDataFrame.append(row,ignore_index=True)
    # print(myDataFrame)

    while 1:
        line = file_input.readline()
        input.append(line)
        if not line:
            break
        pass


    # print(input.__len__())
    # print(input[0])


    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    i = 0
    while i<51:

        try:
            for tweet in tweepy.Cursor(api.search,q = input[i]).items(400):
                # print("tweet time: " +str(tweet.created_at))
                # print("tweet by: @" + tweet.user.screen_name)
                # print(tweet.text)
                myDataFrame.loc[myDataFrame.shape[0]] = [input[i][0:-1],tweet.created_at , tweet.user.screen_name, tweet.text]
            print(myDataFrame)

            time.sleep(10*60)
            i+=1
        except BaseException as e:
            print("------error happens---------")
            time.sleep(15 * 60)
            myDataFrame.to_csv("output.txt", index=False, sep='`')
            continue


    print(myDataFrame)
    myDataFrame.to_csv("output.txt",index = False,sep='`')
    # tweeters = api.home_timeline()
    # for tweet in tweeters:
    #     print(tweet.created_at)
    # twitter_stream = Stream(api.auth, listener = MyListener())
    # file.write(twitter_stream.filter(track = ["spiderman"]))

    # for tweet in tweepy.Cursor(api.friends).items():
    #     print(tweet._json)

    # user = api.get_user('twitter')
    # print(user.screen_name)
    # print(user.followers_count)
    # for friend in user.friends():
    #     print(friend.screen_name)


