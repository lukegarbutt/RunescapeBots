#RUN AS ADMINISTRATOR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import pyautogui
import pytesseract
import cv2
import numpy
import PIL
import os
import random
import time
import pickle
import operator

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

class item():#simple for now, but in future maybe pull ge limits and items from a website??
	def __init__(self, item, limit, image, image_path):
		self.item = item
		self.limit = limit
		self.image = image
		self.image_path = image_path
		self.available_to_buy = limit

	def set_bought_at(self, price):
		self.bought_at = price

	def set_sold_at(self, price):
		self.sold_at = price

	def set_box_containing_item(self, box_coords):
		self.box_loc = box_coords

	def set_time_bought_at(self, time):
		self.time_bought_at = time

	def set_time_placed_buy_offer_at(self, time):
		self.time_placed_buy_offer_at = time

	def update_available_to_buy(self, number):
		self.available_to_buy = number

	def set_number_to_buy(self, number):
		self.number_to_buy = number

def initialise_items():
	#item_names = ['Coal', 'Air rune', 'Water rune', 'Earth rune', 'Fire rune', 'Law rune', 'nature rune', 'Pure essence', 'Mind rune', 'Chaos rune', 'Death rune', 'Cosmic rune']
	#item_limits = [25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000]
	#members item list
	item_names = ['incandescent energy', 'coal', 'fire rune', 'air rune', 'feather', 'broad arrowheads', 'maple logs', 'water rune', 'earth rune', 'nature rune', 'magic logs', 'yew logs', 'brilliant energy', 'blood rune', 'mind rune', 'cannonball', 'lustrous energy', 'luminous energy', 'dragon bones', 'body rune', 'mahogany plank', 'death rune', 'royal bolts', 'polypore spore', 'ascension bolts', 'fishing bait', 'rune arrow', 'chaos rune', 'bowstring', 'ascension shard', 'radiant energy', 'ganodermic flake', 'adamantite ore', 'gold ore', 'flax', 'vial of water', 'vibrant energy', 'araxyte arrow', 'mahogany logs', 'raw shark', 'shark', 'soul rune', 'rocktail', 'adamant bar', 'rune bar', 'gold bar', 'elder energy', 'runite ore', 'law rune', 'raw lobster', 'raw rocktail', 'astral rune', 'cosmic rune', 'black dragon leather', 'onyx bolts (e)', 'steel bar', 'magic shieldbow', 'iron ore', 'black dragonhide', 'grenwall spikes', 'mithril bar', 'willow logs', 'mud rune', 'lobster', 'swamp tar', 'mithril ore', 'adamant arrow', 'snape grass', 'soft clay', 'magic notepaper', 'steel arrow', 'magic shieldbow (u)', 'harralander tar', 'mithril arrow', 'teak plank', 'thread', 'oak plank', 'dark arrow', 'grimy dwarf weed', 'dragon arrowheads', 'grimy lantadyme', 'airut bones', 'gleaming energy', 'infernal ashes', 'frost dragon bones', 'living minerals', 'chitin scraps', 'green dragon leather', 'red chinchompa', 'rune arrowheads', 'eye of newt', 'clean lantadyme', 'rune essence', 'raw tuna']
	#members item limits
	item_limits = [25000, 25000, 25000, 25000, 10000, 10000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 10000, 25000, 25000, 10000, 25000, 10000, 25000, 10000, 30000, 10000, 10000, 10000, 25000, 10000, 10000, 25000, 28000, 25000, 25000, 25000, 10000, 25000, 10000, 25000, 20000, 10000, 25000, 10000, 10000, 10000, 10000, 25000, 25000, 25000, 20000, 20000, 25000, 25000, 10000, 25000, 10000, 5000, 25000, 10000, 5000, 10000, 25000, 25000, 10000, 5000, 25000, 10000, 10000, 10000, 500, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 25000, 5000, 10000, 10000, 20000, 10000, 20000, 10000, 10000, 10000, 25000, 20000]
	#f2p item names
	#item_names = []
	#f2p item limits
	#item_limits = []
	for i in range(len(item_names)):
		item_limits[i] = item_limits[i]-10
	file_path = 'C:/Users/luke_/Desktop/Python stuff/Script Stuff/Runescape/images/'
	item_images_paths = []
	item_images = []
	for i in range(len(item_names)):
		end_of_path = item_names[i].replace(" ", "") + '.png'
		item_images_paths.append(file_path+end_of_path)
	for i in range(len(item_names)):
		item_images.append(cv2.imread(item_images_paths[i]))
	list_of_items = []
	for i in range(len(item_names)):
		name = item_names[i]
		limit = item_limits[i]
		image = item_images[i]
		image_path = item_images_paths[i]
		list_of_items.append(item(name, limit, image, image_path))
	return(list_of_items)

