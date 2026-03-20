
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def setup_vulnerable_db():
    """Create a test database for demonstration"""
    conn = sqlite3.connect('vulnerable_demo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            secret TEXT
        )
    ''')
    
    cursor.execute("DELETE FROM users") 
    
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'admin123', 'Secret: Flag{SQL_Injection_Success}')")
    cursor.execute("INSERT INTO users VALUES (2, 'user', 'password', 'Secret: Nothing here')")
    cursor.execute("INSERT INTO users VALUES (3, 'guest', 'guest', 'Secret: Just a guest')")
    cursor.execute("INSERT INTO users VALUES (4, 'hacker', 'hackme', 'Secret: You found me!')")
    cursor.execute("INSERT INTO users VALUES (5, 'test', 'test', 'Secret: Test account')")
    conn.commit()
    conn.close()

@app.route('/vulnerable-login', methods=['POST'])
def vulnerable_login():
    """
    """
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    result = ""
    error = ""
    
    conn = sqlite3.connect('vulnerable_demo.db')
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    print(f"🔍 Executing query: {query}")
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        
        if user:
            result = f"✅ Welcome, {user[1]}! Your secret is: {user[3]}"
        else:
            error = "❌ Invalid credentials"
    except Exception as e:
        error = f"💥 Database Error: {str(e)}"
    
    conn.close()
    
    return jsonify({
        'result': result,
        'error': error,
        'query': query
    })

@app.route('/secure-login', methods=['POST'])
def secure_login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    conn = sqlite3.connect('vulnerable_demo.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    print(f"🔒 Executing secure query with parameters")
    
    try:
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        if user:
            result = f"✅ Welcome, {user[1]}!"
        else:
            result = "❌ Invalid credentials"
    except Exception as e:
        result = f"Error: {str(e)}"
    
    conn.close()
    
    return jsonify({'result': result})

@app.route('/')
def index():
    return '''
    <html>
    <head><title>SURYA'S SQL Injection Demo</title></head>
    <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1>🎓 SQL Injection Demo</h1>
        <p style="background: #fee; padding: 15px; border-left: 4px solid red;">
            ⚠️ <strong>WARNING:</strong> This is for educational purposes only!<br>
            The vulnerable endpoint demonstrates security flaws you should NEVER use in production.
        </p>
        
        <h2>Test Accounts</h2>
        <ul>
            <li>Username: <code>admin</code> Password: <code>admin123</code></li>
            <li>Username: <code>user</code> Password: <code>password</code></li>
        </ul>
        
        <h2>🚨 Try SQL Injection (Vulnerable Endpoint)</h2>
        <p>Try these malicious inputs to see SQL injection in action:</p>
        <ul>
            <li>Username: <code>admin' OR '1'='1</code> Password: <code>anything</code></li>
            <li>Username: <code>' OR 1=1 --</code> Password: <code>anything</code></li>
            <li>Username: <code>admin'--</code> Password: <code>anything</code></li>
        </ul>
        
        <div style="border: 2px solid red; padding: 20px; margin: 20px 0; background: #ffe;">
            <h3>Vulnerable Login Form</h3>
            <input id="vuln_user" placeholder="Username" style="padding: 8px; width: 200px;"><br><br>
            <input id="vuln_pass" type="password" placeholder="Password" style="padding: 8px; width: 200px;"><br><br>
            <button onclick="vulnerableLogin()" style="padding: 10px 20px; background: red; color: white; border: none; cursor: pointer;">
                Login (Vulnerable)
            </button>
            <div id="vuln_result" style="margin-top: 15px;"></div>
        </div>
        
        <div style="border: 2px solid green; padding: 20px; margin: 20px 0; background: #efe;">
            <h3>Secure Login Form</h3>
            <input id="sec_user" placeholder="Username" style="padding: 8px; width: 200px;"><br><br>
            <input id="sec_pass" type="password" placeholder="Password" style="padding: 8px; width: 200px;"><br><br>
            <button onclick="secureLogin()" style="padding: 10px 20px; background: green; color: white; border: none; cursor: pointer;">
                Login (Secure)
            </button>
            <div id="sec_result" style="margin-top: 15px;"></div>
        </div>
        
        <script>
            async function vulnerableLogin() {
                const username = document.getElementById('vuln_user').value;
                const password = document.getElementById('vuln_pass').value;
                
                const response = await fetch('/vulnerable-login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password})
                });
                
                const data = await response.json();
                document.getElementById('vuln_result').innerHTML = 
                    '<strong>Query executed:</strong><br><code>' + data.query + '</code><br><br>' +
                    '<strong>Result:</strong> ' + (data.result || data.error);
            }
            
            async function secureLogin() {
                const username = document.getElementById('sec_user').value;
                const password = document.getElementById('sec_pass').value;
                
                const response = await fetch('/secure-login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password})
                });
                
                const data = await response.json();
                document.getElementById('sec_result').innerHTML = 
                    '<strong>Result:</strong> ' + data.result;
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("\n" + "="*60)
    print("⚠️  SQL INJECTION DEMONSTRATION ⚠️")
    print("="*60)
    print("This app demonstrates SQL injection vulnerabilities")
    print("NEVER use the vulnerable code in production!")
    print("\nOpen: http://localhost:5001")
    print("="*60 + "\n")
    
    setup_vulnerable_db()
    app.run(debug=True, port=5001)
    