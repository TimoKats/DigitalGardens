import json, os
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def corrected_similarity(sentence_1, sentence_2, sensitivity=0.4):
    embedding_1 = model.encode(sentence_1)
    embedding_2 = model.encode(sentence_2)
    return util.cos_sim(embedding_1, embedding_2).item() - sensitivity

class Data:
    def __init__(self):
        self.current_instance = {}

    def create_file(self, title, description, content):
        data_json = {}
        data_json["title"] = title
        data_json["description"] = description
        data_json["content"] = content
        data_json["comments"] = {}
        with open("data/" + title + ".json", "w+") as outfile:
            json.dump(data_json, outfile, indent=4)

    def load(self, name):
        self.filename = name
        with open("data/" + name) as infile:
            self.current_instance = json.load(infile)

    def get_instancies(self):
        return os.listdir("data/")

    def add_comment(self, selected_text, comment):
        self.current_instance["comments"][selected_text] = [comment, corrected_similarity(selected_text, comment)]

    def write(self):
        with open("data/" + self.filename, "w+") as outfile:
            json.dump(self.current_instance, outfile, indent=4)

