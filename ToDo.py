import os
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Helpers import check_birthdays, add_event, add_task, get_time_remaining, send_email, ticktock
#from Gsheets import rows_to_print
import openpyxl
from datetime import datetime as dt, timedelta
from uuid import uuid4 
from flask import Flask, render_template, request, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import func,extract #datetime functions imported from the sqlAlchemy library
from flask_migrate import Migrate  
from Helpers import check_birthdays,add_event,add_task,get_time_remaining,send_email, ticktock



import openpyxl 
from datetime import datetime as dt,timedelta
import time 
from uuid import uuid4 #for creation of unique id's 

#importing libraries for email 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

# Get today's date
today = dt.now()
today_day_month = today.strftime('%d-%m')  #string object 
today_day_month_dt = dt.strptime(today_day_month,'%d-%m') #datetime object
today_day_month_year = today.strftime('%d/%m/%Y') 
current_day = today.timetuple().tm_yday #integer 



app = Flask(__name__, template_folder='templates')  
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
#'postgresql://planner_m18s_user:ozFLdJsW2P4NxSoQv3EluDsm6ZY8yinu@dpg-co9u8vdjm4es73b5ta00-a.singapore-postgres.render.com/planner_m18s'
#'sqlite:///site.db'

#creating a database object
db = SQLAlchemy(app) 

#creating a migrate object ---To  
migrate=Migrate(app,db) 




#openpyxl code 
 

#parsing quotes txt file 
file1_path = r"Quotes\glittery_quotes.txt" 
file2_path = r"Quotes\motivation_quotes.txt" 
file3_path=r"Quotes\deepWork.txt"
 
@ticktock
def  check_and_send_emails(now, subject,task_body):
    # Check if it's 9 o'clock
    if (now.hour == 8 or now.hour == 14 or now.hour == 19) and now.minute == 0:
    # Example task details 
        print(f"sending an email at {now.hour}......")


        recipient_email = 'onmailharshit@gmail.com'  # Update with recipient's email address

    # Send email notification
        send_email(subject, task_body, recipient_email)










def quotes(curr_day, path1, path2, path3):
    with open(path1, 'r') as file1, open(path2, 'r') as file2,open(path3,'r') as file3:
        gQuotes = file1.readlines()
        mQuotes = file2.readlines()  
        deepWork = file3.readlines()
        index_g = (curr_day % len(gQuotes))
        index_m = (curr_day % len(mQuotes))  
        index_d = (curr_day % len(deepWork))
        return gQuotes[index_g].strip(), mQuotes[index_m].strip(), deepWork[index_d].strip() 
def fileWriter(path1, path2, path3, gQuote, mQuote, dQuote): 
    with open(path1, 'a') as file1, open(path2, 'a') as file2, open(path3, 'a') as file3:  
        if gQuote:  # Check if gQuote is not empty
            file1.write(f"-{gQuote}\n")
        if mQuote:  # Check if mQuote is not empty
            file2.write(f"-{mQuote}\n")
        if dQuote:  # Check if dQuote is not empty
            file3.write(f"-{dQuote}\n")

        

         

        # Read and process the contents of file2
        

#defining database classes Events,Task and Deadline
class Event(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    event = db.Column(db.String(50), unique=False, nullable=False)  # Define the 'event' column
    summary = db.Column(db.String(120))
    start_time = db.Column(db.DateTime)  # Store datetime object for start time
    end_time = db.Column(db.DateTime)  # Store datetime object for end time
    done = db.Column(db.Boolean, default=False)  # Default value for boolean column

    def __repr__(self):
        return f'Event({self.event})'


class Task(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    task = db.Column(db.String(50), unique=False, nullable=False)
    summary = db.Column(db.String(120))
    start_hour = db.Column(db.Integer)  # Store datetime object for start time
    end_hour = db.Column(db.Integer)  # Store datetime object for end time
    done = db.Column(db.Boolean, default=False)  # Default value for boolean column
    
    def __repr__(self):
        return f'Task ({self.task})' 

class Deadline(db.Model):
    __tablename__ = 'deadline'

    id = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime) 
    done = db.Column(db.Boolean, default=False)
    

    def __repr__(self):
        return f'Deadline({self.description})' 
#==================================================================================================================================================
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Person = db.Column(db.String(100), nullable=False)
    FirstName = db.Column(db.String(100), nullable=False)
    LastName = db.Column(db.String(100), nullable=False)
    Bday = db.Column(db.String(100))
    Contact = db.Column(db.String(100))
    Group = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True,)
    Location = db.Column(db.String(100))
    Position = db.Column(db.String(100))
    Company = db.Column(db.String(100))
    Insta_Facebook = db.Column(db.String(100))
    LastContact = db.Column(db.String(100))
    Last_Update = db.Column(db.String(100))

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
 
 




 #**Data Storage
