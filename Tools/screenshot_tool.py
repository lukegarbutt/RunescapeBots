import pyautogui

def take_screenshot():
	file_name = 'screenshots/' + input("What would you like to save the screenshot as? Please enter the entire file name including extension, ie .png\n")
	input("Place curser over the top left corner of the box you'd like to screenshot and press enter")
	top_left = pyautogui.position()
	input("Place curser over the bottom right corner of the box you'd like to screenshot and press enter")
	bottom_right = pyautogui.position()
	width = bottom_right[0] - top_left[0]
	height = bottom_right[1] - top_left[1]
	pyautogui.screenshot(file_name, region=(top_left[0], top_left[1], width, height))

if __name__ == '__main__':
	take_screenshot()
