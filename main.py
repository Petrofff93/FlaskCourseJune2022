from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:123321@localhost:5432/store'

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


# Creating the model class for the books
class BookModel(db.Model):
    __tablename__ = 'books'
    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<{self.pk}> {self.title} from {self.author}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Class based view in order to manipulate the books array
class Books(Resource):
    def post(self):
        data = request.get_json()
        new_book = BookModel(**data)
        db.session.add(new_book)
        db.session.commit()
        return new_book.as_dict()


db.create_all()
api.add_resource(Books, "/")

if __name__ == "__main__":
    app.run(debug=True)