def tesser_image(image):
	image = cv2.resize(image, (0,0), fx=2, fy=2)
	ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
	#cv2.imshow('im', image)
	#cv2.waitKey(0)
	image = PIL.Image.fromarray(image, 'RGB')
	txt = pytesseract.image_to_string(image)
	txt = txt.replace(",", "")
	txt = txt.replace(" ", "")
	if len(txt) == 0:
		txt = pytesseract.image_to_string(image, config='-psm 10')
	try:
		txt = int(txt)
	except:
		txt_list = list(txt)
		for i in range(len(txt)):
			if txt_list[i] == 'B':
				txt_list[i] = '8'
			elif txt_list[i] == 'l':
				txt_list[i] = '1'
			elif txt_list[i] == 'L':
				txt_list[i] = '1'
			elif txt_list[i] == 'i':
				txt_list[i] = '1'
			elif txt_list[i] == 'I':
				txt_list[i] = '1'
			elif txt_list[i] == 'o':
				txt_list[i] = '0'
			elif txt_list[i] == 'O':
				txt_list[i] = '0'
			elif txt_list[i] == 'z':
				txt_list[i] = '2'
			elif txt_list[i] == 'Z':
				txt_list[i] = '2'
			elif txt_list[i] == 'Q':
				txt_list[i] = '0'
			elif txt_list[i] == 's':
				txt_list[i] = '5'
			elif txt_list[i] == 'S':
				txt_list[i] = '5'
			elif txt_list[i] == '.':
				txt_list[i] = '9'
			elif txt_list[i] == ':':
				txt_list[i] = '8'


		if len(txt_list)>1:
			txt = int(''.join(txt_list))
		else:
			txt = int(txt_list[0])
	return(txt)

def screengrab_as_numpy_array(location):
	im = numpy.array(PIL.ImageGrab.grab(bbox=(location[0],location[1],location[2],location[3])))
	im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	#cv2.imshow('im', im)
	#cv2.waitKey(0)
	return(im)

#print(tesser_image(screengrab_as_numpy_array((1179, 427, 1306, 455)))) #how to test tesser

