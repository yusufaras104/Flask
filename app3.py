from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from app import Hex_Noces as Noce, data
import requests
import pyshorteners
from hashlib import sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yuzarsif/Desktop/software-engineer-task-master/app/demo/app/links.db'
db = SQLAlchemy(app)
@app.route("/")
def homepage():
    links = Links.query.all()
    """
    [
        {
            "id":1, 
            "link":"example.com", 
            "short_link":"bit.ly/example | tinyurl.com/exapmle", 
            "gen_token":"0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7"
        }
    ]
    """

    return render_template("index.html", Links_option=[{'Links': 'Bitly'}, {'Links': 'Tinyurl'}], links = links)


@app.route("/add", methods=['POST'])
def addLink():
    Link_Option = request.form.get("Links_option")
    Link = request.form.get("input_link")
    
    #Generate Shorter link
    if Link_Option == 'Bitly':
        s = pyshorteners.Shortener(api_key='99b778a91b033bb2557f85a50dc245e99ea94798')
        Link_shorter = s.bitly.short(Link)

    else:
        res = requests.get('https://tinyurl.com/api-create.php?url=' + Link)
        Link_shorter = res.text

    newLink = Links(link = Link, short_link = str(Link_shorter), gen_token = False)

    db.session.add(newLink)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/create_token/<string:id>")
def createToken(id):
    link = Links.query.filter_by(id=id).first()
    if (link.gen_token == False):
        new_token = Noce.mine(id, data, '0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7', id)
    else:
        pass
    
    newLink = Links(gen_token = new_token)

    db.session.add(newLink)
    db.session.commit()
    return redirect(url_for("index"))

    db.session.commit()
    return redirect(url_for("index"))

class Links(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    link = db.Column(db.String(80))
    short_link = db.Column(db.Text)
    gen_token = db.Column(db.Boolean)

if __name__ == "__main__":
    app.run(debug=True)