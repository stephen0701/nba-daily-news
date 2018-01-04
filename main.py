from flask import Flask, render_template, abort, url_for, current_app, send_from_directory, redirect
from nba_news_reader import *
import db_utils
import os
import time
from gtts import gTTS

app = Flask(__name__,
            template_folder='templates')
            
@app.route('/')
def root():
    return "The server is on."

@app.route('/main')
def main():
    
    # initialize leveldb
    news_db = db_utils.init("news.db")
    
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
    
    news_titles = db_utils.get_keys(news_db)
    return render_template('main.html', data=news_titles)
    
@app.route('/news/<string:date>')
def news(date):

    # initialize leveldb
    news_db = db_utils.init("news.db")

    # Render the news website page
    if db_utils.isValid(news_db, date):
        news_content = db_utils.search(news_db, date)
        # print(news_content)
        return render_template('content.html', date=date, text=news_content)
    else:
        abort(404)
        
# Convert text to audio and Save
def generate_mp3(db, key):
    filename = "nba_news_{}.mp3".format(key)
    text = db_utils.search(db, key)
    
    tts = gTTS(text=text, lang="zh")
    tts.save("audio/{}".format(filename))
    return filename
        
# Download audio file from server
@app.route('/mp3/<string:key>')
def download(key):
    try:
        # initialize leveldb
        news_db = db_utils.init("news.db")
        
        filename = generate_mp3(news_db, key)
        
        file_path = os.path.join(current_app.root_path, "audio")
        print("file path:{}/{}".format(file_path,filename))
        
        if os.path.isfile("{}/{}".format(file_path,filename)):
            print("The file is found")
            return send_from_directory(directory=file_path, filename=filename, as_attachment=True)
        else:
            print("The file is not found")
            return redirect(url_for('news', date=key))
    except:
        return redirect(url_for('news', date=key))
        
if __name__ == "__main__":
    
    app.run(debug=False, port=8080)