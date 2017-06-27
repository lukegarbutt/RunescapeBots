# Main script that will merch items in the GE

import pyautogui
import time
import pickle
import os
import pytesseract
import cv2
import numpy
import random
import PIL

# below are custom modules
from Custom_Modules import realmouse
from Custom_Modules import pointfrombox
from Custom_Modules import gelimitfinder


loaded_pickled_object = None
load_state = False


def main():
	# maybe we should add a pickle load up here so that we can load in a previous state if we have one?
	# this would mean we can save instances and only have to initialise one if we don't have a save file to load
	# we should also have a variable that tells us whether or not we loaded from a saved instance
	# this is important because if we did we don't want to be scoring items immediately (this would create articifically low scores)
	# ask me for more info on this
	# returns a list of object of runescape windows and all their features
	list_of_runescape_windows = detect_runescape_windows()
	if len(list_of_runescape_windows) > 1:
		print('We have detected {} windows'.format(len(list_of_runescape_windows)))
	elif len(list_of_runescape_windows) == 1:
		print('We have detected {} window'.format(len(list_of_runescape_windows)))
	elif len(list_of_runescape_windows) == 0:
		print("Failed, we couldn't detect a runescape window, script will now abort")
		quit()
	logout_prevention_random_number = random.randint(150, 270)
	list_of_items_in_use = []
	while(True):
		for runescape_window in list_of_runescape_windows:
			if time.time() - runescape_window.last_action_time > logout_prevention_random_number:  # prevent auto logout
				logout_prevention_random_number = random.randint(150, 270)
				runescape_window.set_time_of_last_action()
				prevent_logout(runescape_window.top_left_corner,runescape_window.bottom_right_corner)
		# for each window we need to check if there are any completed offers
		# and if so handle them
		completed_offer_check = False # variable to see if there was a completed offer
									# this will be used so that if there is one we can skip the rest of the code
									# and cycle back through to check again untill there is no completed offers
									# to handle, and we can continue filling ge slots, this gives completed offers
									# 100% priority, hopefully increasing performance
		for runescape_window in list_of_runescape_windows:
			coords_of_completed_offer = pyautogui.locateOnScreen('Tools/screenshots/green_offer_complete_bar.png', region=(runescape_window.top_left_corner[0], runescape_window.top_left_corner[
																 1], runescape_window.bottom_right_corner[0] - runescape_window.top_left_corner[0], runescape_window.bottom_right_corner[1] - runescape_window.top_left_corner[1]))
			if coords_of_completed_offer == None:
				continue
			else:
				completed_offer_check = True
				for ge_slot in runescape_window.list_of_ge_slots:
					if ge_slot.top_left_corner[0] < coords_of_completed_offer[0] and ge_slot.top_left_corner[1] < coords_of_completed_offer[1] and ge_slot.bottom_right_corner[0] > coords_of_completed_offer[0] and ge_slot.bottom_right_corner[1] > coords_of_completed_offer[1]:
						# collects the items from the offer
						collect_items_from_ge_slot(ge_slot, runescape_window)
						# do stuff based on buy or sell
						if ge_slot.buy_or_sell == 'buy':
							# if the item was bought then it would simply sell it at the correct price (assuming the order was filled in under
							# a certain amount of time), if the item took too long to buy then we would buy another just to confirm that our
							# price is right). We would also place the item in the cooldown list as a tuple. this tuple would contain
							# the item name, the time it was bought, the quantity that were bought
							# do buy stuff
							# place the item on cooldown
							runescape_window.add_to_items_on_cooldown(ge_slot.item)
							ge_slot.item.number_available_to_buy -= ge_slot.item.quantity_to_buy
							if time.time() - ge_slot.item.time_of_last_pc > 1800:
								# grab a new price to sell items at since it
								# has been a long time since we collected this
								# info
								find_up_to_date_sell_price(runescape_window, ge_slot)
							# sell our items at the price instant bought at
							sell_items(runescape_window, ge_slot)
						elif ge_slot.buy_or_sell == 'sell':
							# do sell stuff
							# score the item somehow (skipping this step for now)
							# also need to track total money and the profit, but again skipping this for now
							# if the item was sold then we would score the item based on the profit it made us and the time it took to buy and sell
							ge_slot.update_buy_or_sell_state(None) # updates the buy or sell state to none to indiate the slot is now empty
							# still need to update lists of items in use accordingly
							# perhaps like this
							list_of_items_in_use.remove(ge_slot.item.item_name)
							ge_slot.item.set_price_instant_bought_at(None)
							ge_slot.item.set_price_instant_sold_at(None)
							ge_slot.set_item_in_ge_slot(None)
		if not completed_offer_check:
			empty_slot_check = False # check if we have found an empty slot, this will be used to break out
									# once we have, so that we only place 1 order before going back through
									# the loop to check for completed offers and such
			for runescape_window in list_of_runescape_windows:
				if runescape_window.number_of_empty_ge_slots > 0:  # scans until it finds a window with an empty ge slot
					for ge_slot in runescape_window.list_of_ge_slots:
						if ge_slot.buy_or_sell == None:
							# we have found an empty slot, so lets place an order
							list_of_items_available = []
							for item in runescape_window.items_to_merch:
								if item.item_name not in list_of_items_in_use:
									if item.number_available_to_buy > 0.2*item.limit:
										list_of_items_available.append(item)
							if len(list_of_items_available) > 0:
								ge_slot.set_item_in_ge_slot(random.choice(list_of_items_available))
								list_of_items_in_use.append(ge_slot.item.item_name)
								find_up_to_date_sell_price(runescape_window, ge_slot)
								find_up_to_date_buy_price(runescape_window, ge_slot)
								buy_item(runescape_window, ge_slot)
							empty_slot_check = True
						if empty_slot_check == True:
							break
				if empty_slot_check == True:
					break




		for runescape_window in list_of_runescape_windows:
			runescape_window.check_for_empty_ge_slots() # this will update states of ge slots correctly
			# we can also add other updates into here such as checking items on cooldown, more to add later
