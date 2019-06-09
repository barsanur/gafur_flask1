from flask import Flask, request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)


csrf_protect = CSRFProtect(app)
api = Api(app, decorators=[csrf_protect.exempt])

mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'gafur1'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class Word(Resource):
    def get(self, word_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM words WHERE id=" + word_id
            cursor.execute(sql)
            return cursor.fetchall()[0]
    
    def delete(self,word_id):
        try:
            with mysql.connect() as cursor:
                sql = "DELETE  FROM words WHERE id=" + word_id
                cursor.execute(sql)
                return {"data": "was deleted"}
        except:
                return {"status": "error"}

    def put(self, word_id):
        word = request.json["word"]
        isNoun = request.json["isNoun"]
        category_id = request.json["category_id"]
        
        try:    
            with mysql.connect() as cursor:
                cursor.execute("""UPDATE words SET word=%s, isNoun=%s, category_id=%s WHERE id=%s""",
                (word, isNoun, category_id, word_id))
                return {"Data": "was Updated"}
        except:
            return {"status": "error"}

class Example(Resource):
    def get(self, example_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM examples WHERE id=" + example_id
            cursor.execute(sql)
            return cursor.fetchall()[0]
    
    def delete(self,example_id):
        try:
            with mysql.connect() as cursor:
                sql = "DELETE  FROM examples WHERE id=" + example_id
                cursor.execute(sql)
                return {"data": "was deleted"}
        except:
                return {"status": "error"}

    def put(self, example_id):
        example = request.json["example"]
        category_id = request.json["category_id"]
        
        try:    
            with mysql.connect() as cursor:
                cursor.execute("""UPDATE examples SET example=%s, category_id=%s WHERE id=%s""",
                (example, category_id, example_id))
                return {"Data": "was Updated"}
        except:
            return {"status": "error"}

class Grammar(Resource):
    def get(self, grammar_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM grammars WHERE id=" + grammar_id
            cursor.execute(sql)
            return cursor.fetchall()[0]
    
    def delete(self,grammar_id):
        try:
            with mysql.connect() as cursor:
                sql = "DELETE  FROM grammars WHERE id=" + grammar_id
                cursor.execute(sql)
                return {"data": "was deleted"}
        except:
                return {"status": "error"}

    def put(self, grammar_id):
        grammar = request.json["grammar"]
        category_id = request.json["category_id"]
        
        try:    
            with mysql.connect() as cursor:
                cursor.execute("""UPDATE grammars SET grammar=%s, category_id=%s WHERE id=%s""",
                (grammar, category_id, grammar_id))
                return {"Data": "was Updated"}
        except:
            return {"status": "error"}

class WordsList(Resource):
    def get(self):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM words ORDER BY id desc"
            cursor.execute(sql)
            return cursor.fetchall()
    
    def post(self):
        word = request.json["word"]
        isNoun = request.json["isNoun"]
        category_id = request.json["category_id"]
        try:
            with mysql.connect() as cursor:
                sql = "INSERT INTO words (word,  isNoun, category_id) VALUES (%s, %s, %s)"
                val = (word, isNoun, category_id)
                cursor.execute(sql, val)
                return {"status": "Ok"}
        except:
            return {"status": "error"}

class ExampleList(Resource):
    def get(self):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM examples ORDER BY id desc"
            cursor.execute(sql)
            return cursor.fetchall()
    
    def post(self):
        example = request.json["example"]
        category_id = request.json["category_id"]
        try:
            with mysql.connect() as cursor:
                sql = "INSERT INTO examples (example, category_id) VALUES (%s, %s)"
                val = (example, category_id)
                cursor.execute(sql, val)
                return {"status": "Ok"}
        except:
            return {"status": "error"}

class GrammarList(Resource):
    def get(self):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM grammars ORDER BY id desc"
            cursor.execute(sql)
            return cursor.fetchall()
    
    def post(self):
        grammar = request.json["grammar"]
        category_id = request.json["category_id"]
        try:
            with mysql.connect() as cursor:
                sql = "INSERT INTO grammars (grammar, category_id) VALUES (%s, %s)"
                val = (grammar, category_id)
                cursor.execute(sql, val)
                return {"status": "Ok"}
        except:
            return {"status": "error"}


class QuestionListByLevel(Resource):
    def get(self, level_id):
        try:
            with mysql.connect() as cursor:
                sql  = """SELECT words.word, examples.example, grammars.grammar, words.isNoun FROM words
                INNER JOIN examples ON words.category_id = examples.category_id
                INNER JOIN grammars ON grammars.category_id = examples.category_id
                WHERE words.category_id='{}' ORDER BY RAND() LIMIT 1""".format(level_id)
               
                cursor.execute(sql)

                return cursor.fetchall()
        except:
            return {"status": "Level error"}

class WordsByLevel(Resource):
    def get(self, level_id):
        try:
            with mysql.connect() as cursor:
                sql1 = """SELECT words.word, categories.category FROM words 
                INNER JOIN categories ON words.category_id = categories.id
                WHERE categories.category='{}'""".format(level_id)
                # sql = "SELECT * FROM words WHERE level='{}'".format(level_id)
                cursor.execute(sql1)
                return cursor.fetchall()
        except:
            return {"status": "Level error"}

class ExamplesByLevel(Resource):
    def get(self, level_id):
        try:
            with mysql.connect() as cursor:
                sql1 = """SELECT examples.example, categories.category FROM examples 
                INNER JOIN categories ON examples.category_id = categories.id
                WHERE categories.category='{}'""".format(level_id)
                # sql = "SELECT * FROM words WHERE level='{}'".format(level_id)
                cursor.execute(sql1)
                return cursor.fetchall()
        except:
            return {"status": "Level error"}

class GrammarsByLevel(Resource):
    def get(self, level_id):
        try:
            with mysql.connect() as cursor:
                sql1 = """SELECT grammars.grammar, categories.category FROM grammars 
                INNER JOIN categories ON grammars.category_id = categories.id
                WHERE categories.category='{}'""".format(level_id)
                # sql = "SELECT * FROM words WHERE level='{}'".format(level_id)
                cursor.execute(sql1)
                return cursor.fetchall()
        except:
            return {"status": "Level error"}
class CategoryList(Resource):
    def get(self):
        try:
            with mysql.connect() as cursor:
                
                sql = "SELECT * FROM categories"
                cursor.execute(sql)
                return cursor.fetchall()
        except:
            return {"status": "Level error"}


api.add_resource(WordsList, '/words')
api.add_resource(ExampleList, '/examples')
api.add_resource(GrammarList, '/grammars')
api.add_resource(CategoryList, '/categories')
api.add_resource(Word, '/words/<string:word_id>')
api.add_resource(Example, '/example/<string:example_id>')
api.add_resource(Grammar, '/grammar/<string:grammar_id>')
api.add_resource(QuestionListByLevel, '/level/<string:level_id>')
# api.add_resource(WordsByLevel, '/words/level/<string:level_id>')
# api.add_resource(ExamplesByLevel, '/examples/level/<string:level_id>')
# api.add_resource(GrammarsByLevel, '/grammars/level/<string:level_id>')



if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='http://159.89.1.89',port=8000,debug=True)