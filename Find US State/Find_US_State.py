from selenium import webdriver
from selenium.common.exceptions import *

from time import sleep
from time import time
from colorama import init, Fore

from State_DB import *

init(autoreset=True)


def is_win():
	import os
	if os.name == 'nt':
		return True
	else:
		return False
	


class Status_Code():
	Status_OK = "[{}+{}]".format(Fore.LIGHTGREEN_EX, Fore.RESET)
	Status_FATAL = "[{}-{}]".format(Fore.LIGHTRED_EX, Fore.RESET)
	Status_INFO = "[{}*{}]".format(Fore.LIGHTBLUE_EX, Fore.RESET)
	Status_WARNING = "[{}!{}]".format(Fore.LIGHTYELLOW_EX, Fore.RESET)


class Play(object):
	

	def __init__(self, email, password, GameType, Delay):
		"""
		Email: User's Email to login to Sporcle
		Password: User's Password to login to Sporcle
		Game Type: OutLine or No Outline
		if Outline(variable) is false:
		this enter No outline Find state [https://www.sporcle.com/games/mhershfield/us-states-no-outlines-minefield]
		else:
		Enter Outline Find State [https://www.sporcle.com/games/Matt/find_the_states]
		"""

		self.Delay = Delay

		self.Game_Type = int(GameType)

		self.Email = email
		self.Password = password

		if self.Game_Type == 1:
			self.Play_URL = 'https://www.sporcle.com/games/Matt/find_the_states'
			self.State_DB = State_Element.State_Element_Outline
		elif self.Game_Type == 2:
			self.Play_URL = 'https://www.sporcle.com/games/mhershfield/us-states-no-outlines-minefield'
			self.State_DB = State_Element.State_Element_No_Outline
		elif self.Game_Type == 3:
			self.Play_URL = 'https://www.sporcle.com/games/teedslaststand/build-me-a-map'
			self.State_DB = State_Element.State_Element_Hidden

		super().__init__()


	@staticmethod
	def Login(Driver, Email, Password):
		"""
		Login to sporcle using users email and password
		"""
		username_input = Driver.find_element_by_id('username_gamepage')
		username_input.send_keys(Email)
		print(Status_Code.Status_INFO + "ENTERING USERNAME")
		password_input = Driver.find_element_by_id('password_gamepage')
		password_input.send_keys(Password)
		print(Status_Code.Status_INFO + "ENTERING PASSWORD")
		print(Status_Code.Status_INFO + "LOGGING IN")
		Driver.find_element_by_id('game_page_login_btn').click()
		sleep(1)
		try:
			if Driver.find_element_by_id('game_page_login_error').is_displayed():
				print(Status_Code.Status_FATAL + "Failed to login. Please manuly login and Press Enter to continue")
				input("Press Enter to Continue")
		except:
			pass

		print(Status_Code.Status_OK + "Login Success")
		sleep(1)


	def Play_Solo(self):
		print(Status_Code.Status_INFO + "Starting a new chrome session")

		if is_win():
			self.Driver = webdriver.Chrome('chromedriver.exe')
		else:
			self.Driver = webdriver.Chrome('./chromedriver')

		print(Status_Code.Status_INFO + "Getting Sporcle Quiz Page")
		self.Driver.get(self.Play_URL)
		print(Status_Code.Status_OK + "Page loading complete")
		
		print(Status_Code.Status_INFO + "Starting Login Procedure")
		Play.Login(self.Driver, self.Email, self.Password)

		try:
			sleep(1)
			self.Driver.find_element_by_id("button-play").click()
		except:
			print(Status_Code.Status_FATAL + "Failed to click on PLAY QUIZ Button, Please click it then press Enter")
			input("Press Enter To Continue")

		print(Status_Code.Status_INFO + "Starting")

		time_start = time()
		for x in range(50):
			try:
				Current_State = self.Driver.find_element_by_id('currgamename').text
				print('\n' + Current_State)
				Element = self.State_DB.get(Current_State)
				print(Element)
				sleep(self.Delay)
				self.Driver.find_element_by_id(Element).click()
			except WebDriverException as unknowError:
				print(Status_Code.Status_FATAL + "Encountered an exception. Exception Msg: {}".format(unknowError))
				print(Status_Code.Status_WARNING + "At S: {}. E: {}".format(Current_State, Element))
				print(Status_Code.Status_INFO + "Ignoring last exception. Continuing")
				self.Driver.execute_script('pickSlot();')
		time_end = time()
		print(Status_Code.Status_OK + "DONE in {} seconds.".format(round(time_end-time_start, 1)))
		
		input("Press Enter To Exit")


	def Play_Against(self):
		print(Status_Code.Status_INFO + "Starting a new chrome session")

		if is_win():
			self.Driver = webdriver.Chrome('chromedriver.exe')
		else:
			self.Driver = webdriver.Chrome('./chromedriver')
		
		print(Status_Code.Status_INFO + "Getting Sporcle Quiz Page")
		self.Driver.get(self.Play_URL)
		print(Status_Code.Status_OK + "Page loading complete")
		
		print(Status_Code.Status_INFO + "Starting Login Procedure")
		Play.Login(self.Driver, self.Email, self.Password)

		while True:  # For playing again
			
			try:
				self.Driver.find_element_by_id('button-connect-showdown').click()
			except:
				print(Status_Code.Status_FATAL + "FAILED TO CLICK ON FIND OPPONENT BTN. PLEASE CLICK IT THEN PRESS ENTER")
				input("PRESS ENTER TO CONTINUE")


			Wait_Oppoent_Time = 0
			while True:	
				if self.Driver.find_element_by_id('answer-wrapper').is_displayed():
					break
				Wait_Oppoent_Time += 1
				print("Matching up for opponent. Time Elapsed: {}".format(Wait_Oppoent_Time), end='\r')
				sleep(1)
			print('\n')


			try:
				last_state = None
				time_start = time()
				for x in range(50):
					try:
							sleep(self.Delay)
							Current_State = self.Driver.find_element_by_id('currgamename').text  # Get Current State
							if last_state == Current_State:
								print(Status_Code.Status_WARNING + "STATE REPEATED. S: {}. E: {}. D: {}. POSSIBLY CAUSED BY EXTREMLY SHORT DELAY TIME")
								print(Status_Code.Status_INFO + "IGNORING REPEATED STATE. CONTINUING\n")
								continue
							print(Current_State)
							Element = self.State_DB.get(Current_State)
							self.Driver.find_element_by_id(Element).click()
							last_state = Current_State
							continue
					except WebDriverException as unknowError:
						print(Status_Code.Status_FATAL + "Encountered an exception. Exception Msg: {}".format(unknowError))
						print(Status_Code.Status_WARNING + "At S: {}. E: {}".format(Current_State, Element))
						print(Status_Code.Status_INFO + "Ignoring last exception. Continuing\n\n")
						self.Driver.execute_script('pickSlot();')
			except NoSuchElementException:
				print(Status_Code.Status_INFO + "EXCEPTION ENCOUNTERED. ASSUMING DONE. CONTINUING")

			time_end = time()
			print(Status_Code.Status_OK + "Done in {} seconds\n".format(round(time_end - time_start, 1)))

			ask_PlayAgain = int(input("Play again? Yes(1) No(2):"))
			if ask_PlayAgain == 1:
				try:
					self.Driver.find_element_by_id('button-replay').click()
				except:
					print(Status_Code.Status_FATAL + "FAILED TO CLICK ON PLAY AGAIN BUTTON, PLEASE CLICK IT AND PRESS ENTER TO CONTINUE")
					input("PRESS ENTER TO CONTINUE")
				sleep(0.5)
				continue
			if ask_PlayAgain == 2:
				raise SystemExit(0)
	
def main():
	askPlayType = int(input("Find State: Outline(1)/No Outline(2)/Hidden(3): "))
	askPlayAgainst = int(input("Play SOLO(1)/Against(2): "))
	askDelay = float(input("Delay (seconds):"))
	askEmail = input("Email: ")
	askPassword = input("Password: ")

	if askPlayAgainst == 1:
		Play(askEmail, askPassword, askPlayType, askDelay).Play_Solo()
	elif askPlayAgainst == 2:
		Play(askEmail, askPassword, askPlayType, askDelay).Play_Against()


main()
