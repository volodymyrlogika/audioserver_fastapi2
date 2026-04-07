from sqlmodel import Session, create_engine, select
from models import Track

sqlite_url = "sqlite:///audioserver.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

tracks = [
    Track(title="Bohemian Rhapsody", artist="Queen", album="A Night at the Opera", genre="Rock", year=1975),
    Track(title="Hotel California", artist="Eagles", album="Hotel California", genre="Rock", year=1977),
    Track(title="Billie Jean", artist="Michael Jackson", album="Thriller", genre="Pop", year=1982),
    Track(title="Smells Like Teen Spirit", artist="Nirvana", album="Nevermind", genre="Grunge", year=1991),
    Track(title="Lose Yourself", artist="Eminem", album="8 Mile", genre="Hip-Hop", year=2002),
    Track(title="Rolling in the Deep", artist="Adele", album="21", genre="Soul", year=2010),
    Track(title="Shape of You", artist="Ed Sheeran", album="Divide", genre="Pop", year=2017),
    Track(title="Blinding Lights", artist="The Weeknd", album="After Hours", genre="Synth-pop", year=2019),
    Track(title="Stairway to Heaven", artist="Led Zeppelin", album="Led Zeppelin IV", genre="Rock", year=1971),
    Track(title="What's Going On", artist="Marvin Gaye", album="What's Going On", genre="Soul", year=1971),
]

with Session(engine) as session:
    for track in tracks:
        session.add(track)
    session.commit()
    print(f"Додано {len(tracks)} треків до бази даних.")
