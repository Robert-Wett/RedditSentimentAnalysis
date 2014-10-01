# Pull requests welcome!
# https://github.com/Robert-Wett/RedditSentimentAnalysis

import sys, json, requests
from textblob import TextBlob

def areyouhappy(username=None, outputjson=None):
    if username is None:
        username = "way_fairer"
    if outputjson is None:
        outputjson = False
    else: outputjson = True

    url = r"http://www.reddit.com/user/%s/comments.json?limit=100" % username
    totalsent, postcount = 0, 0
    pos, neg =[], []
    comment_max = 500
    label = "*"*30+"\n"
    depth = 10
    headers = {'User-Agent': "Reddit Sentiment Analysis Checker - /u/%s" % username}

    r = requests.get(url, headers=headers)
    try:
        data = json.loads(r.text)
    except ValueError as e:
        print "Sorry about that, Something went wrong :("
        return

    try:
        posts = data['data']['children']
    except KeyError as e:
        if data['error'] == 429:
            print "Woops! Looks like we're being rate-limited...."
        elif data['error'] == 404:
            print "Couldn't find that username - check the spelling and try again!"
        else:
            print "Sorry, something went wrong! -", data['error']
        return

    if len(posts) == 0:
        print "Not enough posts to look at!"
        return

    for idx, c in enumerate(posts):
        c = c['data']
        try:
            # TODO: Check 'body_html' for <pre> tags to skip code...
            if len(c['body']) < comment_max:
                sentence = TextBlob(c['body'].decode('utf-8'))
                if sentence.sentiment[0] > 0:
                    pos.append((sentence.string, sentence.sentiment[0]))
                else:
                    neg.append((sentence.string, sentence.sentiment[0]))
                totalsent += sentence.sentiment[0]
                postcount += 1
        except:
            # Super awesome exception handling.
            pass

    psort = sorted(pos, key=lambda x: x[1], reverse=True)
    nsort = sorted(neg, key=lambda x: x[1])
    overall = totalsent/postcount

    # I'll redo this to make proper json objects before exposing it
    if outputjson:
        print json.dumps([overall, psort, nsort])
        return

    print  label + username+"'s", "Top Positive Comments:\n", label
    for idx, x in enumerate(psort):
        if idx < depth:
            print '{0}: "{1}" (Rating: {2:.2%})'.format(idx+1, psort[idx][0], psort[idx][1])
    print "\n\n" + label, username+"'s", "Most Negative Comments:\n", label
    for idx, x in enumerate(nsort):
        if idx < depth:
            print '{0}: "{1}" (Rating: {2:.2%})'.format(idx+1, nsort[idx][0], nsort[idx][1])


    print "\n\n\n", label
    if overall > 0:
        print "{0} is a positive person overall though, with an overall positivity rating of {1:.2%}".format(username, overall)
    else:
        print "{0} is a candidate for the playahatas ball - {0} has an overall negativity rating of {1:.2%}".format(username, overall)


areyouhappy(username=username)
