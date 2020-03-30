# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask, render_template, request, url_for, redirect
import text_to_emoji
  
# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__) 
  
# The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function. 
@app.route('/') 
def run_app(): 
    return render_template('index.html')

# This function renders the result
@app.route('/result')
def result():
    question = request.args.get('jsdata')
    print(question)
    answer = ""
    possible_emojis = {}
    words_set = []
    if question:
        emojis_dict = text_to_emoji.load_emojis_json('emojis.json')
        answer, possible_emojis, words_set = text_to_emoji.text_to_emoji(emojis_dict, question)

    return render_template('result.html', answer=answer, possible_emojis=possible_emojis, words_set=words_set)


# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run(debug=True) 