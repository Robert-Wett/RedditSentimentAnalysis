import sys, json, requests
from textblob import TextBlob
from colorama import *
init()

def areyouhappy(username=None, depth=None):
    if username is None:
        username = "presidentobama"
    if depth is None:
        depth = 10
    else: depth = int(depth)

    url = r"http://www.reddit.com/user/"+username+r"/comments.json?limit=100"
    totalsent=0
    postcount=0
    comment_max = 500
    label = "*"*22
    pos=[]
    neg=[]

    r = requests.get(url)
    data = json.loads(r.text)

    try:
        posts = data['data']['children']
    except KeyError as e:
        if data['error'] == 429:
            print("Woops! Looks like we're being rate-limited.")
            return
        else:
            print("Sorry, something went wrong! -", data['error'])
            return

    if len(posts) == 0:
        print("Not enough posts to look at!")
        return

    for idx, c in enumerate(posts):
        c = c['data']
        try:
            # TODO: Check 'body_html' for <pre> tags to skip code...
            if len(c['body']) < comment_max:
                sentence = TextBlob(c['body'])
                if sentence.sentiment[0] > 0:
                    pos.append((sentence.string, sentence.sentiment[0]))
                else:
                    neg.append((sentence.string, sentence.sentiment[0]))
                totalsent += sentence.sentiment[0]
                postcount += 1
        except:
            pass

    psort = sorted(pos, key=lambda x: x[1], reverse=True)
    nsort = sorted(neg, key=lambda x: x[1])

    print(Fore.GREEN + label,"Top Positive Comments:", label, sep="\n")
    for idx, x in enumerate(psort):
        if idx < depth:
            print(Fore.RESET + '{0}: "{1}" (Rating: {2:.2f})'.format(idx+1, psort[idx][0], psort[idx][1] ), end="\n\n")
    print(Fore.RED + label,"Most Negative Comments:", label, sep="\n")
    for idx, x in enumerate(nsort):
        if idx < depth:
            print(Fore.RESET + '{0}: "{1}" (Rating: {2:.2f})'.format(idx+1, nsort[idx][0], nsort[idx][1]), end="\n\n")

    overall = totalsent/postcount
    if overall > 0:
        print("\n\n\nYou're a happy guy overall though, you're overall positivity is {0:.2f}".format(overall))
    else:
        print("\n\n\nYou're a candidate for the playahatas ball - you're overall negativity is {0:.2f}".format(overall))

try:
    areyouhappy(username=sys.argv[1])
except:
    areyouhappy()
