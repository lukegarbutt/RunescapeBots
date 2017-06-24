# Takes in an item and looks up the corresponding items ge limit and returns it

import re
import urllib.request

wiki_source = urllib.request.urlopen('http://runescape.wikia.com/wiki/Calculator:Grand_Exchange_buying_limits')
wiki_source = str(wiki_source.read())

def find_ge_limit(item_name, wiki_source):
	item_name = item_name.replace(' ','_')
	# wiki_source = '<td><a href="/wiki/Exchange:Impling_jar" title="Exchange:Impling jar">Impling jar</a></td><td>1,000</td></tr><tr><td><a href="/wiki/Exchange:Incandescent_energy" title="Exchange:Incandescent energy">Incandescent energy</a></td><td>25,000</td></tr><tr><td><a href="/wiki/Exchange:Incomplete_hydrix" title="Exchange:Incomplete hydrix">Incomplete hydrix</a></td><td>100</td></tr><tr><td><a href="/wiki/Exchange:Incomplete_pizza" title="Exchange:Incomplete pizza">Incomplete pizza</a></td><td>1,000</td></tr>'
	search_word = 'Exchange:'+item_name
	print(search_word)
	split_text = re.split(r'{0}'.format(search_word), wiki_source, maxsplit=1, flags=0)
	result = re.search(r'(\d*),(\d*)', split_text[1])
	limit = result.group(0)
	return(limit)

item_names = ['Incandescent energy', 'Coal', 'Fire rune', 'Air rune', 'Feather', 'Broad arrowheads', 'Maple logs', 'Water rune', 'Earth rune', 'Nature rune', 'Magic logs', 'Yew logs', 'Brilliant energy', 'Blood rune', 'Mind rune', 'Cannonball', 'Lustrous energy', 'Luminous energy', 'Dragon bones', 'Body rune', 'Mahogany plank', 'Death rune', 'Royal bolts', 'Polypore spore', 'Ascension bolts', 'Fishing bait', 'Rune arrow', 'Chaos rune', 'Bowstring', 'Ascension shard', 'Radiant energy', 'Ganodermic flake', 'Adamantite ore', 'Gold ore', 'Flax', 'Vial of water', 'Vibrant energy', 'Araxyte arrow', 'Mahogany logs', 'Raw shark', 'Shark', 'Soul rune', 'Rocktail', 'Adamant bar', 'Rune bar', 'Gold bar', 'Elder energy', 'Runite ore', 'Law rune', 'Raw lobster', 'Raw rocktail', 'Astral rune', 'Cosmic rune', 'Black dragon leather', 'Onyx bolts (e)', 'Steel bar', 'Magic shieldbow', 'Iron ore', 'Black dragonhide', 'Grenwall spikes', 'Mithril bar', 'Willow logs', 'Mud rune', 'Lobster', 'Swamp tar', 'Mithril ore', 'Adamant arrow', 'Snape grass', 'Soft clay', 'Magic notepaper', 'Steel arrow', 'Magic shieldbow (u)', 'Harralander tar', 'Mithril arrow', 'Teak plank', 'Thread', 'Oak plank', 'Dark arrow', 'Grimy dwarf weed', 'Dragon arrowheads', 'Grimy lantadyme', 'Airut bones', 'Gleaming energy', 'Infernal ashes', 'Frost dragon bones', 'Living minerals', 'Chitin scraps', 'Green dragon leather', 'Red chinchompa', 'Rune arrowheads', 'Eye of newt', 'Clean lantadyme', 'Rune essence', 'Raw tuna']
item_limits = []
for i in item_names:
	print(i, item_limits)
	item_limits.append(find_ge_limit(i, wiki_source))
print(item_names)
print(item_limits)
print(find_ge_limit('Onyx bolts (e)', wiki_source))