# list(list of dictionaries)
#wehre data is stored
events= []
deadlines=[]
tasks=[]
periodic_tasks=[]
task_ct_set=set()
event_ct_set=set()

 





#**Route Functions** 
#_________________________________________________________________________________________________________________________________________________
#INDEX FUNCTION 
@app.route('/index')
@app.route('/home')
@app.route('/')

def index():   

    global ct  
    global today    
   

    current_day_of_week = str(today.strftime('%A'))  
   
    print(current_day_of_week)
    #global rows_to_print
    current_day = today.timetuple().tm_yday 
    
    # time remaining
    time_remaining = get_time_remaining() 
    # checking for birthdays 
   
    #getting quotes 
    gQuote, mQuote,dQuote= quotes(current_day, file1_path, file2_path, file3_path)

    # eventList,#Task List & Deadline List
    event_list = Event.query.all()  # Query all events from the database 
    task_list = Task.query.all()
    deadline_list = Deadline.query.all() 
    rows_to_print = Person.query.filter(extract('day', Person.Bday) == today_day_month_dt.day, 
                                    extract('month', Person.Bday) == today_day_month_dt.month).all()
    print(rows_to_print)
    

    # counting the number of events,tasks done yet
    for todo in event_list:  # Iterate over the queried events
        if todo.done: 
            event_ct_set.add(todo.id)  # Assuming 'done' is a boolean attribute of Event 
    for task in task_list:
        if task.done:
            task_ct_set.add(task.id) 
    #calculatiing the due_in ,overdue a
    
   
    return render_template('index.html', events=event_list, task_ct=len(task_ct_set), event_ct=len(event_ct_set), rows_to_print=rows_to_print, time_remaining=time_remaining, tasks=task_list,deadlines=deadline_list,today_date_string = today_day_month_year,today_date_datetime=today,gQuote=gQuote, mQuote=mQuote,dQuote=dQuote,current_day_of_week = current_day_of_week)


#-------------------------------------------------------------------------------------------------------- 
#function to add quotes
@app.route('/addQuote',methods=['POST'])
def addQuote(): 
    # Access form data using request.form
    w_gQuote = request.form.get('gQuote')  # Use .get() to handle empty input # the input is stored in the form of key-value pairs
    w_mQuote = request.form.get('mQuote')  # Use .get() to handle empty input
    w_dQuote = request.form.get('dQuote')  # Use .get() to handle empty input
    
    global file1_path, file2_path, file3_path 
    fileWriter(file1_path, file2_path, file3_path, w_gQuote, w_mQuote, w_dQuote) 
    return redirect(url_for('index')) 

#add function adds an event
@app.route('/add', methods=['POST'])
def add():
    todo = request.form['todo']
    summary = request.form['Summary']  # Capture the Summary field
    start_date_str = request.form['start_time']  # datetime object
    end_date_str = request.form['end_time']  # datetime object 

    start_date = dt.strptime(start_date_str, '%Y-%m-%dT%H:%M') if start_date_str else None
    end_date = dt.strptime(end_date_str, '%Y-%m-%dT%H:%M') if end_date_str else None

    event_id = str(uuid4())
    event = Event(id=event_id, event=todo, summary=summary, start_time=start_date, end_time=end_date)
    db.session.add(event)
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('index'))



