import feedparser;
import importSQL;

feed = feedparser.parse('http://www.profightdb.com/rss.xml');

for post in feed.entries:
    if "WWE" in post.title:
        print (post.title + ": " + post.link);
        importSQL.importUrl(post.link);