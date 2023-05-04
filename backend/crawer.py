import requests
import uuid
import time
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_path = 'sqlite:///databases.db'
engine = create_engine(db_path)

Base = declarative_base()

class Anime(Base):
    __tablename__ = 'Anime'
    id = Column(String(36), primary_key=True)
    title = Column(String(256), nullable=False)
    category = Column(String(256), nullable=False)
    size = Column(String(64), nullable=False)
    release_time = Column(String(32), nullable=False)
    download_link = Column(String(4096), nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

while True:
    rows = []
    names = []
    url = "https://share.dmhy.org/"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find('div', {'class': 'container'})
    bg = container.find('div', {'class': 'bg'})
    table_clear = bg.find('div', {'class': 'table clear'})
    table = table_clear.find('table',{'class':'tablesorter'})
    tbody = table.find('tbody')
    for tr in tbody.find_all('tr'):
        row = {}
        row['id'] = str(uuid.uuid4())
        for td in tr.find_all('td'):
            if td.get('width') == '98':
                span = td.find('span', {'style': 'display: none;'})
                if span:
                    row['release_time'] = (span.text.strip())
                    continue
            if td.get('width') == '6%':
                category = td.find('font')
                if category:
                    row['category'] = (category.text.strip())
                    continue
            if td.get('class') == ['title']:
                row['title'] = (td.find('a', recursive=False).text.strip())
                continue
            if td.get('nowrap') == 'nowrap' and td.get('align') == 'center':
                if not td.find_all():
                    row['size'] = (td.text.strip())
                    break
                if td.find('a'):
                    row['download_link'] = (td.find('a').get('href'))
                    continue
        rows.append(row)

    sorted_rows = sorted(rows, key=lambda x: x['release_time'])
    # 插入数据
    for row in sorted_rows:
        torrent = session.query(Anime).filter_by(title=row['title'], release_time=row['release_time']).first()
        if torrent:
            torrent.download_link = row['download_link']
            torrent.size = row['size']
        else:
            torrent = Anime(
                id = row['id'],
                title = row['title'],
                category = row['category'],
                release_time = row['release_time'],
                download_link = row['download_link'],
                size = row['size']
            )
        session.add(torrent)

    current_time = int(time.time())
    localtime = time.localtime(current_time)
    nowtime = time.strftime('%Y:%m:%d %H:%M:%S', localtime)

    session.commit()
    print(nowtime)
    time.sleep(600)