#adding tasks
@app.route('/add_task', methods=['POST']) 
def add_task_route(): 
    task_id = str(uuid4())
    task = Task(
        id=task_id,
        task=request.form["task"],
        summary=request.form['task_summary'],
        start_hour=request.form['min_hour'],
        end_hour=request.form['max_hour']
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index')) 

#Adding deadlines
@app.route('/add_deadline', methods=['POST'])
def add_deadline(): 
    global today 
    
    deadline_id = str(uuid4())
    description = request.form['description']
    deadline_date_str = request.form['deadline']  # string object has to be converted to datetime object
    deadline_date = dt.strptime(deadline_date_str, '%Y-%m-%dT%H:%M') if deadline_date_str else None   
    
    # Calculate the difference between today and the deadline 
    
     

    # Extract days, hours, and minutes from the time difference
     


    deadline_id = str(uuid4())
     
    db.session.add(Deadline(id=deadline_id, description=description, deadline=deadline_date ))
    db.session.commit()
    return redirect(url_for('index'))



#-----------------------------------------------------------------------    

# Editing events
@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    event = Event.query.get_or_404(id)
    if request.method == 'POST':
        event.event = request.form['todo']
        event.summary = request.form['Summary']
        event.start_time = request.form['start_time']
        event.end_time = request.form['end_time']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', event=event, id=id)

# Editing tasks
@app.route('/edit_task/<string:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.task = request.form['task']
        task.summary = request.form['task_summary']
        task.start_hour = request.form['min_hour']
        task.end_hour = request.form['max_hour']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task, id=id) 

# Editing deadlines
@app.route('/edit_deadline/<string:id>', methods=['GET', 'POST'])
def edit_deadline(id):
    deadline = Deadline.query.get_or_404(id) #deadline object
    if request.method == 'POST':
        deadline.deadline = request.form['deadline']
        deadline.summary = request.form['Summary']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_deadline.html', deadline=deadline, id=id)


#----------------------------------------------------------------------------------
# Checking (marking as done) an event
@app.route('/check/<string:id>')
def check(id):
    event = Event.query.get_or_404(id)
    event.done = not event.done
    db.session.commit()
    return redirect(url_for('index'))

# Checking (marking as done) a task
@app.route('/check_task/<string:id>')
def check_task(id):
    task = Task.query.get_or_404(id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('index')) 

# Checking (marking as done) a deadline
@app.route('/check_deadline/<string:id>')
def check_deadline(id):
    deadline = Deadline.query.get_or_404(id)
    deadline.done = not deadline.done
    db.session.commit()
    return redirect(url_for('index'))

#----------------------------------------------------------------------------------------------------
# Deleting an event
@app.route('/delete/<string:id>')
def delete(id):
    event = Event.query.get_or_404(id) 
    event_ct_set.discard(event.id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))