def main():
	list_of_items_to_buy = initialise_items()
	list_of_items_on_cooldown = []
	list_of_locations_of_offer_boxes = []
	for i in pyautogui.locateAllOnScreen('images/offerbox.png'):
		list_of_locations_of_offer_boxes.append(i)
	print(len(list_of_locations_of_offer_boxes))
	in_use_boxes = []
	list_of_items_in_ge_buying = []
	list_of_items_in_ge_selling = []
	time_of_last_action = time.time()
	amount_of_money = 90000000
	time_to_wait = random.randrange(100, 250)
	profit = 0
	total_trades_completed = 0

	with open("dict_of_items_with_scores.txt", "rb") as fp:   #Pickling
		items_with_scores = pickle.load(fp)
	print(items_with_scores)
	print(len(items_with_scores))

	#creating a ranked order based on score
	new_list_of_items_to_buy = []
	sorted_items_with_scores = sorted(items_with_scores.items(), key=operator.itemgetter(1))
	sorted_items_with_scores = sorted_items_with_scores[::-1]

	for i in range(len(sorted_items_with_scores)):
		item_name = sorted_items_with_scores[i][0]
		for j in list_of_items_to_buy:
			if j.item == item_name:
				new_list_of_items_to_buy.append(j)
	#print(new_list_of_items_to_buy)
	#print(len(new_list_of_items_to_buy))
	for i in list_of_items_to_buy:
		if i not in new_list_of_items_to_buy:
			new_list_of_items_to_buy.append(i)
	#print(new_list_of_items_to_buy)
	#print(len(new_list_of_items_to_buy))
	list_of_items_to_buy = new_list_of_items_to_buy

	#reversing the list to get scores for items I otherwise wouldn't have
	list_of_items_to_buy = list_of_items_to_buy[::-1]



	#popping a few items from the front of the list and putting them at the back to avoid ge limits
	#print(list_of_items_to_buy[0].item)
	#for i in range(6):
	#	list_of_items_to_buy.append(list_of_items_to_buy.pop(0))
	#print(list_of_items_to_buy[0].item)
	#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

	print('Starting in 15 seconds')
	time.sleep(12)
	print('Starting in 3 seconds')
	time.sleep(3)
	while(True): #can improve the completed offer section using the fact theres a different colour box for a buy or a sell
		if pyautogui.locateOnScreen('images/completedselloffer.png') or pyautogui.locateOnScreen('images/completedbuyoffer.png'):
			time_of_last_action = time.time()
			buy_or_sell, item_completed = buy_or_sell_check(list_of_items_in_ge_buying, list_of_items_in_ge_selling)
			if buy_or_sell != None:
				if buy_or_sell == 'buy':
					item_completed.set_time_bought_at(time.time())
					item_completed.update_available_to_buy(item_completed.available_to_buy-item_completed.number_to_buy)
					collect_money_or_items(item_completed)
					
					if time.time()-item_completed.time_placed_buy_offer_at < 1800:
						sell_items(item_completed) #and append lists correctly
					else:
						find_new_sell_price_and_sell_at_it(item_completed)
						item_completed.update_available_to_buy(item_completed.available_to_buy-1)
						list_of_items_on_cooldown.append([item_completed, 1, time.time()])

					#sell_items(item_completed) #and append lists correctly

					list_of_items_in_ge_buying.remove(item_completed)
					list_of_items_in_ge_selling.append(item_completed)
					list_of_items_on_cooldown.append([item_completed, item_completed.number_to_buy, time.time()])

				elif buy_or_sell == 'sell':
					list_of_items_in_ge_selling.remove(item_completed)
					in_use_boxes.remove(item_completed.box_loc)
					list_of_locations_of_offer_boxes.append(item_completed.box_loc)
					collect_money_or_items(item_completed) #and append lists correctly
					amount_of_money += item_completed.sold_at*item_completed.number_to_buy
					print('amount of money', amount_of_money)
					if item_completed.item in items_with_scores.keys():
						items_with_scores[item_completed.item] = (items_with_scores[item_completed.item]+(5*(item_completed.bought_at - item_completed.sold_at)*(item_completed.number_to_buy)/(time.time()-item_completed.time_placed_buy_offer_at)))/6
					else:
						items_with_scores[item_completed.item] = (item_completed.bought_at - item_completed.sold_at)*(item_completed.number_to_buy)/(time.time()-item_completed.time_placed_buy_offer_at)
					if item_completed.available_to_buy > item_completed.limit * 0.2:
						list_of_items_to_buy.insert(0, item_completed)

					print(item_completed.item)
					print((item_completed.bought_at - item_completed.sold_at)*(item_completed.number_to_buy)/(time.time()-item_completed.time_placed_buy_offer_at))
					#print(items_with_scores)
					profit += (item_completed.bought_at - item_completed.sold_at)*(item_completed.number_to_buy)
					print('Total profit so far is:', profit)
					total_trades_completed += 1
					print('total trades completed so far:', total_trades_completed)


					with open("dict_of_items_with_scores.txt", "wb") as fp:   #Pickling
						pickle.dump(items_with_scores, fp)

		elif len(list_of_locations_of_offer_boxes) > 0 and len(list_of_items_to_buy) > 0:
			time_of_last_action = time.time()
			list_of_locations_of_offer_boxes, list_of_items_to_buy, in_use_boxes, list_of_items_in_ge_buying, amount_of_money, item_used = find_item_prices(list_of_locations_of_offer_boxes, list_of_items_to_buy, in_use_boxes, list_of_items_in_ge_buying, amount_of_money)
			item_used.update_available_to_buy(item_used.available_to_buy-1)
			list_of_items_on_cooldown.append([item_used, 1, time.time()])

		elif int(time.time() - time_of_last_action) > 100:
			if int(time.time() - time_of_last_action) > time_to_wait:
				#print(time_to_wait, 'from random loop')
				time_of_last_action = time.time()
				time_to_wait = random.randrange(100, 250)
				pyautogui.click(pyautogui.locateCenterOnScreen('images/salehistorytab.png'))
				time.sleep(10)
				pyautogui.click(pyautogui.locateCenterOnScreen('images/grandexchangetab.png'))
				time.sleep(5)
		else:
			time.sleep(5)

		for i in range(len(list_of_items_on_cooldown)):
			if time.time()-list_of_items_on_cooldown[i][2]>14400:
				##list_of_items_to_buy.append(list_of_items_on_cooldown[i])
				#list_of_items_to_buy.insert(0, list_of_items_on_cooldown[i])
				list_of_items_on_cooldown[i][0].update_available_to_buy(list_of_items_on_cooldown[i][0].available_to_buy + list_of_items_on_cooldown[i][1])
				if list_of_items_on_cooldown[i][0] not in list_of_items_to_buy:
					list_of_items_to_buy.insert(0, list_of_items_on_cooldown[i][0])
				list_of_items_on_cooldown.pop(i)


