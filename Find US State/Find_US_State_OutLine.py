from selenium import webdriver
from selenium.common.exceptions import *
from time import sleep
from colorama import init, Fore
from State_DB import *

init(autoreset=True)

class Status_Code():
	Status_OK = "[{}+{}]".format(Fore.LIGHTGREEN_EX, Fore.RESET)
	Status_FATAL = "[{}-{}]".format(Fore.LIGHTRED_EX, Fore.RESET)
	Status_INFO = "[{}*{}]".format(Fore.LIGHTBLUE_EX, Fore.RESET)
	Status_WARNING = "[{}!{}]".format(Fore.LIGHTYELLOW_EX, Fore.RESET)


def Play_Solo(email, password):
	global State_DB
	global Driver
	Driver = webdriver.Chrome('chromedriver.exe')
	print(Status_Code.Status_INFO + "Waiting for page to load")
	Driver.get('https://www.sporcle.com/games/Matt/find_the_states')
	print(Status_Code.Status_INFO + "Page Loading complete")

	# Login Procedure
	username_input = Driver.find_element_by_id('username_gamepage')
	username_input.send_keys(email)
	print(Status_Code.Status_INFO + "ENTERING USERNAME")
	password_input = Driver.find_element_by_id('password_gamepage')
	password_input.send_keys(password)
	print(Status_Code.Status_INFO + "ENTERING PASSWORD")
	print(Status_Code.Status_INFO + "LOGGING IN")

	Driver.find_element_by_id("button-play").click()
	print(Status_Code.Status_INFO + "Starting")

	for x in range(50):
		Curren_State = Driver.find_element_by_id('currgamename').text
		print(Curren_State)
		# The following state will raise a error for some reason if encountered.
		if Curren_State == "Michigan":
			Driver.execute_script('pickSlot();')
			print(Status_Code.Status_WARNING + "S Michigan. E a21. WARN. O_E RECV CLK. NXT")
			sleep(0.2)
			continue
		if Curren_State == 'Hawaii':
			Driver.execute_script('pickSlot();')
			print(Status_Code.Status_WARNING + "S Hawaii. E a10. WARN. O_E RECV CLK. NXT")
			sleep(0.2)
			continue
		if Curren_State == "Louisiana":
			Driver.execute_script('pickSlot();')
			print(Status_Code.Status_WARNING + "S Louisiana. E a17. WARN. O_E RECV CLK. NXT")
			sleep(0.2)
			continue
		if Curren_State == "Florida":
			Driver.execute_script('pickSlot();')
			print(Status_Code.Status_WARNING + "S Florida. E a8. WARN. O_E RECV CLK. NXT")
			sleep(0.2)
			continue
		Element = State_DB.get(Curren_State)
		print(Element)
		sleep(0.2)
		Driver.find_element_by_id(Element).click()

	print(Status_Code.Status_OK + "Done")



def Play_Againest(email, password):
	global State_DB
	global Driver
	Driver = webdriver.Chrome('chromedriver.exe')
	print(Status_Code.Status_INFO + "Waiting for page to load")
	Driver.get('https://www.sporcle.com/games/Matt/find_the_states')
	print(Status_Code.Status_OK + "Page Loading complete")

	# Login Procedure
	username_input = Driver.find_element_by_id('username_gamepage')
	username_input.send_keys(email)
	print(Status_Code.Status_INFO + "ENTERING USERNAME")
	password_input = Driver.find_element_by_id('password_gamepage')
	password_input.send_keys(password)
	print(Status_Code.Status_INFO + "ENTERING PASSWORD")
	print(Status_Code.Status_INFO + "LOGGING IN")
	Driver.find_element_by_id('game_page_login_btn').click()
	sleep(2)

	# Close ad pop up
	try:
		Driver.find_element_by_class_name('bx-close-x-adaptive-2').click()
	except:
		pass

	# Big loop for playing again
	while True:
		# Click Find Opponent Button
		try:
			Driver.find_element_by_id('button-connect-showdown').click()
		except:
			print(Status_Code.Status_FATAL + "FAILED TO CLICK ON FIND OPPONENT BTN. PLEASE CLICK IT THEN PRESS ENTER")
			input("PRESS ENTER TO CONTINUE")

		# Check if user still in queue
		Wait_Oppoent_Time = 0
		while True:
			try:
				sleep(1)
				Driver.find_element_by_id('showdown-queueing-message-textbox')
				Wait_Oppoent_Time += 1
				print("Matching up for opponent. Time Elapsed: {}".format(Wait_Oppoent_Time), end='\r')
			except:
				break

		print(Status_Code.Status_INFO + "Waiting for opponent...")

		# Check if the game started
		while True:	
			if Driver.find_element_by_id('answer-wrapper').is_displayed():
				break
			sleep(1)

		print(Status_Code.Status_INFO + "Starting")

		# Loop through the states
		try:
			for x in range(50):
					sleep(0.3)
					Curren_State = Driver.find_element_by_id('currgamename').text  # Get Current State
					print(Curren_State)
					# The following state will cause an unknown error if try to click on it
					if Curren_State == "Michigan":
						Driver.execute_script('pickSlot();')
						print(Status_Code.Status_WARNING + "S Michigan. E a21. WARN. O_E RECV CLK. NXT")
						sleep(0.2)
						continue
					if Curren_State == 'Hawaii':
						Driver.execute_script('pickSlot();')
						print(Status_Code.Status_WARNING + "S Hawaii. E a10. WARN. O_E RECV CLK. NXT")
						sleep(0.2)
						continue
					if Curren_State == "Louisiana":
						Driver.execute_script('pickSlot();')
						print(Status_Code.Status_WARNING + "S Louisiana. E a17. WARN. O_E RECV CLK. NXT")
						sleep(0.2)
						continue
					if Curren_State == "Florida":
						Driver.execute_script('pickSlot();')
						print(Status_Code.Status_WARNING + "S Florida. E a8. WARN. O_E RECV CLK. NXT")
						sleep(0.2)
						continue
					Element = State_DB.get(Curren_State)
					Driver.find_element_by_id(Element).click()
					continue
		except NoSuchElementException:
			print(Status_Code.Status_INFO + "EXCEPTION ENCOUNTERED. ASSUMING DONE. CONTINUEING")

		print(Status_Code.Status_OK + "Done\n")

		ask_PlayAgain = int(input("Play again? Yes(1) No(2):"))
		if ask_PlayAgain == 1:
			Driver.find_element_by_id('button-replay').click()
			sleep(0.5)
			continue
		if ask_PlayAgain == 2:
			raise SystemExit(0)




def main():
	Choice = int(input("Solo(1), Play against(2): "))
	if Choice == 1:
		email = input("Email: ")
		password = input("Password: ")
		Play_Solo(email, password)
	if Choice == 2:
		usrname = input("Email: ")
		password = input("Password: ")
		Play_Againest(usrname, password)


main()
