import tweepy
from tweepy import OAuthHandler
import _json
from tweepy.streaming import StreamListener
from tweepy import Stream
import csv
import numpy
import time
import pandas

file_output = open("output.txt",'w')    # file of output data(not clean)
file_input = open("input.csv", "r")     # name of movies

# rewrite MyListener.on_data function to receive the stream of tweepy
class MyListener(StreamListener):
    #override the on_data function
    def on_data(self, data):
        try:
            with open("python.json","a") as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    # override the on_status function
    def on_status(self,status):
        with open("output.txt","w") as f:
            writer = csv.writer(f)
            writer.writerow()

    # override on_error function
    def on_error(self,status):
        print(status)
        return True



consumer_key = "0bOX47RdpzHaAi1D2PLeTJGJK"          # api key
consumer_secret = "18b5TY18STAcHIpA7wOc4K6A4Nqmwr9Xm91RDJZYEaH54mSMJd"  # api secret
access_token = "1722598579-JU3jnYq5XpYDmgW1DI7IAKkVkRKZGxuVGz7dW66"     # token
access_token_secret = "FdUgaDzVyDvl0HcXuz5ndm7RWn2bxd36phYeUn71D6b0l"   # token secret


# interface of api model
if __name__ == '__main__':

    # create a dataFrame to store the data
    myDataFrame = pandas.DataFrame(columns = ["movie_name","created_time","author","content"])
    input = []  # input stored the name of movies

    # add movie names into input
    while 1:
        line = file_input.readline()
        input.append(line)
        if not line:
            break
        pass


    # use OAuth to identify the api key
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)  # return api object

    # start to download tweet on twitter. Since twitter permits 180 response per 15 minutes.
    # so, I try to sleep function 10 minutes after every loop of return 400 items
    i = 0
    while i<1:

        try:
            for tweet in tweepy.Cursor(api.search,q = "#"+input[i]).items(400):     # search tweets by movie names

                myDataFrame.loc[myDataFrame.shape[0]] = [input[i][0:-1],tweet.created_at , tweet.user.screen_name, tweet.text]  # delete \n in data
            print(myDataFrame)
            print("-------sleep 10 min---------")      # sleep 10 minutes in every loop
            time.sleep(10*60)
            i+=1
        except BaseException as e:
            print("------error happens---------")
            myDataFrame.to_csv("output123.txt", index=False, sep='`')
            file_output.close()
            file_input.close()

    print(myDataFrame)
    myDataFrame.to_csv("output123.txt",index = False,sep='`')       # save row data
    file_output.close()     # close ouput file

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


