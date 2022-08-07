import random, randfacts, json, requests, string
bad_words = ['$ex', '$exy', '@sshole', 'a$$hole', 'assh0le', 'asshole', 'asshol€', 'b00b', 'b1tch', 'bitch', 'boob', 'c0ck', 'cl1t', 'clit', 'cock', 'cum', 'd1ck', 'dick', 'fuck', 'g@y', 'gay', 'le$bian', 'lesb1an', 'lesbi@n', 'lesbian', 'l€sbian', 'n1gg', 'nigg', 'pen1s', 'peni$', 'penis', 'pu$$y', 'pussy', 'p€nis', 'runt', 'sex', 'sexy', 's€x', 's€xy', 't1ts', 't1tty', 'tit$', 'tits', 'titty', 'urm0m', 'urmom', 'v@gin@', 'vag1na', 'vagina']

topics = ["What's your favorite quote",
			"Think of something your own", 
			"What's your Favorite band", 
			"What's the time for you?", 
			"What's your favorite book?", 
			"What's your favorite song?", 
			"When did you join this Discord server?", 
			"If you could, would you go to space?", 
			"What skill would you like to have?", 
			"What do you do most of your time? (School/work don't count)", 
			"What is your favorite subject at school?", 
			"What is your favorite YouTube channel?", 
			"What battery percentage is your phone on?", 
			"What are your hobbies?", 
			"Do you play any sports?", 
			"If you could be an animal, what would you be?", 
			"If you could have any ability in the world, what would it be?", 
			"You can choose a super power but the first person to reply can choose a side effect",
			"What country do you always wanted/want to visit? Why?",
			"What place in the Universe would you like to visit?",
			"How many languages do you speak",
			"If you could learn any language in the world, what would it be?"]
		
get_fact = lambda: randfacts.get_fact()
get_topic = lambda: random.choice(topics)
def in_list(str_, list_):
    text = str_.lower().split()
    for element in text:
        for item in list_:
            if element.replace(item, "") != element:
                return True
    return False
def check_message(message):
    #return type: (action, message, delete_after (0 if it shouldnt be deleted))
    if in_list(message.content, bad_words):
        return ("del", f"Dont say bad words {message.author.mention}!", 5)
    
    return (None, None, None)


# def get_shower():
# 	data = requests.get('https://www.reddit.com/r/showerthoughts/top.json?sort=top&t=week&limit=100')

# 	data = json.loads(data.text)
# 	while True:
# 		data = requests.get('https://www.reddit.com/r/showerthoughts/top.json?sort=top&t=week&limit=100')

# 		data = json.loads(data.text)
# 		try:
# 			if data["message"] == "Too Many Requests":
# 				print("Too Many Requests")
# 		except KeyError:
# 			break
# 	data = data["data"]["children"][random.randint(0,99)]["data"]

# 	title = "\n\"" + data["title"] + "\""
# 	author = "    -" + data["author"] + "\n"
# 	return (title, author)

def get_shower():
	with open("data.json", "r", encoding="utf-8") as f:
		data = json.load(f)
		return random.choice(data["thoughts"])


length = random.randint(12,25)
lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
symbols = string.punctuation
    
all = lower + upper + num + symbols

temp = random.sample(all,length)

am = "".join(temp)
