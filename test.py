import snscrape.modules.twitter as sntwitter


scraper=sntwitter.TwitterSearchScraper("Zemmour since:2021-11-20 lang:fr")
test=[]
j=0
for i,tweet in enumerate(scraper.get_items()):
        test.append(tweet.content)
        j=j+1
        print(j)
print(test)        
print(i)
print(j)
#print(tweet.id,tweet.content,"{}\n\n".format(i))

