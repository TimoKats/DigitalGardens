# packages
from flask import Flask, render_template, request
# classes
from classes.data import Data
from classes.process_comments import *

#other
app = Flask(__name__)
data = Data()

@app.route("/")
def home():
    titles, descriptions = [], []
    for instance in data.get_instancies():
        data.load(instance)
        titles.append(data.current_instance["title"])
        descriptions.append(data.current_instance["description"])
    return render_template("index.html", len=len(data.get_instancies()),
                           titles=titles,
                           descriptions=descriptions)

@app.route("/manual/")
def manual():
    return render_template("manual.html")

@app.route("/plant/", methods=["POST", "GET"])
def plant():
    if request.method == "POST":
        form_data = request.form
        name = form_data["name"]
        description = form_data["description"]
        content = form_data["content"]
        data.create_file(name, description, content)
    return render_template("plant.html")

@app.route("/seed/<name>", methods=["POST","GET"])
def seed(name):
    data.load(name + ".json")
    if request.method == "POST":
        form_data = request.form
        selected_text = form_data["selected_text"]
        comment = form_data["submitted_text"]
        data.add_comment(selected_text, comment)
        data.write()
    return render_template("seed.html", title=data.current_instance["title"],
                           description=data.current_instance["description"],
                           content=color_content(data.current_instance))

@app.route("/log/<name>", methods=["POST","GET"])
def log(name):
    texts, scores, comments = [], [], []
    data.load(name + ".json")
    for text, comment in data.current_instance["comments"].items():
        texts.append(text)
        comments.append(comment[0])
        scores.append(comment[1])
    return render_template("log.html", texts=texts,
                           comments=comments,
                           scores=scores,
                           len=len(comments),
                           title=name)

if __name__ == "__main__":
    app.run(debug=True)