def sell_items(item_completed):
	time.sleep(1)
	pyautogui.click(pyautogui.center(pyautogui.locateOnScreen('images/sellbag.png', region=(item_completed.box_loc))))
	time.sleep(1)
	pyautogui.click(1159, 431) #location of item in inv
	time.sleep(1)
	pyautogui.click(987, 524) #location of price box hard coded
	time.sleep(1)
	pyautogui.typewrite(str(item_completed.bought_at), interval=random.random()/4)
	time.sleep(1)
	pyautogui.press('enter')
	time.sleep(3)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/confirmofferbutton.png'))
	time.sleep(1)

def find_new_sell_price_and_sell_at_it(item_completed):
	time.sleep(1)
	pyautogui.click(pyautogui.center(pyautogui.locateOnScreen('images/buybag.png', region=(item_completed.box_loc))))
	time.sleep(1)
	pyautogui.click(1159, 431) #location of item in inv
	time.sleep(1)
	increase_offer_loc = pyautogui.locateCenterOnScreen('images/+5percbutton.png')
	for i in range(random.randint(35,45)):
		pyautogui.click(increase_offer_loc)
		time.sleep(random.random()/30)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/+1button.png'))
	time.sleep(0.2)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/confirmofferbutton.png'))
	time.sleep(5)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/completedoffer.png', region=(item_completed.box_loc)))
	time.sleep(3)
	pyautogui.click(1091, 638) #loc of collect offer button 2 hard coded in 
	time.sleep(0.3)
	pyautogui.click(1034, 636) #loc of collect offer button 1 hard coded in 
	time.sleep(1)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/salehistorytab.png'))
	time.sleep(2)
	#add check here to make sure the item was actually bought using pytesser probs
	buy_price = tesser_image(screengrab_as_numpy_array((1179, 427, 1306, 455))) #location of price hard coded in
	print(item_completed.bought_at)
	item_completed.set_bought_at(buy_price)
	print(item_completed.bought_at)
	time.sleep(1)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/grandexchangetab.png'))
	time.sleep(1)
	pyautogui.click(pyautogui.center(pyautogui.locateOnScreen('images/sellbag.png', region=(item_completed.box_loc))))
	time.sleep(1)
	pyautogui.click(1159, 431) #location of item in inv
	time.sleep(1)
	pyautogui.click(987, 524) #location of price box hard coded
	time.sleep(1)
	pyautogui.typewrite(str(item_completed.bought_at), interval=random.random()/4)
	time.sleep(1)
	pyautogui.press('enter')
	time.sleep(3)
	pyautogui.click(pyautogui.center(pyautogui.locateOnScreen('images/allbutton.png')))
	time.sleep(3)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/confirmofferbutton.png'))
	time.sleep(1)

