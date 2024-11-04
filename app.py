from flask import Flask, render_template, url_for, request, redirect #import flask class from flask module
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #create an instance of flask class
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'# tells the app where db is located
db = SQLAlchemy(app) #initialise the DB

class Todo(db.Model): 
    #Defining DB model
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow) 

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods = ['POST','GET']) #defines route or URL path where function will be triggered

def index():
    if request.method =='POST': #if the function is post
        taskContent = request.form['content'] #fetching content from form
        newTask = Todo(content=taskContent) #creating a DB model for task content
        try:
            db.session.add(newTask) #add the model to DB
            db.session.commit() #commit the session
            return redirect('/')
        except:
            return "Issue adding task."
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # Querying the DB for all tasks in the order in which they were created
        return render_template('index.html', tasks=tasks) # used to redirect flow to index.html

#setting up a new route for delete functionality
@app.route('/delete/<int:id>') #id is the unique identifier for each row
def delete(id):
    taskToDelete = Todo.query.get_or_404(id) #querying db model(i.e.Todo) for task to delete
    try:
        db.session.delete(taskToDelete) #delete the task
        db.session.commit()
        return redirect('/') # used to redirect flow to index
    except:
        return "Error occured"

@app.route('/update/<int:id>', methods=['GET', 'POST']) #why are methods needed here ?
def update(id):
    task = Todo.query.get_or_404(id) #get the task from id
    if request.method == 'POST': #called when update button is clicked after updating from update.html
        task.content = request.form['content'] #we are setting content of task row in db
        try:
            db.session.commit() #only updating cos we have already set the content in db
            return redirect("/")
        except:
            return 'Error Occured updating task'
    else:
        return render_template('update.html', task=task) #show the update.html page (called when you click on update button for a task in the index.html)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True) #enables debug mode i.e. in case error show them