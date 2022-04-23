from tkinter import *
from main import *
import time #for clock on login screen

#CREATE SPLASH SCREEN
splash = Tk()
#centre splash
splash_width = 500
splash_height = 250

screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()

x = (screen_width / 2) - (splash_width / 2)
y = (screen_height / 2) - (splash_height / 2)

splash.geometry(f'{splash_width}x{splash_height}+{int(x)}+{int(y)}')

#hide title bar
splash.overrideredirect(True)

#splash image
splash_img = PhotoImage(file = "splash.png")
splash_img_label = Label(image=splash_img, borderwidth=0, highlightthickness=0)
splash_img_label.grid(row=0, column=0)	


#--- END OF SPLASH ---#

#CREATE LOGIN SCREEN
def login_init():
	#destroy splash screen when login window shows
	splash.destroy()
	global logo
	global footer

	#create LOGIN window
	login = Tk()
	#centre login window
	login_width = 700
	login_height = 450

	screen_width = login.winfo_screenwidth()
	screen_height = login.winfo_screenheight()

	x = (screen_width / 2) - (login_width / 2)
	y = (screen_height / 2) - (login_height / 2)

	login.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')

	#hide title bar
	login.overrideredirect(True)

	login.configure(background ="grey") 
	#login.iconbitmap("systemicon.ico") 
	logo = PhotoImage(file = "login.png")
	logo_label = Label(image=logo)
	logo_label.grid(row=0, column=0)

	def clock():
		disp_date = time.strftime("%x")
		disp_time = time.strftime("%X")
		#display variables above
		datetime.config(text=disp_date + " | " + disp_time, font=("Calibri", 13))
		#wait 1000ms on each refresh (using clock lib)
		datetime.after(1000,clock)

	datetime = Label(login, text="", bg="grey", fg="white")
	datetime.grid(row=1, column=0, padx=10, sticky=NW) 
	clock()	
	#get username/password strings from user
	username = StringVar()
	password = StringVar()
	#verify login from user entry
	def login_verify():

		user = (username.get())
		pas = (password.get())
		
		if user == "j" and pas == "1":
			correct_label = Label(login, bg="grey", fg="black", text="Logged in successfully. ")
			correct_label.grid(row=4, column=0, padx=(47, 0), ipady=4, ipadx=30, sticky=N)
			correct_label.config(font=("Calibri", 12))
			#initialise main 
			main()
		else:
			incorrect_label = Label(login, bg="grey", fg="red4", text="Incorrect Login, please try again. ")
			incorrect_label.grid(row=4, column=0, padx=(56, 0), ipady=4, sticky=N)
			incorrect_label.config(font=("Calibri", 12))

	def login_quit():
		login.quit()

	#credential login labels 

	username_label = Label(login, bg="grey", text="Username : ")
	username_label.grid(row=1, column=0, padx=(192, 0), pady=(30,0), ipady=4, sticky=W)
	username_label.config(font=("Calibri", 13))

	password_label = Label(login, bg="grey", text="Password : ")
	password_label.grid(row=2, column=0, padx=(196, 0), pady=(10,0), ipady=4, sticky=W)
	password_label.config(font=("Calibri", 13))

	#credential login boxes (280 is left padx, 0 is right padx)
	username = Entry(login, width=30, textvariable=username)
	username.grid(row=1, column=0, pady=(30, 0), padx=(280, 0), ipady=5, sticky=W)

	password = Entry(login, show="*", width=30, textvariable=password)
	password.grid(row=2, column=0, pady=(10, 0), padx=(280, 0), ipady=5,  sticky=W)

	#LOGIN SCREEN BUTTONS 

	#Login button (calls main function)
	login_button = Button(login, text="Login", command=login_verify, fg="white", bg="black")
	login_button.grid(row=3, column=0, pady=(8,0), padx=(279, 0), ipadx=18, ipady=10, sticky=W)
	login_button.config(font=("Calibri", 13))

	#QUIT BUTTON
	register_button_main = Button(login, text="Quit", command=login_quit,  fg="white", bg="black")
	register_button_main.grid(row=3, column=0, pady=(8,0), padx=(375, 0), ipadx=23, ipady=10, sticky=W)
	register_button_main.config(font=("Calibri", 13))

	#FOOTER
	footer = PhotoImage(file = "footer.png")
	footer_label = Label(image=footer, borderwidth=0, highlightthickness=0)
	footer_label.grid(row=4, column=0, sticky=S, pady=(40,0))

#splash timer - after 3s  initialise login, clock
splash.after(3000, login_init)

mainloop() 