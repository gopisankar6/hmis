from flask import Flask, render_template, request
import pyodbc
import os

app = Flask(__name__)

# Connection details (use environment variables in production)
server = os.environ.get('DB_SERVER', 'ynh-hmis-db.database.windows.net')
database = os.environ.get('DB_NAME', 'ynh-hmis-db')
username = os.environ.get('DB_USER', 'dbadmin@ynh-hmis-db')  # include @servername
password = os.environ.get('DB_PASS', 'yanbu@2025')
driver = '{ODBC Driver 17 for SQL Server}'

def get_connection():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        try:
            emp_id = int(request.form['id'])
            emp_name = request.form['name']
            emp_age = int(request.form['age'])

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO [ynh-prod-db] (id, name, age) VALUES (?, ?, ?)",
                           (emp_id, emp_name, emp_age))
            conn.commit()
            cursor.close()
            conn.close()
            message = '✅ Employee data saved successfully!'
        except Exception as e:
            message = f'❌ Error: {str(e)}'
    return render_template('form.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
