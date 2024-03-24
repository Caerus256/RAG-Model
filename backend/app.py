# Code with user Authentication
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
import cassio
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

ASTRA_DB_APPLICATION_TOKEN = "AstraCS:TnAKCcGXsYFqQFTMlzcohEYT:163639b6277776f852895af91f727c3f3f682188edc948ae4b23c5195395db6b"
ASTRA_DB_ID = "028ab0ff-bd0c-49de-a050-b81c743468f7"
OPENAI_API_KEY = "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"

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    ''')
    conn.close()

# Register User
def register_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

# Check if User Exists
def user_exists(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Authenticate User
def authenticate_user(username, password):
    user = user_exists(username)
    if user and check_password_hash(user[2], password):
        return True
    return False

# Initialize Database
init_db()


# PDF Processing
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_file_path = os.path.join(current_dir, 'pdf4testing.pdf')
pdfreader = PdfReader(pdf_file_path)
raw_text = ""
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        raw_text += content
        break

cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800, # Can be changed for further optimization
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)

astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="qa_mini_demo",
    session=None,
    keyspace=None,
)

# Top 50 related data is added to the database
astra_vector_store.add_texts(texts[:50])  # We can use the whole data-set if we want
astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

#####
app.config['UPLOAD_FOLDER'] = 'PDF Files'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Train the model using the uploaded file here
        pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdfreader = PdfReader(pdf_file_path)
        raw_text = ""
        for i, page in enumerate(pdfreader.pages):
            content = page.extract_text()
            if content:
                raw_text += content

        cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)
        llm = OpenAI(openai_api_key=OPENAI_API_KEY)
        embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

        # Data preprocessing 
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=200,
            length_function=len,
        )

        texts = text_splitter.split_text(raw_text)
        astra_vector_store = Cassandra(
            embedding=embedding,
            table_name="qa_mini_demo",
            session=None,
            keyspace=None,
        )

        # Top 50 related data is added to the database
        astra_vector_store.add_texts(texts[:50])
        astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)
        return jsonify({'message': 'File uploaded and model trained successfully'})
    else:
        return jsonify({'message': 'File format not supported'})
#####

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    query_text = data.get('question', '').strip()
    if not query_text:
        return jsonify({'error': 'No question provided'})

    answer = astra_vector_index.query(query_text, llm=llm).strip()

    return jsonify({'answer': answer})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not user_exists(username):
            register_user(username, password)
            return redirect(url_for('login'))
        return "Username already exists! Please try someone other username!!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            return redirect(url_for('protected_route'))
        return "Invalid username or password!"
    return render_template('login.html')

@app.route('/protected')
def protected_route():
    return render_template('index.html') # Dynamically render HTML template

if __name__ == '__main__': # Checking if the script being executed is the main script & is not a module 
    app.run(debug=True) # Restarts the server when changes are detected!