# Deleting a task
@app.route('/delete_task/<string:id>')
def delete_task(id):
    task = Task.query.get_or_404(id) 
    task_ct_set.discard(task.id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index')) 

# Deleting a deadline
@app.route('/delete_deadline/<string:id>')
def delete_deadline(id):
    deadline = Deadline.query.get_or_404(id)
    db.session.delete(deadline)
    db.session.commit()
    return redirect(url_for('index'))


#---------------------------------------------------------------------------------------------------

#Updating an event
@app.route('/update', methods=['POST'])
def update_todo():
    todo_id = request.form.get('todo_id')
    done = request.form.get('done')
    # Query the Event with the given ID
    todo = Event.query.get(todo_id)
    if todo:
        # Update the 'done' attribute of the Event
        todo.done = bool(done)
        db.session.commit()  # Commit the changes to the database
    return redirect(url_for('index')) 

@app.route('/update_task', methods=['POST'])
def update_task():
    task_id = request.form.get('task_id')
    done = request.form.get('done')
    # Query the Task with the given ID
    task = Task.query.get(task_id)
    if task:
        # Update the 'done' attribute of the Task
        task.done = bool(done)
        db.session.commit()  # Commit the changes to the database
    return redirect(url_for('index')) 

# Updating a deadline
@app.route('/update_deadline', methods=['POST'])
def update_deadline():
    deadline_id = request.form.get('deadline_id')
    done = request.form.get('done')
    # Query the Deadline with the given ID
    deadline = Deadline.query.get(deadline_id)
    if deadline:
        # Update the 'done' attribute of the Deadline
        deadline.done = bool(done)
        db.session.commit()
    return redirect(url_for('index'))

#defining the same stuff for deadlines  


#=======================================================================================================================================================================
#for my network 
@app.route('/network') 
@app.route('/Network') 
def display_network(): 
    unfiltered_persons = Person.query.all()   
    groups = Group.query.all()  
    print(groups)

    persons_by_groups =  defaultdict(list) # Initialize empty lists for each group
    for group in groups:
        group_name = group.name.strip().rstrip('>').lstrip('<')  # Remove leading '<' and trailing '>'
        persons_by_groups[group_name] = Person.query.filter_by(Group=group.name).all()
 
        #persons_by_groups[person.Group].append(person)
    
    #print(unfiltered_persons, groups, persons_by_groups)
    return render_template('Network.html', unfiltered_persons=unfiltered_persons, groups=groups, persons_by_groups=persons_by_groups)


@app.route('/add_person', methods=['POST'])
def add_person():
    data = request.form
    # Check if the email already exists
    existing_person = Person.query.filter_by(email=data['email']).first()
    if existing_person:
        print('Email already exists!', 'error')
        return redirect(url_for('display_network'))
    
    # Handle empty 'Bday' field
    bday = data['birthday'] if data['birthday'] else None
    new_person = Person(
        Person=data['person_name'],
        FirstName=data['first_name'],
        LastName=data['last_name'],
        Bday=bday,
        Contact=data['contact'],
        Group=data['group'],
        email=data['email'],
        Location=data['location'],
        Position=data['position'],
        Company=data['company'],
        Insta_Facebook=data['insta_facebook'],
        LastContact=data['LastContact'],
        Last_Update=data['last_update']
    )
    db.session.add(new_person)
    db.session.commit() 
    print('Person added successfully!', 'success')
    return redirect(url_for('display_network'))

@app.route('/edit_person/<string:id_person>', methods=['GET', 'POST'])


@app.route('/edit_person/<string:id_person>', methods=['GET', 'POST'])
def edit_person(id_person):
    person = Person.query.get_or_404(id_person)
 
    # Your edit_person route logic here

    
    if request.method == 'POST':
        data = request.form
        person.Person = data['person_name']
        person.FirstName = data['first_name']
        person.LastName = data['last_name']
        
        # Parse and format the birthday date
        if data['birthday']:
            try:
                birthday = dt.strptime(data['birthday'], '%Y-%m-%d')
                person.Bday = birthday.strftime('%Y-%m-%d')
            except ValueError:
                # Handle invalid date format
                print('Invalid date format for birthday. Please use YYYY-MM-DD format.', 'danger')
                return redirect(url_for('edit_person', id_person=id_person))
        else:
            person.Bday = None  # Set to None if no date provided
        
        person.Contact = data['contact']
        person.Group = data['group']
        person.email = data['email']
        person.Location = data['location']
        person.Position = data['position']
        person.Company = data['company']
        person.Insta_Facebook = data['insta_facebook']
        person.LastContact = data['LastContact']
        person.Last_Update = data['last_update']
        
        db.session.commit() 
        flash('Person details updated successfully.', 'success')
        return redirect(url_for('display_network')) 
    return render_template('edit_person.html', person=person)



@app.route('/delete_person/<string:id>', methods=['POST']) 
def delete_person(id):
    person = Person.query.get_or_404(id) 
    db.session.delete(person)
    db.session.commit() 
    return redirect(url_for('display_network')) 

@app.route('/add_group', methods=['POST']) 
def add_group():
    group_name = request.form['group_name']  # Extract group_name from form data
    new_group = Group(name=group_name)  
    db.session.add(new_group)  
    db.session.commit() 
    print("Successfully added group")
    return redirect(url_for('display_network')) 

@app.route('/edit_group/<string:id>', methods=['GET', 'POST'])
def edit_group(id):
    group = Group.query.get_or_404(id)
    
    if request.method == 'POST':
        # Check if 'group_name' is in the form data
        if 'group_name' in request.form:
            group.name = request.form['group_name']
            db.session.commit()
            return redirect(url_for('display_network'))
        else:
            print('Request not valid')
            return redirect(url_for('edit_group', id=id))
    
    return render_template('edit_group.html', group=group)


@app.route('/delete_group/<string:id>', methods=['POST'])  
def delete_group(id):
    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('display_network'))


    



if __name__ == '__main__':
    with app.app_context(): 
        
        db.create_all()
        db.session.commit()

        event_list = Event.query.all()
        task_list = Task.query.all()
        deadline_list = Deadline.query.all()

        subject = 'Daily Task Reminder'
        task_body = f'''
            You have tasks to complete today                       
            Your Events: {" ".join(f"{event.event} summary: {event.summary}" for event in event_list)}
            Tasks: {" ".join(f"{task.task} summary: {task.summary}" for task in task_list)}
            Deadlines: {" ".join(f"{deadline.description}" for deadline in deadline_list)}
        '''
        check_and_send_emails(today, subject, task_body)