def collect_money_or_items(item_completed):
	time.sleep(1)
	pyautogui.click(pyautogui.center(item_completed.box_loc))
	time.sleep(1)
	pyautogui.click(1091, 638) #loc of collect offer button 2 hard coded in 
	time.sleep(0.3)
	pyautogui.click(1034, 636) #loc of collect offer button 1 hard coded in 
	time.sleep(1)

def buy_or_sell_check(list_of_items_in_ge_buying, list_of_items_in_ge_selling):
	completedoffer_loc = pyautogui.locateOnScreen('images/completedoffer.png', region=(594,397, 1125, 782))
	buy_or_sell = None
	item_completed = None
	if completedoffer_loc != None:
		for item in list_of_items_in_ge_buying:
			#print(item.box_loc, completedoffer_loc, 'buying')
			if item.box_loc[0] < completedoffer_loc[0] and item.box_loc[1] < completedoffer_loc[1] and item.box_loc[0]+item.box_loc[2] > completedoffer_loc[0]+completedoffer_loc[2] and item.box_loc[1]+item.box_loc[3] > completedoffer_loc[1]+completedoffer_loc[3]:
				buy_or_sell = 'buy'
				item_completed = item
		for item in list_of_items_in_ge_selling:
			#print(item.box_loc, completedoffer_loc, 'selling')
			if item.box_loc[0] < completedoffer_loc[0] and item.box_loc[1] < completedoffer_loc[1] and item.box_loc[0]+item.box_loc[2] > completedoffer_loc[0]+completedoffer_loc[2] and item.box_loc[1]+item.box_loc[3] > completedoffer_loc[1]+completedoffer_loc[3]:
				buy_or_sell = 'sell'
				item_completed = item
		return(buy_or_sell, item_completed)

