from logging import debug
from flask import Flask, redirect,render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask_moment import Moment


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db  = SQLAlchemy(app)
# Moment(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/index.html', methods=['GET', 'POST'])
@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Unable to create'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks= tasks )


@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Nothing to delete'
        

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST': 
        task.content = request.form['content']

        try:
            db.session.commit()
        except:
            return 'Error updating'
    
    else:
        return render_template('update.html', task =task)



@app.route('/complete/<int:id>')
def complete(id):
    task = Todo.query.get_or_404(id)
    if task.completed==0:
        task.completed = int(1)
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template('/index.html', tasks=task)


@app.route('/done',methods = ['GET'])
def done():
    task = Todo.query.order_by(Todo.completed)
    return render_template('/done.html', tasks = task)


if __name__== '__main__':
    app.run(debug=True)