# if there are no completed orders then we need to
# check for empty ge slots and fill them with
# orders
# all orders should be unique, ie not buying coal on 2 windows at once, this would harm profit since they would be
# competing with eachother. Instead one window should buy it, then once it has sold the next window can start to buy


class item():

	def __init__(self, name, limit):
		self.item_name = name
		self.limit = limit
		self.number_available_to_buy = limit
		self.image_in_ge_search = check_if_image_exists(name)
		self.price_instant_bought_at = None
		self.price_instant_sold_at = None
		self.current_state = None # this will track if the item is currently being bought, sold or neither (None)

	def set_time_of_last_pc(self):
			self.time_of_last_pc = time.time()

	def set_price_instant_bought_at(self, price):
			self.price_instant_bought_at = price

	def set_price_instant_sold_at(self, price):
			self.price_instant_sold_at = price

	def set_quantity_to_buy(self, number):
			self.quantity_to_buy = number

	def set_current_state(self, state):
			self.current_state = state


class ge_slot():

	def __init__(self, position):
		self.top_left_corner = position[0]
		self.bottom_right_corner = position[1]
		self.buy_or_sell = None
		self.item = None

	def update_buy_or_sell_state(self, state):
		self.buy_or_sell = state

	def set_item_in_ge_slot(self, item):
		self.item = item


class runescape_instance():

	def __init__(self, position):
		self.bottom_right_corner = position
		self.top_left_corner = (position[0] - 750, position[1] - 450)
		self.member_status = members_status_check(self.top_left_corner, self.bottom_right_corner)
		self.list_of_ge_slots = initialise_ge_slots(self.top_left_corner, self.bottom_right_corner)  # this returns a list of ge_slot objects
		self.money = 500000  # given a default for now, we could change this later maybe
		self.profit = 0
		self.last_action_time = time.time()
		# examines money to make the above line accurate
		examine_money(position)
		self.items_to_merch = items_to_merch(self.member_status)
		self.list_of_items_on_cooldown = []
		# will be true if there is an empty slot in this window, else false
		self.number_of_empty_ge_slots = empty_ge_slot_check(self.list_of_ge_slots)

	def check_for_empty_ge_slots(self):
		self.number_of_empty_ge_slots = empty_ge_slot_check(self.list_of_ge_slots)

	def set_time_of_last_action(self):
		self.last_action_time = time.time()

	def add_to_items_on_cooldown(self, item):
		self.list_of_items_on_cooldown.append((item.item_name, time.time(), item.quantity_to_buy))

	def update_money(self, number):
		self.money = number


