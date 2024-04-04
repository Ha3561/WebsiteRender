from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

from flask_script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()


'''
# Define your database model here
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)  # Boolean column for task completion status
    expected_start_time = db.Column(db.DateTime, nullable=False)
    expected_end_time = db.Column(db.DateTime, nullable=False)

# Create database tables outside of main code block  
try:
    with app.app_context():
        db.create_all() 
        new_task = Task(task_name='Work', complete=False) 


                    
        db.session.add(new_task)
        db.session.commit()
except Exception as f:
    print (f"An Exception occureed {f}") 

 
    row_indices = check_birthdays(wb, sheet, max_row) 
    rows_to_print = list()
    for row_index in row_indices:
        row_values = sheet[row_index]  # accesses the row data as an object 
        row_data = [cell.value for cell in row_values]  # there is nothing called row.value 
        print(row_data)
        rows_to_print.append(row_data)    
  




'''