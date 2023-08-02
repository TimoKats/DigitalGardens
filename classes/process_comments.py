from flask import Markup

def map_score(score):
    heatmap = [
        (-1,    '#e93e3a'),
        (-0.5,  '#ed683c'),
        (-0.2, '#f3903f'),
        (-0.1,  '#fdc70c'),
        (0,     '#36454f'),
        (0.1,   '#65cc56'),
        (0.2,  '#41bf2e'),
        (0.5,   '#1c8f0a'),
        (1,     '#107800')
    ]
    for index, item in enumerate(heatmap):
        color = item[1]
        if item[0] >= score:
            return color
    return color

def get_scores(data):
    characters = [*data["content"]]
    scores = [0] * len(characters)
    for text, comment in data["comments"].items():
        start = data["content"].find(text)
        end = start + len(text)
        for index, score in enumerate(scores):
            if index >= start and index < end:
                scores[index] += float(comment[1])
    return scores

def color_content(data):
    content = ""
    scores = get_scores(data)
    characters = [*data["content"]]
    for score, character in zip(scores,characters):
        content += "<span style=color:" + map_score(score) + ">" + character + "</span>"
    return Markup(content)