def buy_item(runescape_window, ge_slot):
	# click the correct buy bag
	move_mouse_to_image_within_region('Tools/screenshots/buy_bag.png', ge_slot)
	pyautogui.click()
	wait_for('Tools/screenshots/quantity_box.png', runescape_window)
	# click search box
	move_mouse_to_image_within_region('Tools/screenshots/search_box.png', runescape_window)
	pyautogui.click()
	# type in item
	random_typer(str(ge_slot.item.item_name))
	wait_for(ge_slot.item.image_in_ge_search, runescape_window)
	# click item
	move_mouse_to_image_within_region(ge_slot.item.image_in_ge_search, runescape_window)
	pyautogui.click()
	# click price box
	coords_of_price_box = pointfrombox.random_point((runescape_window.bottom_right_corner[0]-384, runescape_window.bottom_right_corner[1]-272),
		(runescape_window.bottom_right_corner[0]-291, runescape_window.bottom_right_corner[1]-259))
	realmouse.move_mouse_to(coords_of_price_box[0], coords_of_price_box[1])
	pyautogui.click()
	time.sleep(random.random()+1)
	# type in correct price and hit enter
	random_typer(str(ge_slot.item.price_instant_sold_at))
	pyautogui.press('enter')
	# click quantity box
	move_mouse_to_image_within_region("Tools/screenshots/quantity_box.png", runescape_window)
	pyautogui.click()
	time.sleep(random.random()+2)
	# type in correct quantity and hit enter
	ge_slot.item.set_quantity_to_buy(int(min(ge_slot.item.number_available_to_buy, (runescape_window.money/ge_slot.item.price_instant_sold_at)/runescape_window.number_of_empty_ge_slots)))
	runescape_window.update_money(runescape_window.money - (ge_slot.item.quantity_to_buy*ge_slot.item.price_instant_sold_at))
	random_typer(str(ge_slot.item.quantity_to_buy))
	time.sleep(random.random())
	pyautogui.press('enter')
	# click confirm off
	move_mouse_to_image_within_region("Tools/screenshots/confirm_offer_button.png", runescape_window)
	pyautogui.click()
	wait_for('Tools/screenshots/lent_item_box.png', runescape_window)
	# update states accordingly
	runescape_window.set_time_of_last_action()
	ge_slot.update_buy_or_sell_state('buy')
	runescape_window.check_for_empty_ge_slots()
	print('Placed a buy order for {} {} at {} each'.format(ge_slot.item.quantity_to_buy, ge_slot.item.item_name, ge_slot.item.price_instant_sold_at))

def sell_items(runescape_window, ge_slot):
	# click correct sell bag
	move_mouse_to_image_within_region('Tools/screenshots/sell_bag.png', ge_slot)
	pyautogui.click()
	wait_for('Tools/screenshots/quantity_box.png', runescape_window)
	# click item in inv
	coords_of_item = pointfrombox.random_point((runescape_window.bottom_right_corner[0]-180, runescape_window.bottom_right_corner[1]-372),
		(runescape_window.bottom_right_corner[0]-166, runescape_window.bottom_right_corner[1]-349))
	realmouse.move_mouse_to(coords_of_item[0], coords_of_item[1])
	pyautogui.click()
	# click all button incase
	move_mouse_to_image_within_region("Tools/screenshots/all_button.png", runescape_window)
	pyautogui.click()
	# click price button
	coords_of_price_box = pointfrombox.random_point((runescape_window.bottom_right_corner[0]-384, runescape_window.bottom_right_corner[1]-272),
		(runescape_window.bottom_right_corner[0]-291, runescape_window.bottom_right_corner[1]-259))
	realmouse.move_mouse_to(coords_of_price_box[0], coords_of_price_box[1])
	pyautogui.click()
	time.sleep(2+random.random())
	# type price in and hit enter
	random_typer(str(ge_slot.item.price_instant_bought_at))
	pyautogui.press('enter')
	# click confirm
	move_mouse_to_image_within_region("Tools/screenshots/confirm_offer_button.png", runescape_window)
	pyautogui.click()
	# update state of ge slot
	ge_slot.update_buy_or_sell_state('sell')
	wait_for('Tools/screenshots/lent_item_box.png', runescape_window)
	runescape_window.set_time_of_last_action()
	print('Placed a sell order for {} {} at {} each'.format(ge_slot.item.quantity_to_buy, ge_slot.item.item_name, ge_slot.item.price_instant_bought_at))

