from flask import Flask, render_template, abort, url_for, current_app, send_from_directory
from nba_news_reader import *
import db_utils
import os
import time
from gtts import gTTS

app = Flask(__name__,
            template_folder='templates')

# initialize leveldb
news_db = db_utils.init("news.db")
            
@app.route('/')
def root():
    return "The server is on."

@app.route('/main')
def main():
    news_titles = db_utils.get_keys(news_db)
    return render_template('main.html', data=news_titles)
    
@app.route('/news/<string:date>')
def news(date):
    if db_utils.isValid(news_db, date):
        news_content = db_utils.search(news_db, date)
        print(news_content)
        return render_template('content.html', date=date, text=news_content)
    else:
        abort(404)

# Convert text to audio and Save
def generate_mp3(key):
    filename = "nba_news_{}.mp3".format(key)
    text = db_utils.search(news_db, key)
    
    tts = gTTS(text=text, lang="zh")
    tts.save("audio\\{}".format(filename))
    return filename
        
# Download audio file from server
@app.route('/mp3/<string:key>')
def download(key):
    
    filename = generate_mp3(key)
    
    path = os.path.join(current_app.root_path, "audio")
    return send_from_directory(directory=path, filename=filename, as_attachment=True)

if __name__ == "__main__":
    
    # Get the latest news
    key = time.strftime("%Y%m%d")
    if db_utils.isValid(news_db, key):
        value = get_latest_news(key).encode("utf-8")
        db_utils.update(news_db, key, value)
        print("Update Today NBA News.")
    else:
        value = get_latest_news(key).encode("utf-8")
        db_utils.insert(news_db, key, value)
        print("Add Today NBA News to DB.")

    app.run(debug=False, port=8080)