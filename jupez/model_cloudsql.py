from flask import Flask
from flask_sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START model]
class Jupe(db.Model):
    __tablename__ = 'jupes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publishedDate = db.Column(db.String(255))
    imageUrl = db.Column(db.String(255))
    description = db.Column(db.String(4096))
    createdBy = db.Column(db.String(255))
    createdById = db.Column(db.String(255))

    def __repr__(self):
        return "<Jupe(title='%s', author=%s)" % (self.title, self.author)
# [END model]


# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Jupe.query
             .order_by(Jupe.title)
             .limit(limit)
             .offset(cursor))
    jupes = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(jupes) == limit else None
    return (jupes, next_page)
# [END list]


# [START read]
def read(id):
    result = Jupe.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def create(data):
    jupe = Jupe(**data)
    db.session.add(jupe)
    db.session.commit()
    return from_sql(jupe)
# [END create]


# [START update]
def update(data, id):
    jupe = Jupe.query.get(id)
    for k, v in data.items():
        setattr(jupe, k, v)
    db.session.commit()
    return from_sql(jupe)
# [END update]


def delete(id):
    Jupe.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()