def find_up_to_date_buy_price(runescape_window, ge_slot):
	# click correct sell bag
	move_mouse_to_image_within_region('Tools/screenshots/sell_bag.png', ge_slot)
	pyautogui.click()
	wait_for('Tools/screenshots/quantity_box.png', runescape_window)
	# sell item for cheap
	coords_of_item = pointfrombox.random_point((runescape_window.bottom_right_corner[0]-180, runescape_window.bottom_right_corner[1]-372),
		(runescape_window.bottom_right_corner[0]-166, runescape_window.bottom_right_corner[1]-349))
	realmouse.move_mouse_to(coords_of_item[0], coords_of_item[1])
	pyautogui.click()
	move_mouse_to_image_within_region('Tools/screenshots/-5perc_button.png', runescape_window)
	for i in range(random.randint(20,35)):
		pyautogui.click()
		time.sleep(random.random()/7)
	move_mouse_to_image_within_region('Tools/screenshots/confirm_offer_button.png', runescape_window)
	pyautogui.click()
	wait_for('Tools/screenshots/lent_item_box.png', runescape_window)
	# collect money
	collect_items_from_ge_slot(ge_slot, runescape_window)
	# click sale history
	move_mouse_to_image_within_region('Tools/screenshots/sale_history_button.png', runescape_window)
	pyautogui.click()
	wait_for('Tools/screenshots/sale_history_check.png', runescape_window)
	# check price
	sell_price = check_price(runescape_window)
	# update price
	ge_slot.item.set_price_instant_sold_at(sell_price)
	# click grand exchange window
	move_mouse_to_box('Tools/screenshots/grand_exchange_button.png',
						runescape_window.top_left_corner, runescape_window.bottom_right_corner)
	pyautogui.click()
	wait_for('Tools/screenshots/lent_item_box.png', runescape_window)
	runescape_window.set_time_of_last_action()
	print('{} instantly sold for a price of {}'.format(ge_slot.item.item_name, ge_slot.item.price_instant_sold_at))

def find_up_to_date_sell_price(runescape_window, ge_slot):
	# click correct buy bag
	move_mouse_to_image_within_region('Tools/screenshots/buy_bag.png', ge_slot)
	pyautogui.click()
	wait_for('Tools/screenshots/quantity_box.png', runescape_window)
	# buy item for lots of money
	move_mouse_to_image_within_region('Tools/screenshots/search_box.png', runescape_window)
	pyautogui.click()
	time.sleep(3+random.random())
	random_typer(str(ge_slot.item.item_name))
	wait_for(ge_slot.item.image_in_ge_search, runescape_window)
	move_mouse_to_image_within_region(ge_slot.item.image_in_ge_search, runescape_window)
	pyautogui.click()
	move_mouse_to_image_within_region('Tools/screenshots/+1_button.png', runescape_window)
	pyautogui.click()
	move_mouse_to_image_within_region('Tools/screenshots/+5perc_button.png', runescape_window)
	for i in range(random.randint(20,35)):
		pyautogui.click()
		time.sleep(random.random()/7)
	move_mouse_to_image_within_region('Tools/screenshots/confirm_offer_button.png', runescape_window)
	pyautogui.click()
	wait_for('Tools/screenshots/lent_item_box.png', runescape_window)
	# collect item
	collect_items_from_ge_slot(ge_slot, runescape_window)
	# click sale history
	move_mouse_to_image_within_region('Tools/screenshots/sale_history_button.png', runescape_window)
	pyautogui.click()
	wait_for('Tools/screenshots/sale_history_check.png', runescape_window)
	# check price
	buy_price = check_price(runescape_window)
	# update price
	ge_slot.item.set_price_instant_bought_at(buy_price)
	# click grand exchange window
	move_mouse_to_box('Tools/screenshots/grand_exchange_button.png',
						runescape_window.top_left_corner, runescape_window.bottom_right_corner)
	pyautogui.click()
	wait_for('Tools/screenshots/lent_item_box.png', runescape_window)
	runescape_window.set_time_of_last_action()
	ge_slot.item.set_time_of_last_pc()
	print('{} instantly bought for a price of {}'.format(ge_slot.item.item_name, ge_slot.item.price_instant_bought_at))