def find_item_prices(list_of_locations_of_offer_boxes, list_of_items_to_buy, in_use_boxes, list_of_items_in_ge_buying, amount_of_money):
	offer_box_index = random.randint(0,len(list_of_locations_of_offer_boxes)-1)
	#print(offer_box_index, 'offer index')
	buy_bag_loc = pyautogui.locateCenterOnScreen('images/buybag.png', region=(list_of_locations_of_offer_boxes[offer_box_index][0],list_of_locations_of_offer_boxes[offer_box_index][1], list_of_locations_of_offer_boxes[offer_box_index][2], list_of_locations_of_offer_boxes[offer_box_index][3]))
	pyautogui.click(buy_bag_loc[0], buy_bag_loc[1])
	time.sleep(2)
	#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	item_index = 0
	#item_index = random.randint(0,len(list_of_items_to_buy)-1)
	#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	#print(item_index, 'item index')
	item_to_buy = list_of_items_to_buy[item_index]
	list_of_items_to_buy.pop(item_index)
	string_of_item = str(item_to_buy.item)
	pyautogui.typewrite(string_of_item, interval=random.random()/4)
	time.sleep(2)
	pyautogui.click(pyautogui.locateCenterOnScreen(item_to_buy.image_path))
	time.sleep(2)
	increase_offer_loc = pyautogui.locateCenterOnScreen('images/+5percbutton.png')
	for i in range(random.randint(35,45)):
		pyautogui.click(increase_offer_loc)
		time.sleep(random.random()/30)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/+1button.png'))
	time.sleep(0.2)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/confirmofferbutton.png'))
	#time.sleep(5)
	#pyautogui.click(pyautogui.locateCenterOnScreen('images/completedoffer.png', region=(list_of_locations_of_offer_boxes[offer_box_index][0],list_of_locations_of_offer_boxes[offer_box_index][1], list_of_locations_of_offer_boxes[offer_box_index][2], list_of_locations_of_offer_boxes[offer_box_index][3])))
	#print(pyautogui.locateCenterOnScreen('images/completedoffer.png', region=(list_of_locations_of_offer_boxes[offer_box_index][0],list_of_locations_of_offer_boxes[offer_box_index][1], list_of_locations_of_offer_boxes[offer_box_index][2], list_of_locations_of_offer_boxes[offer_box_index][3])))
	time.sleep(5)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/completedoffer.png', region=(list_of_locations_of_offer_boxes[offer_box_index][0],list_of_locations_of_offer_boxes[offer_box_index][1], list_of_locations_of_offer_boxes[offer_box_index][2], list_of_locations_of_offer_boxes[offer_box_index][3])))
	time.sleep(3)
	pyautogui.click(1091, 638) #loc of collect offer button 2 hard coded in 
	time.sleep(0.3)
	pyautogui.click(1034, 636) #loc of collect offer button 1 hard coded in 
	time.sleep(1)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/salehistorytab.png'))
	time.sleep(2)
	#add check here to make sure the item was actually bought using pytesser probs
	buy_price = tesser_image(screengrab_as_numpy_array((1179, 427, 1306, 455))) #location of price hard coded in
	print(buy_price)
	item_to_buy.set_bought_at(buy_price)
	time.sleep(1)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/grandexchangetab.png'))
	time.sleep(2)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/sellbag.png', region=(list_of_locations_of_offer_boxes[offer_box_index][0],list_of_locations_of_offer_boxes[offer_box_index][1], list_of_locations_of_offer_boxes[offer_box_index][2], list_of_locations_of_offer_boxes[offer_box_index][3])))
	time.sleep(2)
	pyautogui.click(1159, 431)#clicking item in inv hard coded
	time.sleep(1)
	decrease_offer_loc = pyautogui.locateCenterOnScreen('images/-5percbutton.png')
	for i in range(random.randint(35,45)):
		pyautogui.click(decrease_offer_loc)
		time.sleep(random.random()/30)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/confirmofferbutton.png'))
	#time.sleep(5)
	#pyautogui.click(pyautogui.locateCenterOnScreen('images/completedoffer.png', region=(list_of_locations_of_offer_boxes[offer_box_index][0],list_of_locations_of_offer_boxes[offer_box_index][1], list_of_locations_of_offer_boxes[offer_box_index][2], list_of_locations_of_offer_boxes[offer_box_index][3])))
	#print(pyautogui.locateCenterOnScreen('images/completedoffer.png', region=(list_of_locations_of_offer_boxes[offer_box_index][0],list_of_locations_of_offer_boxes[offer_box_index][1], list_of_locations_of_offer_boxes[offer_box_index][2], list_of_locations_of_offer_boxes[offer_box_index][3])))
	time.sleep(5)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/completedoffer.png', region=(list_of_locations_of_offer_boxes[offer_box_index][0],list_of_locations_of_offer_boxes[offer_box_index][1], list_of_locations_of_offer_boxes[offer_box_index][2], list_of_locations_of_offer_boxes[offer_box_index][3])))
	time.sleep(3)
	pyautogui.click(1091, 638) #loc of collect offer button 2 hard coded in 
	time.sleep(0.3)
	pyautogui.click(1034, 636) #loc of collect offer button 1 hard coded in 
	time.sleep(1)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/salehistorytab.png'))
	time.sleep(2)
	sell_price = tesser_image(screengrab_as_numpy_array((1179, 427, 1306, 455))) #location of price hard coded in
	print(sell_price)
	item_to_buy.set_sold_at(sell_price)
	time.sleep(1)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/grandexchangetab.png'))
	time.sleep(1)
	print(string_of_item,'bought at', item_to_buy.bought_at, 'sold at', item_to_buy.sold_at)
	#adding in an undercut/overcut feature
	if item_to_buy.bought_at - item_to_buy.sold_at > 5:
		item_to_buy.set_bought_at(item_to_buy.bought_at - 1)
		item_to_buy.set_sold_at(item_to_buy.sold_at + 1)
	print(string_of_item,'values used are now bought at', item_to_buy.bought_at, 'sold at', item_to_buy.sold_at)
	#time to turn a profit
	pyautogui.click(buy_bag_loc[0], buy_bag_loc[1])
	time.sleep(2)
	pyautogui.typewrite(string_of_item, interval=random.random()/4)
	time.sleep(2)
	pyautogui.click(pyautogui.locateCenterOnScreen(item_to_buy.image_path))
	time.sleep(1)
	pyautogui.click(727, 524) #location of quantity box hard coded
	time.sleep(1)
	#finding a number to buy that fits our cash stack. This could be done better with keeping track of our cash stack and spending it accordingly buying some cheap and expensive items at the same time
	item_to_buy.set_number_to_buy(int(min(item_to_buy.available_to_buy, (amount_of_money/item_to_buy.sold_at)/len(list_of_locations_of_offer_boxes))))
	amount_of_money -= item_to_buy.number_to_buy*item_to_buy.sold_at
	pyautogui.typewrite(str(item_to_buy.number_to_buy), interval=random.random()/4)
	#pyautogui.typewrite(str(item_to_buy.limit), interval=0.25)   the way that worked@@@@@@@@@@@@
	time.sleep(1)
	pyautogui.press('enter')
	time.sleep(3)
	pyautogui.click(987, 524) #location of price box hard coded
	time.sleep(1)
	pyautogui.typewrite(str(item_to_buy.sold_at), interval=random.random()/4)
	time.sleep(1)
	pyautogui.press('enter')
	time.sleep(3)
	pyautogui.click(pyautogui.locateCenterOnScreen('images/confirmofferbutton.png'))
	print('amount of money', amount_of_money)
	item_to_buy.set_time_placed_buy_offer_at(time.time())
	time.sleep(5)
	in_use_boxes.append(list_of_locations_of_offer_boxes[offer_box_index])
	item_to_buy.set_box_containing_item(list_of_locations_of_offer_boxes[offer_box_index])
	list_of_locations_of_offer_boxes.pop(offer_box_index)
	list_of_items_in_ge_buying.append(item_to_buy)
	return(list_of_locations_of_offer_boxes, list_of_items_to_buy, in_use_boxes, list_of_items_in_ge_buying, amount_of_money, item_to_buy)


