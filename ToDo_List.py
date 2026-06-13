from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import psycopg2

# Initialize the Flask application
app = Flask(__name__) # configure the SQLite database, relative to the app instance folder 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Loveson.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)



class Loveson(db.Model):
    Sn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
	return f'{self.Sn} - {self.title}'
	

with app.app_context():
    db.create_all()
# Define the homepage route

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
    	title = request.form['title']
    	desc = request.form['desc']
    	todo = Loveson(title=title, desc=desc)
    	db.session.add(todo)
    	db.session.commit()
    all_todo = Loveson.query.all()
    return render_template('index.html', all_todo=all_todo)
 
    

@app.route('/show')
def product():
	all_todo = Loveson.query.all()
	print(all_todo)
	return 'This shows ToDo list'
	
@app.route('/update/<int:Sn>', methods=['GET', 'POST'])
def update(Sn):
	 
	if request.method == 'POST':
	       title = request.form['title']
	       desc = request.form['desc']
	       todo = Loveson.query.filter_by(Sn=Sn).first()
	       todo.title = title
	       todo.desc = desc
	       db.session.add(todo)
	       db.session.commit()
	       return redirect('/')
		
	todo = Loveson.query.filter_by(Sn=Sn).first()

	return render_template('update.html', todo=todo)
	
@app.route('/delete/<int:Sn>')
def delete(Sn):
	todo = Loveson.query.filter_by(Sn=Sn).first()
	db.session.delete(todo)
	db.session.commit()
	return redirect('/')


if __name__ == '__main__':

    with app.app_context():
    	db.create_all()
   
    app.run(debug=True)