def random_typer(word):
	for i in word:
		pyautogui.typewrite(i, interval=random.random()/4)

def check_price(runescape_window):
	loc_of_price = (runescape_window.bottom_right_corner[0] - 144, runescape_window.bottom_right_corner[1] - 364,
		runescape_window.bottom_right_corner[0] - 22, runescape_window.bottom_right_corner[1] - 337)
	price = tesser_image(screengrab_as_numpy_array((loc_of_price[0], loc_of_price[1], loc_of_price[2], loc_of_price[3])))
	return(price)

def screengrab_as_numpy_array(location):
	im = numpy.array(PIL.ImageGrab.grab(bbox=(location[0],location[1],location[2],location[3])))
	im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	#cv2.imshow('im', im)
	#cv2.waitKey(0)
	return(im)

def tesser_image(image):
	image = cv2.resize(image, (0,0), fx=2, fy=2)
	ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
	#cv2.imshow('im', image)
	#cv2.waitKey(0)
	image = PIL.Image.fromarray(image, 'RGB')
	txt = pytesseract.image_to_string(image)
	txt = txt.replace(",", "")
	txt = txt.replace(" ", "")
	txt = txt.replace(".", "")
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
		if len(txt_list)>1:
			txt = int(''.join(txt_list))
		else:
			txt = int(txt_list[0])
	return(txt)

def move_mouse_to_image_within_region(image, region): # region takes in an object
	image_loc = pyautogui.locateOnScreen(image, region=(region.top_left_corner[0], region.top_left_corner[1], region.bottom_right_corner[0]-region.top_left_corner[0], region.bottom_right_corner[1]-region.top_left_corner[1]))
	while(image_loc == None):
		image_loc = pyautogui.locateOnScreen(image, region=(region.top_left_corner[0], region.top_left_corner[1], region.bottom_right_corner[0]-region.top_left_corner[0], region.bottom_right_corner[1]-region.top_left_corner[1]))
	point_to_click = pointfrombox.random_point((image_loc[0], image_loc[1]), (image_loc[0]+image_loc[2], image_loc[1]+image_loc[3]))
	realmouse.move_mouse_to(point_to_click[0], point_to_click[1])

def collect_items_from_ge_slot(ge_slot, runescape_window):
	point_to_click = pointfrombox.random_point(ge_slot.top_left_corner, ge_slot.bottom_right_corner)
	realmouse.move_mouse_to(point_to_click[0], point_to_click[1])
	pyautogui.click()
	wait_for('Tools/screenshots/completed_offer_page.png', runescape_window)
	point_of_item_collection_box_1 = pointfrombox.random_point((runescape_window.bottom_right_corner[0] - 303, runescape_window.bottom_right_corner[
															   1] - 166), (runescape_window.bottom_right_corner[0] - 273, runescape_window.bottom_right_corner[1] - 138))
	point_of_item_collection_box_2 = pointfrombox.random_point((runescape_window.bottom_right_corner[0] - 254, runescape_window.bottom_right_corner[
															   1] - 166), (runescape_window.bottom_right_corner[0] - 222, runescape_window.bottom_right_corner[1] - 138))
	realmouse.move_mouse_to(point_of_item_collection_box_2[0], point_of_item_collection_box_2[1])
	pyautogui.click()
	realmouse.move_mouse_to(point_of_item_collection_box_1[0], point_of_item_collection_box_1[1])
	pyautogui.click()
	wait_for('Tools/screenshots/lent_item_box.png', runescape_window)

