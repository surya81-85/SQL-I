# 🚀 Quick Start Guide - SQL Injection Demo

## Start the App (3 Steps)

```bash
# 1. Install Flask
pip install flask

# 2. Run the app
python vulnerable_demo.py

# 3. Open browser
http://localhost:5001
```

---

## 🎮 Try These Attacks

### On the RED "Vulnerable" Form:

**Attack 1: Bypass Login**
```
Username: admin' OR '1'='1
Password: anything
```
✅ Result: You're logged in without the password!

**Attack 2: Comment Bypass**
```
Username: admin'--
Password: anything
```
✅ Result: Password check is skipped!

**Attack 3: Get All Users**
```
Username: ' OR 1=1 --
Password: anything
```
✅ Result: Returns first user in database!

---

### On the GREEN "Secure" Form:

**Try the same attacks:**
- ❌ All attacks fail
- ✅ The app is protected

---

## 📊 What's Happening?

### Vulnerable Code:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
# Input is inserted directly - DANGEROUS! 🚨
```

### Secure Code:
```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
# Input is treated as data only - SAFE! ✅
```

---

## 🔑 Key Takeaway

**ALWAYS use `?` placeholders (parameterized queries)**

Never use:
- ❌ f-strings: `f"SELECT * FROM users WHERE id = {id}"`
- ❌ Concatenation: `"SELECT * FROM users WHERE id = " + id`
- ❌ Format: `"SELECT * FROM users WHERE id = %s" % id`

Always use:
- ✅ Placeholders: `cursor.execute("SELECT * FROM users WHERE id = ?", (id,))`


## ⚠️ Remember

This is for **learning only**! Never use vulnerable code in production.
