import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__, instance_relative_config=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "db.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


@app.route("/<name>", methods=['GET', 'POST'])
def start_page(name):
    if request.method == 'POST':
        new_message = Message(
            user = name,
            content = request.form['content']
        )
        db.session.add(new_message)
        db.session.commit()

    messages = Message.query.order_by(Message.created_at).all()
    return render_template('index.html', messages=messages)
    


if __name__ == "__main__":
    app.run(debug=True)