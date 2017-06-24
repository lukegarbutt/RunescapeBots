# Takes in a list of items and looks up the corresponding items ge limits and returns them as a list

import re
import urllib.request

def pull_item_limit_webpage():
	wiki_source = urllib.request.urlopen('http://runescape.wikia.com/wiki/Calculator:Grand_Exchange_buying_limits') # opens the url of runescape wiki page that contains item limit info
	wiki_source = str(wiki_source.read()) # converts this ?binary? file to a human-readable text file. This gives us a human readable version of the source code for the page.
	return(wiki_source)

def parse_webpage(item_name, wiki_source):
	item_name = item_name.replace(' ','_') # strips out the spaces in our items and replaces them with '_' so that they are in the format we are looking for in the source code
	# wiki_source = '<td><a href="/wiki/Exchange:Impling_jar" title="Exchange:Impling jar">Impling jar</a></td><td>1,000</td></tr><tr><td><a href="/wiki/Exchange:Incandescent_energy" title="Exchange:Incandescent energy">Incandescent energy</a></td><td>25,000</td></tr><tr><td><a href="/wiki/Exchange:Incomplete_hydrix" title="Exchange:Incomplete hydrix">Incomplete hydrix</a></td><td>100</td></tr><tr><td><a href="/wiki/Exchange:Incomplete_pizza" title="Exchange:Incomplete pizza">Incomplete pizza</a></td><td>1,000</td></tr>'
	search_word = 'Exchange:'+item_name+'"' # creates a variable that contains the term we will search the source code for to locate the item
	split_text = re.split(r'{0}'.format(re.escape(search_word)), wiki_source, maxsplit=1, flags=0) # splits the source code into 2 at the position of the word we are looking for, this means that the ge limit of the item is the first number in the second element of the split_text variable
	result = re.search(r'[0-9,]+', split_text[1]) # tries to locate the first number in the second entry of our split_text list. This number is in the format (any number of digits) + (,) + (any number of digits). This allows us to find numbers such as 25,000
	limit = result.group(0) # this returns the correct values from our regex 'result' for more info try calling print(result) on the line above
	return(limit)

def find_ge_limit(item_names): # pass in item list, return item limits as list
	item_limits = []
	wiki_source = pull_item_limit_webpage() # fetches the source code of the wiki page containing item limit information
	for i in item_names:
		item_limits.append(parse_webpage(i, wiki_source)) # for each item parse the webpage and append its limit to item_limits
	for i in range(len(item_limits)):
		item_limits[i] = int(item_limits[i].replace(',', '')) # strip the commas out and replace with nothing. Also convert string to int
	return(item_limits)

item_names = ['Incandescent energy', 'Coal', 'Fire rune', 'Air rune', 'Feather', 'Broad arrowheads', 'Maple logs', 'Water rune', 'Earth rune', 'Nature rune', 'Magic logs', 'Yew logs', 'Brilliant energy', 'Blood rune', 'Mind rune', 'Cannonball', 'Lustrous energy', 'Luminous energy', 'Dragon bones', 'Body rune', 'Mahogany plank', 'Death rune', 'Royal bolts', 'Polypore spore', 'Ascension bolts', 'Fishing bait', 'Rune arrow', 'Chaos rune', 'Bowstring', 'Ascension shard', 'Radiant energy', 'Ganodermic flake', 'Adamantite ore', 'Gold ore', 'Flax', 'Vial of water', 'Vibrant energy', 'Araxyte arrow', 'Mahogany logs', 'Raw shark', 'Shark', 'Soul rune', 'Rocktail', 'Adamant bar', 'Rune bar', 'Gold bar', 'Elder energy', 'Runite ore', 'Law rune', 'Raw lobster', 'Raw rocktail', 'Astral rune', 'Cosmic rune', 'Black dragon leather', 'Onyx bolts (e)', 'Steel bar', 'Magic shieldbow', 'Iron ore', 'Black dragonhide', 'Grenwall spikes', 'Mithril bar', 'Willow logs', 'Mud rune', 'Lobster', 'Swamp tar', 'Mithril ore', 'Adamant arrow', 'Snape grass', 'Soft clay', 'Magic notepaper', 'Steel arrow', 'Magic shieldbow (u)', 'Harralander tar', 'Mithril arrow', 'Teak plank', 'Thread', 'Oak plank', 'Dark arrow', 'Grimy dwarf weed', 'Dragon arrowheads', 'Grimy lantadyme', 'Airut bones', 'Gleaming energy', 'Infernal ashes', 'Frost dragon bones', 'Living minerals', 'Chitin scraps', 'Green dragon leather', 'Red chinchompa', 'Rune arrowheads', 'Eye of newt', 'Clean lantadyme', 'Rune essence', 'Raw tuna']
x = find_ge_limit(item_names)
print(x)


