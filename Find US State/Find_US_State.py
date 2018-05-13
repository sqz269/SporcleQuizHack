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


class Play(object):
	

	def __init__(self, email, password, GameType):
		"""
		Email: User's Email to login to Sporcle
		Password: User's Password to login to Sporcle
		Game Type: OutLine or No Outline
		if Outline(variable) is false:
		this enter No outline Find state [https://www.sporcle.com/games/mhershfield/us-states-no-outlines-minefield]
		else:
		Enter Outline Find State [https://www.sporcle.com/games/Matt/find_the_states]
		"""
		if GameType == 1:
			self.Outline = True
		else:
			self.Outline = False

		self.Email = email
		self.Password = password

		if self.Outline:
			self.Play_URL = 'https://www.sporcle.com/games/Matt/find_the_states'
			self.State_DB = State_Element.State_Element_Outline
		else:
			self.Play_URL = 'https://www.sporcle.com/games/mhershfield/us-states-no-outlines-minefield'
			self.State_DB = State_Element.State_Element_No_Outline

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
		self.Driver = webdriver.Chrome('chromedriver.exe')
		
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

		for x in range(50):
			Current_State = self.Driver.find_element_by_id('currgamename').text
			print('\n' + Current_State)
		# The following state will raise a error for some reason if encountered.
			if Current_State == "Michigan":
				self.Driver.execute_script('pickSlot();')
				print(Status_Code.Status_WARNING + "S Michigan. E a21. WARN. O_E RECV CLK. NXT")
				sleep(0.2)
				continue
			if Current_State == 'Hawaii':
				self.Driver.execute_script('pickSlot();')
				print(Status_Code.Status_WARNING + "S Hawaii. E a10. WARN. O_E RECV CLK. NXT")
				sleep(0.2)
				continue
			if Current_State == "Louisiana":
				self.Driver.execute_script('pickSlot();')
				print(Status_Code.Status_WARNING + "S Louisiana. E a17. WARN. O_E RECV CLK. NXT")
				sleep(0.2)
				continue
			if Current_State == "Florida":
				self.Driver.execute_script('pickSlot();')
				print(Status_Code.Status_WARNING + "S Florida. E a8. WARN. O_E RECV CLK. NXT")
				sleep(0.2)
				continue
			Element = self.State_DB.get(Current_State)
			print(Element)
			sleep(0.2)
			self.Driver.find_element_by_id(Element).click()
		print(Status_Code.Status_OK + "DONE")
		
		input("Press Enter To Exit")


	def Play_Against(self):
		print(Status_Code.Status_INFO + "Starting a new chrome session")
		self.Driver = webdriver.Chrome('chromedriver.exe')
		
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


			try:
				for x in range(50):
						sleep(0.3)
						Current_State = self.Driver.find_element_by_id('currgamename').text  # Get Current State
						print(Current_State)
						# The following state will cause an unknown error if try to click on it
						if Current_State == "Michigan":
							self.Driver.execute_script('pickSlot();')
							print(Status_Code.Status_WARNING + "S Michigan. E a21. WARN. O_E RECV CLK. NXT")
							sleep(0.2)
							continue
						if Current_State == 'Hawaii':
							self.Driver.execute_script('pickSlot();')
							print(Status_Code.Status_WARNING + "S Hawaii. E a10. WARN. O_E RECV CLK. NXT")
							sleep(0.2)
							continue
						if Current_State == "Louisiana":
							self.Driver.execute_script('pickSlot();')
							print(Status_Code.Status_WARNING + "S Louisiana. E a17. WARN. O_E RECV CLK. NXT")
							sleep(0.2)
							continue
						if Current_State == "Florida":
							self.Driver.execute_script('pickSlot();')
							print(Status_Code.Status_WARNING + "S Florida. E a8. WARN. O_E RECV CLK. NXT")
							sleep(0.2)
							continue
						Element = self.State_DB.get(Current_State)
						self.Driver.find_element_by_id(Element).click()
						continue
			except NoSuchElementException:
				print(Status_Code.Status_INFO + "EXCEPTION ENCOUNTERED. ASSUMING DONE. CONTINUING")

			print(Status_Code.Status_OK + "Done\n")

			ask_PlayAgain = int(input("Play again? Yes(1) No(2):"))
			if ask_PlayAgain == 1:
				self.Driver.find_element_by_id('button-replay').click()
				sleep(0.5)
				continue
			if ask_PlayAgain == 2:
				raise SystemExit(0)
	
def main():
	askPlayType = int(input("Find State: Outline(1)/No Outline(2): "))
	askPlayAgainst = int(input("Play SOLO(1)/Against(2): "))
	askEmail = input("Email: ")
	askPassword = input("Password: ")

	if askPlayAgainst == 1:
		Play(askEmail, askPassword, askPlayType).Play_Solo()
	elif askPlayAgainst == 2:
		Play(askEmail, askPassword, askPlayType).Play_Against()


main()
