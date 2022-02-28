import os
import sys
import flask
import requests
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import Column, Integer, String

app = flask.Flask(__name__)
app.secret_key = 'some_unique_key_used_to_encrypt_client_side_session_data'

Base = sqlalchemy.orm.declarative_base()
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)

if not "DATABASE_URL" in os.environ:
    print("DATABASE_URL must be set")
    sys.exit()

database_url = os.environ["DATABASE_URL"]
engine = sqlalchemy.create_engine(f'sqlite:///{database_url}')

if not os.path.exists(database_url):
    app.app_context().push()
    print(f"Creating {database_url}")
    Base.metadata.create_all(engine)

session = sqlalchemy.orm.sessionmaker(bind=engine)

def get_requests_count():
    counter = flask.session["counter"] if "counter" in flask.session else 0
    counter += 1
    flask.session["counter"] = counter
    return counter

@app.route("/")
def index():
    return flask.send_file(f"../public/index.html")

@app.route("/<static_filename>")
def static_files(static_filename):
    return flask.send_file(f"../public/{static_filename}")

@app.route("/items")
def sample_retrieve_all():
    db_session = session()
    try:
        result = db_session.query(Item).all()
        items = []
        for row in result:
            items.append({
                "id": row.id,
                "name": row.name
            })
        return flask.jsonify({
            "items": items,
            "requests_count": get_requests_count()
        })
    except Exception as e:
        return flask.jsonify(str(e))
    finally:
        db_session.close()

@app.route("/items", methods=['POST'])
def sample_create():
    db_session = session()
    try:
        obj = flask.request.get_json()
        item = Item(name=obj["name"])
        db_session.add(item)
        db_session.commit()
        return flask.jsonify({
            "inserted_id": item.id,
            "requests_count": get_requests_count()
        })
    except Exception as e:
        return flask.jsonify(str(e))
    finally:
        db_session.close()

@app.route("/items/<id>", methods=['GET'])
def sample_retrieve(id):
    db_session = session()
    try:
        item = db_session.query(Item).filter_by(id=id).one()
        return flask.jsonify({
            "name": item.name,
            "requests_count": get_requests_count()
        })
    except Exception as e:
        return flask.jsonify(str(e))
    finally:
        db_session.close()

@app.route("/items/<id>", methods=['PUT'])
def sample_update(id):
    db_session = session()
    try:
        obj = flask.request.get_json()
        item = db_session.query(Item).filter_by(id=id).one()
        item.name = obj["name"]
        db_session.commit()
        return flask.jsonify({
            "requests_count": get_requests_count()
        })
    except Exception as e:
        return flask.jsonify(str(e))
    finally:
        db_session.close()

@app.route("/items/<id>", methods=['DELETE'])
def sample_delete(id):
    db_session = session()
    try:
        item = db_session.query(Item).filter_by(id=id).delete()
        db_session.commit()
        return flask.jsonify({
            "requests_count": get_requests_count()
        })
    except Exception as e:
        return flask.jsonify(str(e))
    finally:
        db_session.close()

@app.route("/myip")
def sample_http_client():
    try:
        obj = requests.get("http://httpbin.org/ip").json()
        return flask.jsonify({
            "myIP": obj["origin"],
            "requests_count": get_requests_count()
        })
    except Exception as e:
        return flask.jsonify(str(e))
