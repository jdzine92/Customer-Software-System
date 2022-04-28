########################
###  JORDAN SYSTEMS  ###
########################

#--- IMPORT MODULES ---#
import tkinter as tk
import sqlite3
from tkinter import colorchooser #for setup colour function
from tkinter import messagebox
import login

#SET FONT
font_18 = ("Calibri", 18)
font_16 = ("Calibri", 16)
font_14 = ("Calibri", 14)
font_13 = ("Calibri", 13)

class Program:
	def __init__(self, main):
		self.main = main
  
		def create_db():
			#create database / connection
			conn = sqlite3.connect("demo.db")
   			#create cursor
			c = conn.cursor()
			#create table
			c.execute("""CREATE TABLE customer (
				first_name TEXT,
				last_name TEXT,
				DOB TEXT,
				address_l1 TEXT,
				address_l2 TEXT,
				address_l3 TEXT,
				postcode TEXT,
				email TEXT
			)
			 
			 """)
   
			#commit and close
			conn.commit()
			conn.close()
   
		#run once to create demo db / table
		#create_db()

		#FUNCTION FOR SEARCH
		def search():
			conn = sqlite3.connect("demo.db")
			c = conn.cursor()
   
			#get data from search_box
			user_search = search_box.get()
			#execute sql query (show any entries where last name = user_search)
			c.execute("SELECT * FROM customer WHERE last_name = (?)", (user_search,))
			result = c.fetchall()
   
			#if no match, print error message
			if not result:
				result = "Record not found, please try again."
			#else, display result on screen	
			#create search results frame
			global searchresultsframe
			searchresultsframe = tk.LabelFrame(main, fg="black", bg="gray80", width=845, height=300, borderwidth=0)
			searchresultsframe.grid(row=3, column=1, sticky=tk.NSEW)
			#force width and height on frame
			searchresultsframe.grid_propagate(0)
   
			#search results title
			search_results_lbl = tk.Label(searchresultsframe, fg="gray10", bg="gray80", font=font_16, text="Search Results ").grid(row=0, column=0, pady=(10,30), padx=(20,0), ipady=4, sticky=tk.W)
			#display search results
			user_search_lbl = tk.Label(searchresultsframe, fg="gray10", bg="gray80", font=font_13, text=result).grid(row=1, column=0, pady=(10,0), padx=(20,0))
   
			conn.commit()
			conn.close()
   
		#Submit data function for button inside frame
		#ADD RECORD TO DB
		def submit_record():
			#make global so add_record can access
			global submit_record
			#connect to database
			conn = sqlite3.connect("demo.db")
			#create cursor
			c = conn.cursor()

			#insert into table
			c.execute("INSERT INTO customer VALUES (:first_name, :last_name, :DOB, :address_l1, :address_l2, :address_l3, :postcode, :email)",
					{

						'first_name': first_name.get(),
						'last_name': last_name.get(),
						'DOB': DOB.get(),
						'address_l1': address_l1.get(),
						'address_l2': address_l2.get(),
						'address_l3': address_l3.get(),
						'postcode': postcode.get(),
						'email': email.get()
					}

				)
			#commit and close db
			conn.commit()
			conn.close()
			#display error or success message to user
			if c.rowcount < 1:
				error_lbl = tk.Label(addrecordframe, fg="red4", bg="gray80", font=font_14, text="Error, record was not entered. ").grid(row=11, column=2, pady=10, ipady=4, sticky=tk.W)
			else:
				success_lbl = tk.Label(addrecordframe, fg="green4", bg="gray80", font=font_14, text="Record entered sucessfully. ").grid(row=11, column=2, pady=10, ipady=4, sticky=tk.W)

			#clear textboxes after submitting
			first_name.delete(0, tk.END)
			last_name.delete(0, tk.END)
			DOB.delete(0, tk.END)
			address_l1.delete(0, tk.END)
			address_l2.delete(0, tk.END)
			address_l3.delete(0, tk.END)
			postcode.delete(0, tk.END)
			email.delete(0, tk.END)
   
		#FUNCTION FOR ADD RECORD BUTTON
		def add_record():
			#MENU element - CURRENT
			add_button = tk.Button(buttonframe, font=font_13, text="Add Record", command=add_record,  fg="white", bg="#254c6e", borderwidth=0).grid(row=3, column=0, ipadx=56, ipady=10, sticky=tk.W)
   
			#FRAME for add record, make global so submit_record, edit can access
			global addrecordframe
			addrecordframe = tk.LabelFrame(main, fg="black", bg="gray80", width=845, height=300, borderwidth=0)
			addrecordframe.grid(row=3, column=1, sticky=tk.NSEW)
			#force width and height on frame
			addrecordframe.grid_propagate(0)

			#add record title
			addrecord_lbl = tk.Label(addrecordframe, fg="gray10", bg="gray80", font=font_16, text="Adding new record ").grid(row=3, column=1, pady=(10,30), padx=(20,0), ipady=4, sticky=tk.W)

			#entry boxes (make global so submit_record() can access)
			global first_name
			global last_name
			global DOB
			global address_l1
			global address_l2
			global address_l3
			global postcode
			global email
   
			#keep .grid() separate, interferes with. get() for submit_record()
			first_name = tk.Entry(addrecordframe, width=30)
			first_name.grid(row=4, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			last_name = tk.Entry(addrecordframe, width=30)
			last_name.grid(row=4, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)
			DOB = tk.Entry(addrecordframe, width=15)
			DOB.grid(row=5, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			address_l1 = tk.Entry(addrecordframe, width=30)
			address_l1.grid(row=6, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			address_l2 = tk.Entry(addrecordframe, width=30)
			address_l2.grid(row=6, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)
			address_l3 = tk.Entry(addrecordframe, width=30)
			address_l3.grid(row=7, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			postcode = tk.Entry(addrecordframe, width=30)
			postcode.grid(row=7, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)
			email = tk.Entry(addrecordframe, width=30)
			email.grid(row=9, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)

			#text box labels
			first_name_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="First Name").grid(row=4, column=1, padx=10, pady=5, sticky=tk.E)
			last_name_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Last Name").grid(row=4, column=3, padx=10, sticky=tk.E)
			DOB_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="DOB").grid(row=5, column=1, padx=10, sticky=tk.E)
			address_l1_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Address Line 1").grid(row=6, column=1, padx=10, pady=5, sticky=tk.E)
			address_l2_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Address Line 2").grid(row=6, column=3, padx=10, pady=5, sticky=tk.E)
			address_l3_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="City").grid(row=7, column=1, padx=10, pady=5, sticky=tk.E)
			postcode_label = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Postcode").grid(row=7, column=3, padx=10, pady=5, sticky=tk.E)
			email_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Email").grid(row=9, column=1, padx=10, pady=5, sticky=tk.E)

			#Submit entry button
			submit_button = tk.Button(addrecordframe, font=font_14, text="Add Record", command=submit_record, fg="white", bg="black", borderwidth=0).grid(row=10, column=4, pady=10, padx=0, ipadx=5, ipady=5, sticky=tk.SE)
   
		#Delete function for Delete Record button
		def delete():
			#connect to database
			conn = sqlite3.connect("demo.db")
			#create cursor
			c = conn.cursor()
			#delete function (search by oid) get input from modify_id entry field
			c.execute("DELETE from customer WHERE oid = " + modify_id.get())
			#Commit and close connection
			conn.commit()
			conn.close()
   
		#Update record function for show_all()
		def update_record():
			#connect to database
			conn = sqlite3.connect("demo.db")
			#create cursor
			c = conn.cursor()
			#create record_id var
			record_id = modify_id.get()
			#update records (names on left when table was first created)
			#names on right are new variable
			c.execute("""UPDATE customer SET 
				first_name = :first,
				last_name = :last,
				DOB = :dob,
				address_l1 = :address_l1,
				address_l2 = :address_l2,
				address_l3 = :address_l3,
				postcode = :postcode,
				email = :email

				WHERE oid = :oid""",
				#designate key value pairs, tell program what these values are
				{
				'first':first_name_edit.get(),
				'last':last_name_edit.get(),
				'dob':DOB_edit.get(),
				'address_l1':address_l1_edit.get(),
				'address_l2':address_l2_edit.get(),
				'address_l3':address_l3_edit.get(),
				'postcode':postcode_edit.get(),
				'email':email_edit.get(),
				'oid': record_id
				})

			conn.commit()
			conn.close()

			#clear textboxes after submitting
			first_name_edit.delete(0, tk.END)
			last_name_edit.delete(0, tk.END)
			DOB_edit.delete(0, tk.END)
			address_l1_edit.delete(0, tk.END)
			address_l2_edit.delete(0, tk.END)
			address_l3_edit.delete(0, tk.END)
			postcode_edit.delete(0, tk.END)
			email_edit.delete(0, tk.END)
	
		#Edit function for Edit record button
		def edit():
			#FRAME edit record
			editrecordframe = tk.LabelFrame(main, bg="gray60", width=845, height=300, borderwidth=0)
			editrecordframe.grid(row=3, column=1, pady=10)
			#force width and height on frame
			editrecordframe.grid_propagate(0)

			#Edit record message
			editrecord_label = tk.Label(editrecordframe, fg="gray10", bg="gray60", font=font_13, text="Editing selected record ").grid(row=0, column=0, pady=10, padx=(20,0), ipady=4, sticky=tk.W)

			#SQLITE code for editing
			#connect to database
			conn = sqlite3.connect("demo.db")
			#create cursor
			c = conn.cursor()
			#get user input from delete box
			record_id = modify_id.get()
			#run query (select everything that matches user oid)
			c.execute("SELECT * FROM customer WHERE oid = " + record_id)
		
			#fetch all records (assign var)
			records = c.fetchall()

			#make entry boxes global
			global first_name_edit
			global last_name_edit
			global DOB_edit
			global address_l1_edit
			global address_l2_edit
			global address_l3_edit
			global postcode_edit
			global email_edit

			#entry boxes for edit keep .grid() separate for .get()
			
			first_name_edit = tk.Entry(editrecordframe, width=30)
			first_name_edit.grid(row=4, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			
			last_name_edit = tk.Entry(editrecordframe, width=30)
			last_name_edit.grid(row=4, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)
			
			DOB_edit = tk.Entry(editrecordframe, width=15)
			DOB_edit.grid(row=5, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)

			address_l1_edit = tk.Entry(editrecordframe, width=30)
			address_l1_edit.grid(row=6, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			
			address_l2_edit = tk.Entry(editrecordframe, width=30)
			address_l2_edit.grid(row=6, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)
			
			address_l3_edit = tk.Entry(editrecordframe, width=30)
			address_l3_edit.grid(row=7, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)

			postcode_edit = tk.Entry(editrecordframe, width=30)
			postcode_edit.grid(row=7, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)
   
			email_edit = tk.Entry(editrecordframe, width=30)
			email_edit.grid(row=8, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)

			#text box labels
			first_name_label = tk.Label(editrecordframe, fg="white", bg="gray30", text="First Name").grid(row=4, column=1, padx=10, pady=5, sticky=tk.E)
			last_name_label = tk.Label(editrecordframe, fg="white", bg="gray30", text="Last Name").grid(row=4, column=3, padx=10, sticky=tk.E)
			DOB_label = tk.Label(editrecordframe, fg="white", bg="gray30", text="DOB").grid(row=5, column=1, padx=10, sticky=tk.E)
			address_l1_label = tk.Label(editrecordframe, fg="white", bg="gray30", text="Address Line 1").grid(row=6, column=1, padx=10, pady=5, sticky=tk.E)
			address_l2_label = tk.Label(editrecordframe, fg="white", bg="gray30", text="Address Line 2").grid(row=6, column=3, padx=10, pady=5, sticky=tk.E)
			address_l3_label = tk.Label(editrecordframe, fg="white", bg="gray30", text="City").grid(row=7, column=1, padx=10, pady=5, sticky=tk.E)
			postcode_label = tk.Label(editrecordframe, fg="white", bg="gray30", text="Postcode").grid(row=7, column=3, padx=10, pady=5, sticky=tk.E)
			email_label = tk.Label(editrecordframe, fg="white", bg="gray30", text="Email").grid(row=8, column=1, padx=10, pady=5, sticky=tk.E)

			#Save edited record button (keep .grid() separate
			submit_button = tk.Button(editrecordframe, font=font_14, text="Save Record", command=update_record,  fg="white", bg="black")
			submit_button.grid(row=9, column=2, pady=10, padx=20, ipadx=5, ipady=5)

			#Insert ORIGINAL data into fields 
			for record in records:
				first_name_edit.insert(0, record[0])
				last_name_edit.insert(0, record[1])
				DOB_edit.insert(0, record[2])
				address_l1_edit.insert(0, record[3])
				address_l2_edit.insert(0, record[4])
				address_l3_edit.insert(0, record[5])
				postcode_edit.insert(0, record[6])
				email_edit.insert(0, record[7])

			#commit and close db
			conn.commit()
			conn.close()
	
		#Display function for SHOW_ALL
		def show_all():
			#FRAME for show all
			global showrecordframe
			showrecordframe = tk.LabelFrame(main, bg="gray80", width=845, height=500, borderwidth=0)
			showrecordframe.grid(row=3, column=1, pady=10)
			#force width and height on frame
			showrecordframe.grid_propagate(0)
   
			#show all record title
			showrecord_lbl = tk.Label(showrecordframe, fg="gray10", bg="gray80", font=font_16, text="Showing All Records ").grid(row=0, column=0, pady=5, padx=(20,0), ipady=4, sticky=tk.W)

			#connect to database
			conn = sqlite3.connect("demo.db")
			#create cursor
			c = conn.cursor()
			#Show user how many records there are in db
			#run query (select everything)
			c.execute("SELECT * FROM customer")
			records = c.fetchall()
			recordcount = len(records)
		
			#showing all records label
			allrecords_lbl = tk.Label(showrecordframe, fg="gray30", bg="gray80", font=font_13, text="There are " + str(recordcount) + " records to display").grid(row=1, column=0, padx=(20, 0), pady=(5,0), ipady=4, sticky=tk.W)
			#run query (select everything and the primary key(oid))
			c.execute("SELECT *,oid FROM customer")
			#fetch all records (assign var)
			#show all records in the system
			records = c.fetchall()
			#format results - record[8] refers to the oid (primary key)
			print_records = ''
			for record in records:
				print_records += str(record[8]) + " | " + str(record[0]) + " " + str(record[1]) + "\n" + str(record[2]) + "\n" + str(record[3]) + ", " + str(record[4]) + ", " + str(record[5]) + ", " + str(record[6] + "\n" + str(record[7])) + "\n\n" 
			#show results in query label
			query_lbl = tk.Label(showrecordframe, text=print_records).grid(row=3, column=0, columnspan=2, pady=10, padx=30, ipadx=10, ipady=10, sticky=tk.W)		
			#commit and close db
			conn.commit()
			conn.close()
			#Delete entry box label
			modify_id_lbl = tk.Label(showrecordframe, font=font_13, text="Select ID to modify: ", fg="gray30", bg="gray80").grid(row=4, column=2, pady=(0,0), padx=(30, 0), sticky=tk.E)
			#Entry box to enter ID the user wishes to delete from DB
			#make global so we can use .get() in delete()
			global modify_id
			modify_id = tk.Entry(showrecordframe, width=10)
			#keep .grid separate (interferes with .get() when chained)
			modify_id.grid(row=4, column=3, padx=(10,0), pady=(5,0), sticky=tk.E)
			#delete button - calls DEF DELETE
			delete_button = tk.Button(showrecordframe, font=font_13, text="Delete Record", command=delete,  fg="white", bg="black", borderwidth=0)
			delete_button.grid(row=5, column=2, pady=(10,0), padx=(30,0), ipadx=10, ipady=10, sticky=tk.E)
			#edit button - calls DEF EDIT
			edit_button = tk.Button(showrecordframe, font=font_13, text="Edit Record", command=edit, fg="white", bg="black", borderwidth=0)
			edit_button.grid(row=5, column=3, pady=(10,0), padx=(5,0), ipadx=16, ipady=10, sticky=tk.E)	

  
		#FUNCTION FOR SETUP
		def setup():
			#FRAME for setup
			setupframe = tk.LabelFrame(main, bg="gray30", width=750, height=450, borderwidth=0)
			setupframe.grid(row=3, column=1, pady=10)
			#force width and height on frame
			setupframe.grid_propagate(0)
			#Setup welcome message
			wel_setup = tk.Label(setupframe, fg="white", bg="gray30", text="Setup ")
			wel_setup.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)
			wel_setup.config(font=("Calibri", 16))

			def color():
				#make global so that program can access
				select_color = colorchooser.askcolor()
				select_color.set("blue")
				#call colour window
				select_color = colorchooser.askcolor()
				
			sel_clr_btn = tk.Button(setupframe, text="Set Theme", command=color, borderwidth=0)
			sel_clr_btn.grid(row=7, column=1, padx=20)
			sel_clr_btn.config(font=("Calibri", 13))
  
		#FUNCTION FOR CALCULATOR
		def calc():
			#FRAME 
			calcframe = tk.LabelFrame(main, bg="gray80", width=845, height=500, borderwidth=0)
			calcframe.grid(row=3, column=1, pady=10)
			#force width and height on frame
			calcframe.grid_propagate(0)
			#Calculator welcome message
			calc_title = tk.Label(calcframe, fg="gray10", bg="gray80", font=font_16, text="Calculator").grid(row=0, column=0, padx=10, sticky=tk.W)
			e = tk.Entry(calcframe, width=20, borderwidth=5, font=font_16)
			#keep separate for get functionality
			e.grid(row=1, column=1, columnspan=3, padx=15, pady=15,  sticky=tk.NSEW)

			def btn_click(number):
				current = e.get() 
				e.delete(0, tk.END) 
				e.insert(0, str(current) + str(number)) #insert the current + new number that was pressed (str for display only, not for calculations)

			def btn_clear():
				e.delete(0, tk.END) 

			def btn_equal():
				second_num = float(e.get()) 
				e.delete(0, tk.END) 
				
				if math == "add": 
					e.insert(0, first_num + float(second_num))
				if math == "sub": 
					e.insert(0, first_num - float(second_num))
				if math == "mul": 
					e.insert(0, first_num * float(second_num))
				if math == "div": 
					e.insert(0, first_num / float(second_num))
					
			def btn_add(): 
				global first_num 
				global math
				first_num = float(e.get()) 
				math = "add"
				e.delete(0, tk.END) 

			def btn_sub():
				global first_num 
				global math
				first_num = float(e.get()) 
				math = "sub"
				e.delete(0, tk.END) 

			def btn_mul():
				global first_num 
				global math
				first_num = float(e.get()) 
				math = "mul"
				e.delete(0, tk.END)

			def btn_div():
				global first_num 
				global math
				first_num = float(e.get()) 
				math = "div"
				e.delete(0, tk.END)
	
			def btn_save():
					value = e.get()
					value_label = tk.Label(calcframe, fg="white", bg="gray30", text=value, font=font_16).grid(row=1, column=5, sticky=tk.E)
	
					
			#CREATE NUMBER BUTTONS (0-9)
			''' we have to use the lambda function to pass parameters in, as with tkinter
			you cannot add () inside the brackets. we want the value of the button to be equal
			to its number on screen, so 1=1 2=2 etc. '''
			btn_1 = tk.Button(calcframe, fg="white", bg="#254c6e", text="1", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(1))
			btn_2 = tk.Button(calcframe, fg="white", bg="#254c6e", text="2", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(2))
			btn_3 = tk.Button(calcframe, fg="white", bg="#254c6e", text="3", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(3))
			btn_4 = tk.Button(calcframe, fg="white", bg="#254c6e", text="4", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(4))
			btn_5 = tk.Button(calcframe, fg="white", bg="#254c6e", text="5", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(5))
			btn_6 = tk.Button(calcframe, fg="white", bg="#254c6e", text="6", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(6))
			btn_7 = tk.Button(calcframe, fg="white", bg="#254c6e", text="7", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(7))
			btn_8 = tk.Button(calcframe, fg="white", bg="#254c6e", text="8", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(8))
			btn_9 = tk.Button(calcframe, fg="white", bg="#254c6e", text="9", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(9))
			btn_0 = tk.Button(calcframe, fg="white", bg="#254c6e", text="0", padx=40, font=font_16, borderwidth=3, command=lambda: btn_click(0))
			btn_dot = tk.Button(calcframe, fg="white", bg="#254c6e", text=".", padx=43, font=font_16, borderwidth=3, command=lambda: btn_click('.'))
			#CREATE OPERATOR BUTTONS (WITH OWN FUNCTIONS)
			btn_add = tk.Button(calcframe, fg="white", bg="#254c6e", text="+", padx=40, font=font_16, command=btn_add, borderwidth=3)
			btn_sub = tk.Button(calcframe, fg="white", bg="#254c6e", text="-", padx=42, font=font_16, command=btn_sub, borderwidth=3)
			btn_mul = tk.Button(calcframe, fg="white", bg="#254c6e", text="*", padx=41, font=font_16, command=btn_mul, borderwidth=3)
			btn_div = tk.Button(calcframe, fg="white", bg="#254c6e", text="/", padx=41, font=font_16, command=btn_div, borderwidth=3)
			btn_equal = tk.Button(calcframe, fg="white", bg="#254c6e", text="=", padx=95, font=font_16, command=btn_equal, borderwidth=3)
			btn_clear = tk.Button(calcframe, fg="white", bg="#254c6e", text="AC", padx=33, font=font_16, command=btn_clear, borderwidth=3)
			btn_save = tk.Button(calcframe, fg="white", bg="#254c6e", text="SAVE", padx=10, font=font_16, command=btn_save, borderwidth=3)	

			#DISPLAY BUTTONS (0-9) 
			btn_1.grid(row=4, column=1, sticky=tk.E)
			btn_2.grid(row=4, column=2, sticky=tk.E)
			btn_3.grid(row=4, column=3, sticky=tk.E)
			btn_4.grid(row=3, column=1, sticky=tk.E)
			btn_5.grid(row=3, column=2, sticky=tk.E)
			btn_6.grid(row=3, column=3, sticky=tk.E)
			btn_7.grid(row=2, column=1, sticky=tk.E)
			btn_8.grid(row=2, column=2, sticky=tk.E)
			btn_9.grid(row=2, column=3, sticky=tk.E)
			btn_0.grid(row=5, column=1, sticky=tk.E)
			btn_dot.grid(row=5, column=2, sticky=tk.E)
			#DISPLAY OPERATOR BUTTONS
			btn_add.grid(row=6, column=1, sticky=tk.E)
			btn_sub.grid(row=7, column=1, sticky=tk.E)
			btn_mul.grid(row=7, column=2, sticky=tk.E)
			btn_div.grid(row=7, column=3, sticky=tk.E)
			btn_equal.grid(row=6, column=2, columnspan=2, sticky=tk.E) 
			btn_clear.grid(row=5, column=3, sticky=tk.E)
			btn_save.grid(row=7, column=4, sticky=tk.E)
   			
	
		#QUIT
		def quit():
			log_out = messagebox.askyesno("Log Out", "You are about to log out, are you sure ?")
			if log_out == 'yes':
				main.destroy()
  
		#--- LOGOFRAME ---#
		#Define logoframe size/position
		logoframe = tk.LabelFrame(main, bg="#eee", width=1000, height=125, borderwidth=0)
		logoframe.grid(row=0, column=0, columnspan=4, ipadx=25, sticky=tk.N)
		#force width and height on frame
		logoframe.grid_propagate(0)
		#Define logo image and grid position (using self to stop auto garbage collection)
		self.logo = tk.PhotoImage(file = "wel.png")
		logo_label = tk.Label(logoframe, image=self.logo,  borderwidth=0, highlightthickness=0)
		logo_label.grid(row=0, column=0)
  
		#--- SEARCHFRAME ---#
		#Define searchframe size/position
		searchframe = tk.LabelFrame(main, bg="gray30", width=1000, height=100, borderwidth=0)
		searchframe.grid(row=1, column=0, ipadx=25, columnspan=4, sticky=tk.N)
		#Force width and height on frame
		searchframe.grid_propagate(0)
  
		#remove default text on left click
		def on_click(event):
			search_box.delete(0, tk.END)
   
		#Search entry box size/position
		search_box = tk.Entry(searchframe, width=50,)
		search_box.grid(row=2, column=0, padx=(80,0), ipady=2, sticky=tk.W)
		#bind click event <Button-1> is a left click
		search_box.bind("<Button-1>", on_click)
   
  		#predefined text on search box
		search_box.insert(0, "Search by surname, Example: Smith John.")
		#Search button size/position. DEF QUERY will be called from rootfunc.py file
		search_button = tk.Button(searchframe, text="Search Records", command=search,  fg="white", bg="#6492b6", borderwidth=0)
		search_button.grid(row=2, column=0, pady=10, padx=(400,0), sticky=tk.W)
		search_button.config(font=("Calibri", 14))
		#Search welcome message
		search_wel_label = tk.Label(searchframe, wraplength=350, fg="white", bg="gray30", text="To get started search for a customer below: ")
		search_wel_label.grid(row=1, column=0, padx=(90, 0), pady=(5,0), sticky=tk.W)
		search_wel_label.config(font=("Calibri", 12))
  
		#--- BUTTONFRAME ---#
		#Create button frame
		buttonframe = tk.LabelFrame(main, bg="#6492b6", borderwidth=0)
		buttonframe.grid(row=3, column=0, ipady=120, sticky=tk.NW)

		#--- MENU BUTTONS ---#
		#Add button - calls add_record() / submit_record()
		global add_button
		add_button = tk.Button(buttonframe, text="Add Record", command=add_record,  fg="white", bg="#366f9e", borderwidth=0)
		add_button.grid(row=3, column=0, ipadx=56, ipady=10, sticky=tk.W)
		add_button.config(font=("Calibri", 13))
  
		#Show all records button = calls show_all()
		show_all_button = tk.Button(buttonframe, text="Show All Records", command=show_all, fg="white", bg="#366f9e", borderwidth=0)
		show_all_button.grid(row=4, column=0, ipadx=36, ipady=10, sticky=tk.W)
		show_all_button.config(font=("Calibri", 13))
  
		#calculator button
		calc_button = tk.Button(buttonframe, text="Calculator", command=calc,  fg="white", bg="#366f9e", borderwidth=0)
		calc_button.grid(row=6, column=0, ipadx=61, ipady=10, sticky=tk.W)
		calc_button.config(font=("Calibri", 13))

		#Setup button - calls DEF SETUP
		setup_button = tk.Button(buttonframe, text="Setup", command=setup, fg="white", bg="#366f9e", borderwidth=0)
		setup_button.grid(row=7, column=0, ipadx=76, ipady=10, sticky=tk.W)
		setup_button.config(font=("Calibri", 13))

		#Quit button - calls DEF QUIT
		quit_button = tk.Button(buttonframe, text="Quit", command=quit,  fg="white", bg="#366f9e", borderwidth=0)
		quit_button.grid(row=8, column=0, ipadx=81, ipady=10, sticky=tk.W)
		quit_button.config(font=("Calibri", 13))
  
#GET USERNAME
def get_user():
	return login.get_user()
  
	 		
#RUN TKINTER MAINLOOP		
def main(): 
	#toplevel window, DO NOT CHANGE
	root = tk.Toplevel()
	#Declare an instance of the Program class to init program
	program = Program(root)
	username = get_user()
	root.title("Welcome  " + username)
	#Set window size
	root.geometry("1000x700")
	root.configure(background ="white") 
	root.iconbitmap("systemicon.ico") 
	root.resizable(False, False)
	
	tk.mainloop()
	
#run main if being run as standalone
if __name__ == '__main__':
	main()