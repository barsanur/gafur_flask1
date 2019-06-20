from flask import Flask, request, flash, redirect, url_for
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import os
import time
from datetime import datetime
import pipes
import os.path


app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)


csrf_protect = CSRFProtect(app)
api = Api(app, decorators=[csrf_protect.exempt])

mysql = MySQL(cursorclass=DictCursor)

app.secret_key = os.urandom(24)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ocp32COsa6/'
app.config['MYSQL_DATABASE_DB'] = 'gafur1'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

homedir = os.path.expanduser("~")

DB_HOST = 'localhost' 
DB_USER = 'root'
DB_USER_PASSWORD = 'ocp32COsa6/'
DB_NAME = 'gafur1'
BACKUP_PATH = homedir+'/Folder'

mysql.init_app(app)


class backupData(Resource):
    def get(self):
        try:
            os.stat(BACKUP_PATH)
        except:
            os.mkdir(BACKUP_PATH)
        now = datetime.now() # current date and time
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        time = now.strftime("%H:%M:%S")
        date_time = now.strftime("%d_%m_%Y_%H:%M:%S")
        TODAYBACKUPPATH = BACKUP_PATH + '/' + date_time

        try:
            os.stat(TODAYBACKUPPATH)
        except:
            os.mkdir(TODAYBACKUPPATH)
        print ("checking for databases names file.")
        
        if os.path.exists(DB_NAME):
            file1 = open(DB_NAME)
            multi = 1
            print ("Databases file found...")
            print ("Starting backup of all dbs listed in file " + DB_NAME)
        else:
            print ("Databases file not found...")
            print ("Starting backup of database " + DB_NAME)
            multi = 0
        
        if multi:
            in_file = open(DB_NAME,"r")
            flength = len(in_file.readlines())
            in_file.close()
            p = 1
            dbfile = open(DB_NAME,"r")
        
            while p <= flength:
                db = dbfile.readline()   # reading database name from file
                db = db[:-1]         # deletes extra line
                dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
                os.system(dumpcmd)
                gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
                os.system(gzipcmd)
                p = p + 1
            dbfile.close()
        else:
            db = DB_NAME
            dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
            os.system(dumpcmd)
            gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
            os.system(gzipcmd)
            # t = ("Your backups have been created in '" + TODAYBACKUPPATH + "' directory")
            return "Your Folder have been created in '" + TODAYBACKUPPATH + "'." 
        


class TrennbareList(Resource):
    def get(self):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM trennbare ORDER BY id desc"
            cursor.execute(sql)
            return cursor.fetchall()
    
    def post(self):
        word = request.json["word"]
        answer = request.json["answer"]
        category_id = request.json["category_id"]
        try:
            with mysql.connect() as cursor:
                sql = "INSERT INTO trennbare (word,  answer, category_id) VALUES (%s, %s, %s)"
                val = (word, answer, category_id)
                cursor.execute(sql, val)
                return {"status": "Ok"}
        except:
            return {"status": "error"}

