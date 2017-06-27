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
	list_of_items = ['Incandescent energy', 'Coal', 'Fire rune', 'Air rune', 'Feather', 'Broad arrowheads', 'Maple logs', 'Water rune', 'Earth rune', 'Nature rune', 'Magic logs', 'Yew logs', 'Brilliant energy', 'Blood rune', 'Mind rune', 'Cannonball', 'Lustrous energy', 'Luminous energy', 'Dragon bones', 'Body rune', 'Mahogany plank', 'Death rune', 'Royal bolts', 'Polypore spore', 'Ascension bolts', 'Fishing bait', 'Rune arrow', 'Chaos rune', 'Bowstring', 'Ascension shard', 'Radiant energy', 'Ganodermic flake', 'Adamantite ore', 'Gold ore', 'Flax', 'Vial of water', 'Vibrant energy', 'Araxyte arrow', 'Mahogany logs', 'Raw shark', 'Shark', 'Soul rune', 'Rocktail', 'Adamant bar', 'Rune bar', 'Gold bar', 'Elder energy', 'Runite ore', 'Law rune', 'Raw lobster', 'Raw rocktail', 'Astral rune', 'Cosmic rune', 'Black dragon leather', 'Onyx bolts (e)', 'Steel bar', 'Magic shieldbow', 'Iron ore', 'Black dragonhide', 'Grenwall spikes', 'Mithril bar', 'Willow logs', 'Mud rune', 'Lobster', 'Swamp tar', 'Mithril ore', 'Adamant arrow', 'Snape grass', 'Soft clay', 'Magic notepaper', 'Steel arrow', 'Magic shieldbow (u)', 'Harralander tar', 'Mithril arrow', 'Teak plank', 'Thread', 'Oak plank', 'Dark arrow', 'Grimy dwarf weed', 'Dragon arrowheads', 'Grimy lantadyme', 'Airut bones', 'Gleaming energy', 'Infernal ashes', 'Frost dragon bones', 'Living minerals', 'Chitin scraps', 'Green dragon leather', 'Red chinchompa', 'Rune arrowheads', 'Eye of newt', 'Clean lantadyme', 'Rune essence', 'Raw tuna']
	list_of_file_names = []
	for i in range(len(list_of_items)):
		list_of_file_names.append(list_of_items[i].replace(' ', '_')+'.png')
	for i in range(len(list_of_items)):
		file_name_1 = 'screenshots/items/'+list_of_file_names[i]
		file_name_2 = 'screenshots/temp_items/'+list_of_file_names[i]
		if os.path.isfile(file_name_1):
			print('file exists', file_name_1)
			continue
		x = len(list_of_items[i])
		pyautogui.typewrite(list_of_items[i], random.random()/10)
		time.sleep(2)
		pyautogui.screenshot(file_name_2, region=(box_1_coords))
		for x in range(x):
			pyautogui.press('backspace')
			time.sleep(random.random()/10)
		time.sleep(1)



main()