#first we want to check if there are any completed offers
#if there are we want to collect these, we need to know if what we are collecting is a completed buy or sell
#this could come from perhaps some list of current offers in the ge?
#then we need to check if there are any available slots, if there are we need to file an order
#this would go as follows, buy max, record price, sell min, record price, file a buy order
#then we need to repeat 


#buy_price = tesser_image(screengrab_as_numpy_array((1179, 427, 1306, 455))) #location of price hard coded in
#print(buy_price)

	#cv2.imshow('image', list_of_items[0].image)
	#cv2.waitKey(0)
#loc_to_screen = (778, 489, 940, 510)
#im = screengrab_as_numpy_array(loc_to_screen)

#cv2.imwrite('images/completedselloffer.png',im)

#print(pyautogui.locateCenterOnScreen('images/completedoffer.png'))
#time.sleep(10)
#pyautogui.click(pyautogui.locateCenterOnScreen('images/completedoffer.png', region=(list_of_locations_of_offer_boxes[offer_box_index][0],list_of_locations_of_offer_boxes[offer_box_index][1], list_of_locations_of_offer_boxes[offer_box_index][2], list_of_locations_of_offer_boxes[offer_box_index][3])))
#time.sleep(3)

#image_taker()

main()
#print(tesser_image(screengrab_as_numpy_array((1179, 427, 1306, 455))))

#print(pyautogui.locateCenterOnScreen('images/magiclogs.png'))
	


#loc_to_screen = (639, 645, 704, 661)
#im = screengrab_as_numpy_array(loc_to_screen)

#cv2.imwrite('images/magiclogs.png',im)
#for i in item_names:
#	string = 'images/' + i.replace(" ", "") + '.png'
#	pyautogui.typewrite(i, interval=0.05)
#	time.sleep(3)
#	im = screengrab_as_numpy_array(loc_to_screen)
#	cv2.imwrite(string ,im)
#	for j in range(len(i)):
#		time.sleep(0.1)
#		pyautogui.press('backspace')
	