class TrennbareByLevel(Resource):
    def get(self, trennbare_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM trennbare WHERE category_id='{}' ORDER BY RAND() LIMIT 1".format(trennbare_id)
            cursor.execute(sql)
            return cursor.fetchall()[0]

class Trennbare(Resource):
    def get(self, trennbare_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM trennbare WHERE id="+trennbare_id
            cursor.execute(sql)
            return cursor.fetchone()
    
    def delete(self,trennbare_id):
        try:
            with mysql.connect() as cursor:
                sql = "DELETE  FROM trennbare WHERE id=" + trennbare_id
                cursor.execute(sql)
                return {"data": "was deleted"}
        except:
                return {"status": "error"}

    def put(self, trennbare_id):
        word = request.json["word"]
        answer = request.json["answer"]
        category_id = request.json["category_id"]
        
        try:    
            with mysql.connect() as cursor:
                cursor.execute("""UPDATE trennbare SET word=%s, answer=%s, category_id=%s WHERE id=%s""",
                (word, answer, category_id, trennbare_id))
                return {"Data": "was Updated"}
        except:
            return {"status": "error"}        
class PerfektList(Resource):
    def get(self):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM perfekt ORDER BY id desc"
            cursor.execute(sql)
            return cursor.fetchall()
    
    def post(self):
        word = request.json["word"]
        answer = request.json["answer"]
        category_id = request.json["category_id"]
        try:
            with mysql.connect() as cursor:
                sql = "INSERT INTO perfekt (word,  answer, category_id) VALUES (%s, %s, %s)"
                val = (word, answer, category_id)
                cursor.execute(sql, val)
                return {"status": "Ok"}
        except:
            return {"status": "error"}

class PerfektByLevel(Resource):
    def get(self, perfekt_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM perfekt WHERE category_id='{}' ORDER BY RAND() LIMIT 1".format(perfekt_id)
            cursor.execute(sql)
            return cursor.fetchall()[0]

class Perfekt(Resource):
    def get(self, perfekt_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM perfekt WHERE id="+perfekt_id
            cursor.execute(sql)
            return cursor.fetchone()
    
    def delete(self,perfekt_id):
        try:
            with mysql.connect() as cursor:
                sql = "DELETE  FROM perfekt WHERE id=" + perfekt_id
                cursor.execute(sql)
                return {"data": "was deleted"}
        except:
                return {"status": "error"}

    def put(self, perfekt_id):
        word = request.json["word"]
        answer = request.json["answer"]
        category_id = request.json["category_id"]
        
        try:    
            with mysql.connect() as cursor:
                cursor.execute("""UPDATE perfekt SET word=%s, answer=%s, category_id=%s WHERE id=%s""",
                (word, answer, category_id, perfekt_id))
                return {"Data": "was Updated"}
        except:
            return {"status": "error"}       
            
class NounsList(Resource):
    def get(self):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM noun ORDER BY id desc"
            cursor.execute(sql)
            return cursor.fetchall()
    
    def post(self):
        word = request.json["word"]
        answer = request.json["answer"]
        category_id = request.json["category_id"]
        try:
            with mysql.connect() as cursor:
                sql = "INSERT INTO noun (word,  answer, category_id) VALUES (%s, %s, %s)"
                val = (word, answer, category_id)
                cursor.execute(sql, val)
                return {"status": "Ok"}
        except:
            return {"status": "error"}

class NounByLevel(Resource):
    def get(self, noun_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM noun WHERE category_id='{}' ORDER BY RAND() LIMIT 1".format(noun_id)
            cursor.execute(sql)
            return cursor.fetchall()[0]

class Noun(Resource):
    def get(self, noun_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM noun WHERE id="+noun_id
            cursor.execute(sql)
            return cursor.fetchone()
    
    def delete(self,noun_id):
        try:
            with mysql.connect() as cursor:
                sql = "DELETE  FROM noun WHERE id=" + noun_id
                cursor.execute(sql)
                return {"data": "was deleted"}
        except:
                return {"status": "error"}

    def put(self, noun_id):
        word = request.json["word"]
        answer = request.json["answer"]
        category_id = request.json["category_id"]
        
        try:    
            with mysql.connect() as cursor:
                cursor.execute("""UPDATE noun SET word=%s, answer=%s, category_id=%s WHERE id=%s""",
                (word, answer, category_id, noun_id))
                return {"Data": "was Updated"}
        except:
            return {"status": "error"}

class VerbsList(Resource):
    def get(self):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM verb ORDER BY id desc"
            cursor.execute(sql)
            return cursor.fetchall()
    
    def post(self):
        word = request.json["word"]
        answer = request.json["answer"]
        category_id = request.json["category_id"]
        try:
            with mysql.connect() as cursor:
                sql = "INSERT INTO verb (word,  answer, category_id) VALUES (%s, %s, %s)"
                val = (word, answer, category_id)
                cursor.execute(sql, val)
                return {"status": "Ok"}
        except:
            return {"status": "error"}

class VerbByLevel(Resource):
    def get(self, verb_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM verb WHERE category_id='{}' ORDER BY RAND() LIMIT 1".format(verb_id)
            cursor.execute(sql)
            return cursor.fetchall()[0]

class Verb(Resource):
    def get(self, verb_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM verb WHERE id="+verb_id
            cursor.execute(sql)
            return cursor.fetchone()
    
    def delete(self,verb_id):
        try:
            with mysql.connect() as cursor:
                sql = "DELETE  FROM verb WHERE id=" + verb_id
                cursor.execute(sql)
                return {"data": "was deleted"}
        except:
                return {"status": "error"}

    def put(self, verb_id):
        word = request.json["word"]
        answer = request.json["answer"]
        category_id = request.json["category_id"]
        
        try:    
            with mysql.connect() as cursor:
                cursor.execute("""UPDATE verb SET word=%s, answer=%s, category_id=%s WHERE id=%s""",
                (word, answer, category_id, verb_id))
                return {"Data": "was Updated"}
        except:
            return {"status": "error"}

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



api.add_resource(backupData, '/backup')
api.add_resource(TrennbareList, '/trennbares')
api.add_resource(TrennbareByLevel, '/trennbares/level/<string:trennbare_id>')
api.add_resource(Trennbare, '/trennbares/<string:trennbare_id>')
api.add_resource(PerfektList, '/perfekts')
api.add_resource(PerfektByLevel, '/perfekts/level/<string:perfekt_id>')
api.add_resource(Perfekt, '/perfekts/<string:perfekt_id>')
api.add_resource(NounsList, '/nouns')
api.add_resource(NounByLevel, '/nouns/level/<string:noun_id>')
api.add_resource(Noun, '/nouns/<string:noun_id>')
api.add_resource(VerbsList, '/verbs')
api.add_resource(VerbByLevel, '/verbs/level/<string:verb_id>')
api.add_resource(Verb, '/verbs/<string:verb_id>')
api.add_resource(WordsList, '/words')
api.add_resource(ExampleList, '/examples')
api.add_resource(GrammarList, '/grammars')
api.add_resource(CategoryList, '/categories')
api.add_resource(Word, '/words/<string:word_id>')
api.add_resource(Example, '/examples/<string:example_id>')
api.add_resource(Grammar, '/grammars/<string:grammar_id>')
api.add_resource(QuestionListByLevel, '/level/<string:level_id>')
api.add_resource(WordsByLevel, '/words/level/<string:level_id>')
api.add_resource(ExamplesByLevel, '/examples/level/<string:level_id>')
api.add_resource(GrammarsByLevel, '/grammars/level/<string:level_id>')



if __name__ == '__main__':
    app.run(host='0.0.0.0')