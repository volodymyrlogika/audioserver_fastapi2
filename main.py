from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, Query, Path, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Field, Session, SQLModel, create_engine, select
from models import Track, User, TrackUpdate
from auth import token_create
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

sqlite_file_name = "audioserver.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# OAuth2PasswordBearer - це клас, який використовується для визначення схеми аутентифікації OAuth2 з паролем. 
# Він вказує, що токен доступу буде отриманий через URL-адресу "/token".
# Це дозволяє FastAPI автоматично обробляти запити на отримання токена та перевіряти його при кожному запиті до захищених маршрутів.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()



@app.post('/token')
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep ):
    user = session.exec(select(User).where(User.login == form_data.username)).first()
    if not user or form_data.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = token_create(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", response_class=HTMLResponse)
async def track_list_page(request: Request, session: SessionDep):
    tracks = session.exec(select(Track)).all()

    return templates.TemplateResponse(
        request=request, name="track_list.html", context={"tracks": tracks}
    )

@app.get("/tracks/all")
async def get_all_tracks(session: SessionDep):
    tracks = session.exec(select(Track)).all()

    return {"Tracks": tracks}


@app.get('/tracks/search')
async def search_track(
        q: Annotated[str, Query(..., min_length=1, max_length=50, description='Пошуковий запит')],
        session: SessionDep
    ):
    q = q.lower().strip()
    result = session.exec(select(Track).where(Track.title.ilike(f"%{q}%") | Track.artist.ilike(f"%{q}%"))).all()
    if not result:
        raise HTTPException(status_code=404, detail="No tracks found matching the query")
    return {'query': q, 'result': result}


@app.get("/tracks/{track_id}")
async def get_track(track_id: int, session: SessionDep):
    track = session.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    return {"track": track}


@app.post("/tracks/add")
async def add_new_track(body: Track, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    session.add(body)
    session.commit()
    session.refresh(body)
    return {"message": "Track added", "track": body}


@app.delete("/tracks/{track_id}")
async def delete_track(track_id: int, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    track = session.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    session.delete(track)
    session.commit()
    return {'message': 'Track deleted'}


@app.patch("/tracks/{track_id}")
async def update_track(track_id: int, body: TrackUpdate, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    track = session.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    track_data = body.model_dump(exclude_unset=True)
    track.sqlmodel_update(track_data)
    session.add(track)
    session.commit()
    session.refresh(track)
    return track

    

