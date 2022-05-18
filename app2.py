from flask import Flask

app = Flask(__name__)
@app.route("/")
def index():
    return "Anasayfa"
@app.route("/search")
def search():
    return "Search Page"
@app.route("/delete/item")
def delete():
    return "Delete Item"
@app.route("/delete/<string:id>")
def deleteID(id):
    return "Id: " + id

if __name__ == "__main__":
    app.run(debug= True)