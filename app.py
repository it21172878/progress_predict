# from flask import Flask, render_template,request, redirect
# from helper import preprocessing, vectorizer, get_prediction
# from logger import logging

# app = Flask(__name__)

# logging.info('Flask server started')

# data = dict()
# reviews = []
# positive = 0
# negative = 0

# @app.route("/")
# def index():
#     data['reviews'] = reviews
#     data['positive'] = positive
#     data['negative'] = negative

#     logging.info('========== Open home page ============')

#     return render_template('index.html', data=data)

# @app.route("/", methods = ['post'])
# def my_post():
#     text = request.form['text']
#     logging.info(f'Text : {text}')

#     preprocessed_txt = preprocessing(text)
#     logging.info(f'Preprocessed Text : {preprocessed_txt}')

#     vectorized_txt = vectorizer(preprocessed_txt)
#     logging.info(f'Vectorized Text : {vectorized_txt}')

#     prediction = get_prediction(vectorized_txt)
#     logging.info(f'Prediction : {prediction}')

#     if prediction == 'negative':
#         global negative
#         negative += 1
#     else:
#         global positive
#         positive += 1
    
#     reviews.insert(0, text)
#     return redirect(request.url)

# if __name__ == "__main__":
#     app.run()









from flask import Flask, render_template, request, redirect, url_for
from helper import preprocessing, vectorizer, get_prediction
from logger import logging

app = Flask(__name__)

logging.info('Flask server started')

data = dict()
reviews = []
positive = 0
negative = 0

@app.route("/")
def index():
    data['reviews'] = reviews
    data['positive'] = positive
    data['negative'] = negative

    logging.info('========== Open home page ============')

    return render_template('index.html', data=data)

@app.route("/", methods=['POST'])
def my_post():
    text = request.form['text']
    logging.info(f'Text : {text}')

    preprocessed_txt = preprocessing(text)
    logging.info(f'Preprocessed Text : {preprocessed_txt}')

    vectorized_txt = vectorizer(preprocessed_txt)
    logging.info(f'Vectorized Text : {vectorized_txt}')

    prediction = get_prediction(vectorized_txt)
    logging.info(f'Prediction : {prediction}')

    global positive, negative
    if prediction == 'negative':
        negative += 1
    else:
        positive += 1

    reviews.insert(0, text)
    return redirect(request.url)

@app.route("/delete/<int:review_index>", methods=['POST'])
def delete_review(review_index):
    global positive, negative
    if 0 <= review_index < len(reviews):
        deleted_review = reviews.pop(review_index)
        preprocessed_txt = preprocessing(deleted_review)
        vectorized_txt = vectorizer(preprocessed_txt)
        prediction = get_prediction(vectorized_txt)

        if prediction == 'negative':
            negative -= 1
        else:
            positive -= 1

    logging.info(f'Deleted review at index: {review_index}')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
