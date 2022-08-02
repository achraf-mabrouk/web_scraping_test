from flask import *

# loading data from json file

with open("Hotel_burj_arab.json", 'r', encoding='utf-8') as f:
    dataset = json.load(f)


def filter_by_date(comments: list, date: str) -> list:
    filtered_comments = []
    for i in range(len(comments)):
        if comments[i]["Date commentaire"] == date:
            filtered_comments.append(comments[i])
    return filtered_comments


def filter_by_date_sejour(comments: list, date_sejour: str) -> list:
    filtered_comments = []
    for i in range(len(comments)):
        if comments[i]["date de sejour"] == date_sejour:
            filtered_comments.append(comments[i])
    return filtered_comments


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# home
@app.route('/', methods=['GET'])
def index():
    return jsonify(dataset)


@app.route('/comments', methods=['GET'])
def get_comments():
    comments = dataset['comments']
    args = request.args
    date_comment = args.get('date_comment')
    date_sejour = args.get('date_sejour')
    nb_contributions = args.get('nb_contributions')

    if date_comment != None:
        user_query = str(date_comment)  # /comments?date_comment=DATE 
        return jsonify(filter_by_date(comments, user_query))

    elif date_sejour != None:
        user_query = str(date_sejour) # /comments?date_sejour=DATE_SEJOUR
        filtered_comments = filter_by_date_sejour(comments, user_query)
        return jsonify(filtered_comments)

    elif nb_contributions != None: # comments?nb_contributions=NB_contrib
        
        nb_contributions = str(nb_contributions)
        if nb_contributions[0] == "<":
           result = [ comment for comment in comments if int(comment['nb contributions']) < int(nb_contributions[1:])]
        elif nb_contributions[0] == ">":
            result = [ comment for comment in comments if int(comment['nb contributions']) > int(nb_contributions[1:])]
        return jsonify(result)   
    else:
        return jsonify(comments)



if __name__ == '__main__':
    app.run(port=7777, debug=True)
