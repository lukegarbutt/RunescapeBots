#short script that will take in a list of items and search for them in the ge to be screenshot
import pyautogui
import time
import random
import os

def main():
	box_1_coords = (43,850,150,40)
	box_2_coords = (215,850,150,40)
	box_3_coords = (387,850,150,40)
	box_4_coords = (43,905,150,40)
	box_5_coords = (215,905,150,40)
	box_6_coords = (387,905,150,40)
	time.sleep(3)
	list_of_items = ['incandescent energy', 'coal', 'fire rune', 'air rune', 'feather', 'broad arrowheads', 'maple logs', 'water rune', 'earth rune', 'nature rune', 'magic logs', 'yew logs', 'brilliant energy', 'blood rune', 'mind rune', 'cannonball', 'lustrous energy', 'luminous energy', 'dragon bones', 'body rune', 'mahogany plank', 'death rune', 'royal bolts', 'polypore spore', 'ascension bolts', 'fishing bait', 'rune arrow', 'chaos rune', 'bowstring', 'ascension shard', 'radiant energy', 'ganodermic flake', 'adamantite ore', 'gold ore', 'flax', 'vial of water', 'vibrant energy', 'araxyte arrow', 'mahogany logs', 'raw shark', 'shark', 'soul rune', 'rocktail', 'adamant bar', 'rune bar', 'gold bar', 'elder energy', 'runite ore', 'law rune', 'raw lobster', 'raw rocktail', 'astral rune', 'cosmic rune', 'black dragon leather', 'onyx bolts (e)', 'steel bar', 'magic shieldbow', 'iron ore', 'black dragonhide', 'grenwall spikes', 'mithril bar', 'willow logs', 'mud rune', 'lobster', 'swamp tar', 'mithril ore', 'adamant arrow', 'snape grass', 'soft clay', 'magic notepaper', 'steel arrow', 'magic shieldbow (u)', 'harralander tar', 'mithril arrow', 'teak plank', 'thread', 'oak plank', 'dark arrow', 'grimy dwarf weed', 'dragon arrowheads', 'grimy lantadyme', 'airut bones', 'gleaming energy', 'infernal ashes', 'frost dragon bones', 'living minerals', 'chitin scraps', 'green dragon leather', 'red chinchompa', 'rune arrowheads', 'eye of newt', 'clean lantadyme', 'rune essence', 'raw tuna']
	list_of_file_names = []
	for i in range(len(list_of_items)):
		list_of_file_names.append(list_of_items[i].replace(' ', '_')+'.png')
	print(list_of_items)
	print(list_of_file_names)
	for i in range(len(list_of_items)):
		file_name_1 = 'screenshots/items/'+list_of_file_names[i]
		file_name_2 = 'screenshots/temp_items/'+list_of_file_names[i]
		if os.path.isfile(file_name_1):
			print('file exists', file_name_1)
			continue
		x = len(list_of_items[i])
		pyautogui.typewrite(list_of_items[i], random.random()/20)
		time.sleep(2)
		pyautogui.screenshot(file_name_2, region=(box_1_coords))
		for x in range(x):
			pyautogui.press('backspace')
			time.sleep(random.random()/20)
		#time.sleep(10)



main()