def wait_for(image, runescape_window):
	# adding a possible failsafe in here
	time_entered = time.time()
	# could add a failsafe in here incase we misclick or something, this
	# should be something to come back to
	while(True):
		found = pyautogui.locateOnScreen(image, region=(runescape_window.top_left_corner[0], runescape_window.top_left_corner[1], runescape_window.bottom_right_corner[
										 0] - runescape_window.top_left_corner[0], runescape_window.bottom_right_corner[1] - runescape_window.top_left_corner[1]))
		if found != None:
			break
		elif time.time()-time_entered > 5 :
			print('We appear to be stuck so attempting to click again and see if this fixes it')
			pyautogui.click()
			time_entered = time.time()

def empty_ge_slot_check(list_of_ge_slots):
	number_of_ge_slots_open = 0
	for slot in list_of_ge_slots:
		if slot.buy_or_sell == None:
			number_of_ge_slots_open += 1
	return(number_of_ge_slots_open)

def prevent_logout(top_left_corner, bottom_right_corner):
	seed = random.random()
	if seed > 0.5:  # opens up the sale history tab for 5 seconds then returns to ge tab
		move_mouse_to_box('Tools/screenshots/sale_history_button.png', top_left_corner, bottom_right_corner)
		pyautogui.click()
		time.sleep(9*random.random()+1)
		move_mouse_to_box('Tools/screenshots/grand_exchange_button.png', top_left_corner, bottom_right_corner)
		pyautogui.click()
	else:  # examines the money pouch
		examine_money(bottom_right_corner)

# pass in an image and a search region
def move_mouse_to_box(image_of_box, top_left_corner, bottom_right_corner):
	box_to_click = pyautogui.locateOnScreen(image_of_box, region=(top_left_corner[0], top_left_corner[
											1], bottom_right_corner[0] - top_left_corner[0], bottom_right_corner[1] - top_left_corner[1]))
	random_x = random.randint(0, box_to_click[2])
	random_y = random.randint(0, box_to_click[3])
	realmouse.move_mouse_to(box_to_click[0] + random_x, box_to_click[1] + random_y)

def check_if_image_exists(item_name):
	file_name = 'Tools/screenshots/items/' + \
		item_name.replace(' ', '_') + '.png'
	if os.path.isfile(file_name):
		return(file_name)
	else:
		print('You do not have an image file for {} so the script is aborting, to fix this issue either take a screenshot of {} or remove it from the list of items to merch'.format(item_name, item_name))

def items_to_merch(member_status):
	if member_status:
		items_to_merch = []
		# below is a list of members items to merch
		list_of_items = ['Coal', 'Air rune', 'Fire rune',
						 'Rune bar', 'Runite ore', 'Water rune', 'Maple logs', 'Yew logs', 'Nature rune', 'Law rune',
						 'Infernal ashes', 'Airut bones', 'Magic notepaper', 'Cannonball']
		list_of_item_limits = gelimitfinder.find_ge_limit(list_of_items)
		for i in range(len(list_of_items)):
			items_to_merch.append(item(list_of_items[i], list_of_item_limits[i]))
		# we are a member so initialise a members item list
	else:
		items_to_merch = []
		# below is a list of f2p items to merch
		list_of_items = ['Coal', 'Air rune', 'Fire rune',
						 'Rune bar', 'Runite ore', 'Water rune', 'Maple logs', 'Yew logs', 'Nature rune', 'Law rune']
		list_of_item_limits = gelimitfinder.find_ge_limit(list_of_items)
		for i in range(len(list_of_items)):
			items_to_merch.append(item(list_of_items[i], list_of_item_limits[i]))
		# we are f2p so initialise a f2p item list
	return(items_to_merch)

