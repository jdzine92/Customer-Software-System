########################
###  JORDAN SYSTEMS  ###
########################

#--- IMPORT MODULES ---#
import tkinter as tk
from tkinter import ttk
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
   			#define required fields as NOT NULL
			c.execute("""CREATE TABLE customer (
				title TEXT,
				first_name TEXT NOT NULL,
				last_name TEXT NOT NULL,
				DOB TEXT,
				address_l1 TEXT NOT NULL,
				address_l2 TEXT,
				address_l3 TEXT,
				postcode TEXT NOT NULL,
				email TEXT,
				telephone INTEGER NOT NULL
	
				 
			)
			 
			 """);
   
			#commit and close
			conn.commit()
			conn.close()
   
		#run once to create demo db / table
		#create_db()

		#FUNCTION FOR SEARCH
		def search():
			#destroy any other frames open
			destroy_frames()
			#create search results frame
			global searchresultsframe
			searchresultsframe = tk.Frame(main, bg="gray80", width=1215, height=400, borderwidth=0)
			searchresultsframe.grid(row=2, column=1, sticky=tk.NSEW)
			#force width and height on frame
			searchresultsframe.grid_propagate(0)

			#search results title
			search_results_lbl = tk.Label(searchresultsframe, fg="gray10", bg="gray80", font=font_16, text="Search Results ").grid(row=0, column=0, pady=10, padx=(20,0), ipady=4, sticky=tk.W)
			conn = sqlite3.connect("demo.db")
			c = conn.cursor()
   
			#get data from search_box
			user_search = search_box.get()
			#execute sql query (show entries where last name = user_search)
			c.execute("SELECT first_name, last_name FROM customer WHERE last_name = (?)", (user_search,))
			result = c.fetchall()
			recordcount = len(result)
   
			#if no match, print error message
			if not result:
				no_results_lbl = tk.Label(searchresultsframe, fg="red4", bg="gray80", font=font_13, text="No record match, please search again.").grid(row=1, column=0, pady=(10,0), padx=(20,0))
			#else, display result on screen	
			else:
				#display num of entries returned
				num_records_lbl = tk.Label(searchresultsframe, fg="green4", bg="gray80", font=font_13, text=str(recordcount) + " results found" ).grid(row=1, column=0, pady=(10,0), padx=(20,0))
				#display search results
				show_results = ''
				for results in result:
					show_results += str(results[0]) + " " + str(results[1])
				show_results_lbl = tk.Label(searchresultsframe, fg="gray10", bg="gray80", font=font_13, text=show_results).grid(row=2, column=0, pady=(10,0), padx=(20,0))
   
			conn.commit()
			conn.close()
   
		#Submit data function for button inside frame
		#ADD RECORD TO DB
		def submit_record():
			#validate data entry first
			if first_name.get() == '':
				messagebox.showerror('Error!', 'First Name cannot be blank.')
			elif last_name.get() == '':
					messagebox.showerror('Error!', 'Last Name cannot be blank.')
			elif address_l1.get() == '':
					messagebox.showerror('Error!', 'Address Line 1 cannot be blank.')
			elif postcode.get() == '':
					messagebox.showerror('Error!', 'Postcode cannot be blank.')
			elif telephone.get() == '':
					messagebox.showerror('Error!', 'Phone cannot be blank.')
			else:
				#make global so add_record can access
				global submit_record
				#connect to database
				conn = sqlite3.connect("demo.db")
				#create cursor
				c = conn.cursor()

				#insert into table
				c.execute("INSERT INTO customer VALUES (:title, :first_name, :last_name, :DOB, :address_l1, :address_l2, :address_l3, :postcode, :email, :telephone)",
						{
							'title': title.get(),
							'first_name': first_name.get(),
							'last_name': last_name.get(),
							'DOB': DOB.get(),
							'address_l1': address_l1.get(),
							'address_l2': address_l2.get(),
							'address_l3': address_l3.get(),
							'postcode': postcode.get(),
							'email': email.get(),
							'telephone': telephone.get()
						}

					)
				#commit and close db
				conn.commit()
				conn.close()
				#display error or success message to user
				if c.rowcount < 1:
					error_lbl = tk.Label(addrecordframe, fg="red4", bg="gray80", font=font_14, text="Error, record entry failed. Please contact HelpDesk on xxxx-xxx-xxxx").grid(row=11, column=2, pady=10, ipady=4, sticky=tk.W)
				else:
					success_lbl = tk.Label(addrecordframe, fg="green4", bg="gray80", font=font_14, text="Record entered sucessfully. ").grid(row=11, column=3, pady=10, ipady=4, sticky=tk.W)

				#clear textboxes after submitting
				title.delete(0, tk.END)
				first_name.delete(0, tk.END)
				last_name.delete(0, tk.END)
				DOB.delete(0, tk.END)
				address_l1.delete(0, tk.END)
				address_l2.delete(0, tk.END)
				address_l3.delete(0, tk.END)
				postcode.delete(0, tk.END)
				email.delete(0, tk.END)
				telephone.delete(0, tk.END)
	
		#FUNCTION FOR ADD RECORD BUTTON
		def add_record():
			#destroy any other frames open
			destroy_frames()
   			#handle current tab colour
			handle_current_tab("addrecord")
			#FRAME for add record, make global so submit_record, edit can access
			global addrecordframe
			addrecordframe = tk.Frame(main, bg="gray80", width=1215, height=500, borderwidth=0)
			addrecordframe.grid(row=2, column=1, sticky=tk.NSEW)
			#force width and height on frame
			addrecordframe.grid_propagate(0)

			#add record title
			addrecord_lbl = tk.Label(addrecordframe, fg="gray10", bg="gray80", font=font_16, text="Adding new record ").grid(row=0, column=0, pady=(10,30), padx=(20,0), ipady=4, sticky=tk.W)

			#entry boxes (make global so submit_record() can access)
			global title, first_name, last_name, DOB, address_l1, address_l2, address_l3, postcode, email, telephone
   
			#keep .grid() separate, interferes with. get() for submit_record()
			title = tk.Entry(addrecordframe, width=4)
			title.grid(row=1, column=1, pady=5, padx=5, ipady=2, sticky=tk.W)
			first_name = tk.Entry(addrecordframe, width=30)
			first_name.grid(row=2, column=1, pady=5, padx=5, ipady=2, sticky=tk.W)
			last_name = tk.Entry(addrecordframe, width=30)
			last_name.grid(row=2, column=3, pady=5, padx=5, ipady=2, sticky=tk.W)
			DOB = tk.Entry(addrecordframe, width=10)
			DOB.grid(row=3, column=1, pady=5, padx=5, ipady=2, sticky=tk.W)
			address_l1 = tk.Entry(addrecordframe, width=30)
			address_l1.grid(row=4, column=1, pady=5, padx=5, ipady=2, sticky=tk.W)
			address_l2 = tk.Entry(addrecordframe, width=30)
			address_l2.grid(row=4, column=3, pady=5, padx=5, ipady=2, sticky=tk.W)
			address_l3 = tk.Entry(addrecordframe, width=30)
			address_l3.grid(row=5, column=1, pady=5, padx=5, ipady=2, sticky=tk.W)
			postcode = tk.Entry(addrecordframe, width=30)
			postcode.grid(row=5, column=3, pady=5, padx=5, ipady=2, sticky=tk.W)
			email = tk.Entry(addrecordframe, width=30)
			email.grid(row=7, column=1, pady=5, padx=5, ipady=2, sticky=tk.W)
			telephone = tk.Entry(addrecordframe, width=11)
			telephone.grid(row=7, column=3, pady=5, padx=5, ipady=2, sticky=tk.W)

			#text box labels
			title_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Title *").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
			first_name_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="First Name *").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
			last_name_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Last Name *").grid(row=2, column=2, padx=10, sticky=tk.E)
			DOB_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="DOB").grid(row=3, column=0, padx=10, sticky=tk.E)
			address_l1_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Address Line 1 *").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
			address_l2_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Address Line 2").grid(row=4, column=2, padx=10, pady=5, sticky=tk.E)
			address_l3_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="City").grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
			postcode_label = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Postcode *").grid(row=5, column=2, padx=10, pady=5, sticky=tk.E)
			email_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Email").grid(row=7, column=0, padx=10, pady=5, sticky=tk.E)
			telephone_lbl = tk.Label(addrecordframe, fg="gray30", bg="gray80", font=font_13, text="Phone *").grid(row=7, column=2, padx=10, pady=5, sticky=tk.E)
   
			#advisory label (wrap length / justify attributes given)
			advisory_lbl = tk.Label(addrecordframe, fg="red4", bg="gray80", font=font_13, text="Fields marked with a * are compulsory.", wraplength=150, justify="left").grid(row=8, column=1, padx=10, pady=5, sticky=tk.W)
   
			#Submit entry button
			submit_button = tk.Button(addrecordframe, font=font_14, text="Add Record", command=submit_record, fg="white", bg="black", borderwidth=0).grid(row=9, column=3, pady=(30,0), padx=0, ipadx=5, ipady=5, sticky=tk.SE)
   
		#Delete function for Delete Record button
		def delete():
				response = messagebox.askokcancel("Warning", "You are about to delete this record, this action cannot be undone. Are you sure ?")
				if response:
					selection = my_tree.selection()[0]
					my_tree.delete(selection)
				#connect to database
				conn = sqlite3.connect("demo.db")
				#create cursor
				c = conn.cursor()
				#delete function (search by oid) get input from modify_id entry field
				c.execute("DELETE from customer WHERE oid = " + get_cust_id)
				#Commit and close connection
				conn.commit()
				conn.close()
				#clear text boxes
				cust_id.delete(0, tk.END)
				title.delete(0, tk.END)
				first_name.delete(0, tk.END)
				last_name.delete(0, tk.END)
				DOB.delete(0, tk.END)
				address_l1.delete(0, tk.END)
				address_l2.delete(0, tk.END)
				address_l3.delete(0, tk.END)
				postcode.delete(0, tk.END)
				email.delete(0, tk.END)
				telephone.delete(0, tk.END)
	
		def update():
			#validate data entry first
			if first_name.get() == '':
				messagebox.showerror('Error!', 'First Name cannot be blank.')
			elif last_name.get() == '':
					messagebox.showerror('Error!', 'Last Name cannot be blank.')
			elif address_l1.get() == '':
					messagebox.showerror('Error!', 'Address Line 1 cannot be blank.')
			elif postcode.get() == '':
					messagebox.showerror('Error!', 'Postcode cannot be blank.')
			elif telephone.get() == '':
					messagebox.showerror('Error!', 'Phone cannot be blank.')
			else:
				#get record
				selected = my_tree.focus()
				#update tree
				my_tree.item(selected, text="", values=(cust_id.get(), title.get(), first_name.get(), last_name.get(), DOB.get(), address_l1.get(), address_l2.get(), address_l3.get(), postcode.get(), email.get(), telephone.get(),))
			
				#connect to database
				conn = sqlite3.connect("demo.db")
				#create cursor
				c = conn.cursor()

				#update database
				c.execute(""" UPDATE customer SET
						title = :title,
						first_name = :first_name,
						last_name = :last_name,
						DOB = :DOB,
						address_l1 = :address_l1,
						address_l2 = :address_l2,
						address_l3 = :address_l3,
						postcode = :postcode,
						email = :email,
						telephone = :telephone
					
					WHERE oid = :oid """,
					{
							'title': title.get(),
							'first_name': first_name.get(),
							'last_name': last_name.get(),
							'DOB': DOB.get(),
							'address_l1': address_l1.get(),
							'address_l2': address_l2.get(),
							'address_l3': address_l3.get(),
							'postcode': postcode.get(),
							'email': email.get(),
							'telephone': telephone.get(),
							'oid': cust_id.get()
					}
					)
	
				conn.commit()
				conn.close()
	
				#print update success label
				update_success_lbl = tk.Label(btn_frame, fg="green4", bg="#eee", font=font_13, text="Record Updated", wraplength=150, justify="left").grid(row=0, column=2, padx=10, sticky=tk.W)
   
	
   
		#select record (pass in event for bind)
		def select(event):
			#clear text boxes
			cust_id.delete(0, tk.END)
			title.delete(0, tk.END)
			first_name.delete(0, tk.END)
			last_name.delete(0, tk.END)
			DOB.delete(0, tk.END)
			address_l1.delete(0, tk.END)
			address_l2.delete(0, tk.END)
			address_l3.delete(0, tk.END)
			postcode.delete(0, tk.END)
			email.delete(0, tk.END)
			telephone.delete(0, tk.END)
			
			#get record 
			selected = my_tree.focus()
			#get values
			values = my_tree.item(selected, 'values')
			#output values
			title.insert(0, values[1])
			cust_id.insert(0, values[0])
			first_name.insert(0, values[2])
			last_name.insert(0, values[3])
			DOB.insert(0, values[4])
			address_l1.insert(0, values[5])
			address_l2.insert(0, values[6])
			address_l3.insert(0, values[7])
			postcode.insert(0, values[8])
			email.insert(0, values[9])
			telephone.insert(0, values[10])
   
			#prevent ID from being edited by user
			cust_id.configure(state=tk.DISABLED)

	
		#Display function for SHOW_ALL
		def show_all():
			#destroy any other frames open
			destroy_frames()
   			#handle current tab colour
			handle_current_tab("showall")
			#FRAME for show all
			global showrecordframe
			showrecordframe = tk.Frame(main, bg="gray80", borderwidth=0)
			showrecordframe.grid(row=2, column=1)
			#force width and height on frame
			#showrecordframe.grid_propagate(0)
   
			#show all record title
			showrecord_lbl = tk.Label(showrecordframe, fg="gray10", bg="gray80", font=font_16, text="Showing All Records ").grid(row=0, column=0, ipady=4, sticky=tk.W)
			#style / colours
			style = ttk.Style()
			style.theme_use('default')
			style.configure(
				"Treeview",
				background="gray80",
				foreground="gray10",
				rowheight=25,
				fieldbackground="gray80"
			)

			#highlight selected row
			style.map(
				"Treeview",
				background=[('selected', "#254c6e")]
			)

			#create frame to allow for scrollbar
			tree_frame = tk.Frame(showrecordframe)
			tree_frame.grid(row=1, column=0, sticky=tk.NW)
   
			#create scrollbar
			scroll = tk.Scrollbar(tree_frame)
			scroll.pack(side=tk.RIGHT, fill=tk.Y)

			#Create main treeview
			global my_tree
			my_tree = ttk.Treeview(tree_frame, yscrollcommand=scroll.set, selectmode="extended", height=7)
			my_tree.pack()

			#configure scrollbar
			scroll.config(command=my_tree.yview)

			#define columns
			my_tree['columns'] = ("ID", "Title", "First Name", "Last Name", "DOB", "Address Line 1", "Address Line 2", "City", "Postcode", "Email", "Phone")

			#format columns
			#hide 0th column (ttk default)
			my_tree.column("#0", width=0, stretch=tk.NO)

			my_tree.column("ID", anchor=tk.W, width=5)
			my_tree.column("Title", anchor=tk.W, width=45)
			my_tree.column("First Name", anchor=tk.W, width=110)
			my_tree.column("Last Name", anchor=tk.W, width=150)
			my_tree.column("DOB", anchor=tk.W, width=80)
			my_tree.column("Address Line 1", anchor=tk.W, width=150)
			my_tree.column("Address Line 2", anchor=tk.W, width=150)
			my_tree.column("City", anchor=tk.W, width=120)
			my_tree.column("Postcode", anchor=tk.W, width=90)
			my_tree.column("Email", anchor=tk.W, width=130)
			my_tree.column("Phone", anchor=tk.W, width=95)

			#create headings
			my_tree.heading("#0", text="", anchor=tk.W)
			my_tree.heading("ID", text="ID", anchor=tk.W)
			my_tree.heading("Title", text="Title", anchor=tk.W)
			my_tree.heading("First Name", text="First Name", anchor=tk.W)
			my_tree.heading("Last Name", text="Last Name", anchor=tk.W)
			my_tree.heading("DOB", text="DOB", anchor=tk.W)
			my_tree.heading("Address Line 1", text="Address Line 1", anchor=tk.W)
			my_tree.heading("Address Line 2", text="Address Line 2", anchor=tk.W)
			my_tree.heading("City", text="City", anchor=tk.W)
			my_tree.heading("Postcode", text="Postcode", anchor=tk.W)
			my_tree.heading("Email", text="Email", anchor=tk.W)
			my_tree.heading("Phone", text="Phone", anchor=tk.W)
   
			#striped rows
			my_tree.tag_configure('oddrow', background="gray60")
			my_tree.tag_configure('evenrow', background="gray80")
   
			#connect to database
			conn = sqlite3.connect("demo.db")
			#create cursor
			c = conn.cursor()
			#Show user how many records there are in db
			#run query (select everything)
			c.execute("SELECT rowid, * FROM customer")
			records = c.fetchall()
			recordcount = len(records)

			#add data to tree
			global count 
			global get_cust_id
			count = 0
			for record in records:
				get_cust_id = str(record[0])
				if count % 2  == 0:
					my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=('evenrow',))
				else:
					my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10],), tags=('oddrow',))
				count += 1
				
			#add entry boxes for editing
			data_frame = tk.LabelFrame(showrecordframe, text="Record", bg="gray80")
			data_frame.grid(row=2, column=0, columnspan=4, ipadx=240, sticky=tk.NW)

			#make global so select() can access
			global title, cust_id, first_name, last_name, DOB, address_l1, address_l2, address_l3, postcode, email, telephone
			title = tk.Entry(data_frame, width=4)
			title.grid(row=4, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			cust_id = tk.Entry(data_frame, width=4)
			cust_id.grid(row=4, column=3, pady=5, padx=5, ipady=2, sticky=tk.W)
			first_name = tk.Entry(data_frame, width=30)
			first_name.grid(row=5, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			last_name = tk.Entry(data_frame, width=30)
			last_name.grid(row=5, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)
			DOB = tk.Entry(data_frame, width=10)
			DOB.grid(row=6, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			address_l1 = tk.Entry(data_frame, width=30)
			address_l1.grid(row=7, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			address_l2 = tk.Entry(data_frame, width=30)
			address_l2.grid(row=7, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)
			address_l3 = tk.Entry(data_frame, width=30)
			address_l3.grid(row=8, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			postcode = tk.Entry(data_frame, width=30)
			postcode.grid(row=8, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)
			email = tk.Entry(data_frame, width=30)
			email.grid(row=10, column=2, pady=5, padx=5, ipady=2, sticky=tk.W)
			telephone = tk.Entry(data_frame, width=11)
			telephone.grid(row=10, column=4, pady=5, padx=5, ipady=2, sticky=tk.W)

			#text box labels
			title_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="Title *").grid(row=4, column=1, padx=10, pady=5, sticky=tk.E)
			cust_id_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="ID").grid(row=4, column=2, padx=10, pady=5, sticky=tk.E)
			first_name_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="First Name *").grid(row=5, column=1, padx=10, pady=5, sticky=tk.E)
			last_name_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="Last Name *").grid(row=5, column=3, padx=10, sticky=tk.E)
			DOB_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="DOB").grid(row=6, column=1, padx=10, sticky=tk.E)
			address_l1_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="Address Line 1 *").grid(row=7, column=1, padx=10, pady=5, sticky=tk.E)
			address_l2_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="Address Line 2").grid(row=7, column=3, padx=10, pady=5, sticky=tk.E)
			address_l3_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="City").grid(row=8, column=1, padx=10, pady=5, sticky=tk.E)
			postcode_label = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="Postcode *").grid(row=8, column=3, padx=10, pady=5, sticky=tk.E)
			email_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="Email").grid(row=10, column=1, padx=10, pady=5, sticky=tk.E)
			telephone_lbl = tk.Label(data_frame, fg="gray30", bg="gray80", font=font_13, text="Phone *").grid(row=10, column=3, padx=10, pady=5, sticky=tk.E)
   
			#add buttons
			#make global for update() to print success label 
			global btn_frame
			btn_frame = tk.Frame(showrecordframe, borderwidth=0)
			btn_frame.grid(row=3, column=0, columnspan=4, sticky=tk.NSEW)

			edit_btn = tk.Button(btn_frame, font=font_13, text="Update Record", command=update, fg="white", bg="black", borderwidth=0)
			edit_btn.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=5)

			delete_btn = tk.Button(btn_frame, font=font_13, text="Delete Record", command=delete, fg="white", bg="black", borderwidth=0)
			delete_btn.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=5)

			#bind (left click release)
			my_tree.bind("<ButtonRelease-1>", select)
  
		#FUNCTION FOR CALCULATOR
		def calc():
			#destroy any other frames open
			destroy_frames()
   			#handle current tab colour
			handle_current_tab("calc")
			#FRAME 
			global calcframe
			calcframe = tk.Frame(main, bg="gray80", width=1215, height=500, borderwidth=0)
			calcframe.grid(row=2, column=1, sticky=tk.NSEW)
			#force width and height on frame
			calcframe.grid_propagate(0)
			#Calculator welcome message
			calc_title = tk.Label(calcframe, fg="gray10", bg="gray80", font=font_16, text="Calculator").grid(row=0, column=0, pady=(10,30), padx=(20,0), ipady=4, sticky=tk.W)
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
			btn_1 = tk.Button(calcframe, fg="white", bg="#254c6e", text="1", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(1))
			btn_2 = tk.Button(calcframe, fg="white", bg="#254c6e", text="2", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(2))
			btn_3 = tk.Button(calcframe, fg="white", bg="#254c6e", text="3", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(3))
			btn_4 = tk.Button(calcframe, fg="white", bg="#254c6e", text="4", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(4))
			btn_5 = tk.Button(calcframe, fg="white", bg="#254c6e", text="5", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(5))
			btn_6 = tk.Button(calcframe, fg="white", bg="#254c6e", text="6", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(6))
			btn_7 = tk.Button(calcframe, fg="white", bg="#254c6e", text="7", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(7))
			btn_8 = tk.Button(calcframe, fg="white", bg="#254c6e", text="8", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(8))
			btn_9 = tk.Button(calcframe, fg="white", bg="#254c6e", text="9", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(9))
			btn_0 = tk.Button(calcframe, fg="white", bg="#254c6e", text="0", padx=40, font=font_16, borderwidth=1, command=lambda: btn_click(0))
			btn_dot = tk.Button(calcframe, fg="white", bg="#254c6e", text=".", padx=43, font=font_16, borderwidth=1, command=lambda: btn_click('.'))
			#CREATE OPERATOR BUTTONS (WITH OWN FUNCTIONS)
			btn_add = tk.Button(calcframe, fg="white", bg="#254c6e", text="+", padx=40, font=font_16, command=btn_add, borderwidth=1)
			btn_sub = tk.Button(calcframe, fg="white", bg="#254c6e", text="-", padx=42, font=font_16, command=btn_sub, borderwidth=1)
			btn_mul = tk.Button(calcframe, fg="white", bg="#254c6e", text="*", padx=41, font=font_16, command=btn_mul, borderwidth=1)
			btn_div = tk.Button(calcframe, fg="white", bg="#254c6e", text="/", padx=41, font=font_16, command=btn_div, borderwidth=1)
			btn_equal = tk.Button(calcframe, fg="white", bg="#254c6e", text="=", padx=93, font=font_16, command=btn_equal, borderwidth=1)
			btn_clear = tk.Button(calcframe, fg="white", bg="#254c6e", text="AC", padx=34, font=font_16, command=btn_clear, borderwidth=1)
			btn_save = tk.Button(calcframe, fg="white", bg="#254c6e", text="SAVE", padx=10, font=font_16, command=btn_save, borderwidth=1)	

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
   
   
		#function to handle destruction of frames
		def destroy_frames():
				try:
					addrecordframe.destroy()
				except (NameError):
					print("addrecordframe does not exist, nothing to destroy")
				try:
					showrecordframe.destroy()
				except (NameError):
					print("showrecordframe does not exist, nothing to destroy")
				try:
					calcframe.destroy()
				except (NameError):
					print("calcframe does not exist, nothing to destroy")
				try:
					searchresultsframe.destroy()
				except (NameError):
					print("searchresultsframe does not exist, nothing to destroy")

		#function to handle current selected nav item
		def handle_current_tab(tab):
			if tab == "addrecord":
				add_button['bg'] = "#254c6e"
				show_all_button['bg'] = "#366f9e"
				calc_button['bg'] = "#366f9e"
				quit_button['bg'] = "#366f9e"
			elif tab == "showall":
				add_button['bg'] = "#366f9e"
				show_all_button['bg'] = "#254c6e"
				calc_button['bg'] = "#366f9e"
				quit_button['bg'] = "#366f9e"
			elif tab == "calc":
				add_button['bg'] = "#366f9e"
				show_all_button['bg'] = "#366f9e"
				calc_button['bg'] = "#254c6e"
				quit_button['bg'] = "#366f9e"
			else:
				add_button['bg'] = "#366f9e"
				show_all_button['bg'] = "#366f9e"
				calc_button['bg'] = "#366f9e"
				quit_button['bg'] = "#254c6e"
			
				
   			
	
		#QUIT
		def quit():
			log_out = messagebox.askyesno("Log Out", "You are about to log out, are you sure ?")
			if log_out == 1:
				main.destroy()
				login.correct_label.destroy()
  
		#--- LOGOFRAME ---#
		#Define logoframe size/position
		logoframe = tk.Frame(main, bg="#eee", width=1366, height=125, borderwidth=0)
		logoframe.grid(row=0, column=0, columnspan=5, ipadx=25, sticky=tk.N)
		#force width and height on frame
		logoframe.grid_propagate(0)
		#Define logo image and grid position (using self to stop auto garbage collection)
		self.logo = tk.PhotoImage(file = "wel.png")
		logo_label = tk.Label(logoframe, image=self.logo,  borderwidth=0, highlightthickness=0)
		logo_label.grid(row=0, column=0)
  
		#--- SEARCHFRAME ---#
		#Define searchframe size/position
		searchframe = tk.Frame(main, bg="gray30", width=1366, height=100, borderwidth=0)
		searchframe.grid(row=1, column=0, ipadx=25, columnspan=5, sticky=tk.N)
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
		buttonframe = tk.Frame(main, bg="#6492b6", borderwidth=0)
		buttonframe.grid(row=2, column=0, ipady=170, sticky=tk.NW)

  
		#--- MENU BUTTONS ---#
		#Add button - calls add_record() / submit_record()
		#global for handle_current_tab()
		global add_button, show_all_button, calc_button
		add_button = tk.Button(buttonframe, font=font_13, text="Add Record", command=add_record,  fg="white", bg="#366f9e", borderwidth=0)
		add_button.grid(row=3, column=0, ipadx=56, ipady=10, sticky=tk.W)
  
		#Show all records button = calls show_all()
		show_all_button = tk.Button(buttonframe, font=font_13, text="Show All Records", command=show_all, fg="white", bg="#366f9e", borderwidth=0)
		show_all_button.grid(row=4, column=0, ipadx=36, ipady=10, sticky=tk.W)
  
		#calculator button
		calc_button = tk.Button(buttonframe, font=font_13, text="Calculator", command=calc,  fg="white", bg="#366f9e", borderwidth=0)
		calc_button.grid(row=6, column=0, ipadx=61, ipady=10, sticky=tk.W)
  
		#Quit button - calls DEF QUIT
		quit_button = tk.Button(buttonframe, font=font_13, text="Quit", command=quit,  fg="white", bg="#366f9e", borderwidth=0)
		quit_button.grid(row=8, column=0, ipadx=81, ipady=10, sticky=tk.W)
  
  
  
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
	root.geometry("1366x768")
	root.configure(background ="gray80") 
	root.iconbitmap("systemicon.ico") 
	root.resizable(False, False)
	
	tk.mainloop()
	
#run main if being run as standalone
if __name__ == '__main__':
	main()