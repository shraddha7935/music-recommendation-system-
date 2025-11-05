from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Load song data
songs_df = pd.read_csv('songs.csv')

# Home route
@app.route('/')
def home():
    # Get unique genres from CSV for dropdown
    genres = songs_df['genre'].unique()
    return render_template('index.html', genres=genres)

# Recommend route (POST method for form)
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        genre = request.form.get('genre')
        # Filter songs by genre
        filtered_songs = songs_df[songs_df['genre'].str.lower() == genre.lower()]

        if filtered_songs.empty:
            message = f"No songs found for genre: {genre}"
            return render_template('recommend.html', songs=[], message=message)

        return render_template('recommend.html', songs=filtered_songs.to_dict(orient='records'), message=None)
    return redirect(url_for('home'))

# Serve songs from static folder
@app.route('/songs/<filename>')
def get_song(filename):
    return redirect(url_for('static', filename=f'songs/{filename}'))

if __name__ == '__main__':
    app.run(debug=True)