def examine_money(position):
	# this whole block just examines the amount of money
	point = pointfrombox.random_point((138, 94), (189, 109))
	# that the account has just for auto log out purposes
	money_pouch = (position[0] - point[0], position[1] - point[1])
	# so that it has a recording of the last time an action
	realmouse.move_mouse_to(money_pouch[0], money_pouch[1])
	# was taken and can keep track of this value in future to stop logouts
	# occuring
	pyautogui.click(button='right')
	point = pointfrombox.random_point((-75, -35), (74, -24))
	examine = (money_pouch[0] - point[0], money_pouch[1] - point[1])
	realmouse.move_mouse_to(examine[0], examine[1])
	pyautogui.click()

def initialise_ge_slots(top_left_corner, bottom_right_corner):
	ge_slots = []
	for i in count_ge_slots(top_left_corner, bottom_right_corner):
		ge_slots.append(ge_slot(((i[0], i[1]), (i[0] + i[2], i[1] + i[3]))))
	return(ge_slots)

def members_status_check(top_left_corner, bottom_right_corner):
	width = bottom_right_corner[0] - top_left_corner[0]
	height = bottom_right_corner[1] - top_left_corner[1]
	if len(list(pyautogui.locateAllOnScreen('Tools/screenshots/non_mems_slot.png',
							 region=(top_left_corner[0], top_left_corner[1], width, height)))) != 0:
		return(False)
	else:
		return(True)

def detect_runescape_windows():  # this function will detect how many runescape windows are present and where they are
	list_of_runescape_windows = []
	for i in pyautogui.locateAllOnScreen('Tools/screenshots/collect_all_buttons.png'):
		list_of_runescape_windows.append(
			runescape_instance((i[0] + i[2], i[1] + i[3])))
	return(list_of_runescape_windows)

def move_and_resize_runescape_windows():
	pass  # this will move and resize the detected windows.
	# Initially this will just pass since we don't know how to do this, but
	# further down the road we can add to this and implement it

# this checks how many slots a particular window has available
def count_ge_slots(top_left_corner, bottom_right_corner):
	width = bottom_right_corner[0] - top_left_corner[0]
	height = bottom_right_corner[1] - top_left_corner[1]
	list_of_ge_slots = list(pyautogui.locateAllOnScreen(
		'Tools/screenshots/available_ge_slot.png', region=(top_left_corner[0], top_left_corner[1], width, height)))
	return(list_of_ge_slots)

def load_pickle(pickle_file):
	"""Returns binary object from file path passed
		and sets global variable loaded_pickled_object
		equal to returned object"""
	global loaded_pickled_object, load_state

	with open(pickle_file, 'rb') as f:
		try:
			loaded_pickled_object = pickle.load(f)
			print("{} LOADED!".format(pickle_file))
			load_state = True
			return loaded_pickled_object
		except:
			print("{} is N0T a a pickle object!".format(pickle_file))
			load_state = False

def save_pickle(var_to_save):
	save_name = 'save1.pickle'
	with open('Saves/' + save_name, 'wb') as f:
		try:
			print(var_to_save)
			pickle.dump(var_to_save, f)
			print("{} Saved!".format(save_name))
			load_state = True
		except Exception as e:
			print(e)
			print("{} is N0T a a pickle object!".format(save_name))
			load_state = False

def load_previous_state():
	"""Looks up a pickled file, if found loads it"""

	global loaded_pickled_object, load_state

	save_name = 'save1.pickle'
	save_dir_name = "Saves/"
	saved_file = save_dir_name + save_name

	# looks up file names in siaves folder
	for (dirpath, dirnames, filenames) in os.walk(save_dir_name):
		break
	# loads pickled file if exists
	if save_name in filenames:
		load_pickle(saved_file)

	# ask user to create save file
	else:
		print("Save file: '{}' NOT FOUND!\n".format(saved_file))

if __name__ == '__main__':
	main()
