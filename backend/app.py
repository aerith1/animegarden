from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ernest/Sakura/backend/databases.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
class Anime(db.Model):
    __tablename__ = "Anime"
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(256), nullable=False)
    size = db.Column(db.String(64), nullable=False)
    release_time = db.Column(db.String(32), nullable=False)
    download_link = db.Column(db.String(4096), nullable=False)

@app.route('/', methods=['get'])
def index():
    page = int(request.args.get('page', 1))
    display_count = 10
    start = (page - 1) * display_count
    end = start + display_count
    anime = Anime.query.all()
    total_pages = int(Anime.query.count() / display_count) + 1
    anime_list = [] 
    for a in anime:
        anime_list.append({
            "id": a.id,
            "title": a.title,
            "category": a.category,
            "size": a.size,
            "release_time": a.release_time,
            "download_link": a.download_link
        })
    anime_list.reverse()
    return jsonify({
        "data": anime_list[start:end],
        "total_pages": total_pages
    })


if __name__ == '__main__':
    app.run(debug=True)
