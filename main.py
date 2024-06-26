from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, session

import psycopg2
import openai
import time
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
openai.api_key = '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'

conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
mycursor = conn.cursor()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8e3223904ac0df382b253f7f49ec73b7'

db_config = {
   'host': 'localhost',
   'user': 'postgres',
   'password': 'postgres',
   'database': 'colleges',
}


def get_completion(prompt):
    print(prompt)
    query = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    time.sleep(15)
    response = query.choices[0].text
    return response

@app.route('/')
def test():
   return render_template('index.html')
@app.route("/essayhelp", methods=['POST', 'GET'])
def query_view():
    if request.method == 'POST':
        print('step1')
        prompt = request.form['prompt']
        response = get_completion(prompt)
        print(response)

        return jsonify({'response': response})
    return render_template('essayhelp.html')





@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        mycursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = mycursor.fetchone()

        if result and result[0] == password:
            mycursor.execute("SELECT name FROM users WHERE username = %s", (username,))
            session['user_name'] = mycursor.fetchone()[0]
            
            mycursor.execute("SELECT COUNT(*) FROM MyColleges")
            row_count = mycursor.fetchone()[0]
            return render_template('welcome.html', user_name=session['user_name'], row_count=row_count)

        else:
            return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        query = "INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)"
        values = (name, username, email, password)

        mycursor.execute(query, values)
        conn.commit()

        # print(f"User added to the database: {name}, {username}, {email}, {password}")
        # return "Thank you for signing up!"
        return render_template('index.html')

    return render_template('signup.html')

@app.route('/welcome')
def welcome():
    user_name = session.get('user_name')

    if user_name:
        mycursor.execute("SELECT COUNT(*) FROM MyColleges")
        row_count = mycursor.fetchone()[0]
        return render_template('welcome.html', user_name=user_name, row_count=row_count)
    
    else:
        flash('Please log in first.', 'error')
        return redirect(url_for('test'))
    
@app.route('/table')
def table():
   mycursor.execute("SELECT * FROM Colleges")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)




@app.route('/order_by_act')
def order_by_act():
   mycursor.execute("SELECT * FROM Colleges ORDER BY act_avg")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)




@app.route('/order_by_sat')
def order_by_sat():
   mycursor.execute("SELECT * FROM Colleges ORDER BY sat_avg")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)




@app.route('/order_by_class_size')
def order_by_class_size():
   mycursor.execute("SELECT * FROM Colleges ORDER BY enrollment")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)




@app.route('/order_by_acceptance_rate')
def order_by_acceptance_rate():
   mycursor.execute("SELECT * FROM Colleges ORDER BY acceptance_rate")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)




@app.route('/order_by_cost')
def order_by_cost():
   mycursor.execute("SELECT * FROM Colleges ORDER BY cost")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)




@app.route('/order_by_rank')
def order_by_rank():
   mycursor.execute("SELECT * FROM Colleges ORDER BY national_rank")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)




@app.route('/order_by_gpa')
def order_by_gpa():
   mycursor.execute("SELECT * FROM Colleges ORDER BY hs_gpa")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)


@app.route('/save_values', methods=['POST'])
def save_values():
    try:
        data = request.get_json()
        min_value = data['min']
        max_value = data['max']

        if min_value > max_value:
            raise ValueError("Minimum value should not be greater than the maximum value.")

        mycursor = conn.cursor()

        query = "SELECT * FROM Colleges WHERE cost BETWEEN %s AND %s ORDER BY cost"
        mycursor.execute(query, (min_value, max_value))

        data = mycursor.fetchall()
        return jsonify({"data": data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)})

    finally:
        mycursor.close()

@app.route('/save_values_enrollment', methods=['POST'])
def save_values_enrollment():
    try:
        data = request.get_json()
        min_enrollment_value = data['min'];
        max_enrollment_value = data['max'];

        # Check if min_enrollment_value is greater than max_enrollment_value
        if min_enrollment_value > max_enrollment_value:
            raise ValueError("Minimum enrollment should not be greater than the maximum enrollment.")

        mycursor = conn.cursor()

        query = "SELECT * FROM Colleges WHERE enrollment BETWEEN %s AND %s ORDER BY enrollment"
        mycursor.execute(query, (min_enrollment_value, max_enrollment_value))

        data = mycursor.fetchall()
        return jsonify({"data": data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)})

    finally:
        mycursor.close()


@app.route('/filter_by_region', methods=['POST'])
def filter_by_region():
    try:
        data = request.get_json()
        states = data['states']

        mycursor = conn.cursor()

        query = "SELECT * FROM Colleges WHERE state IN %s"
        mycursor.execute(query, (tuple(states),))

        data = mycursor.fetchall()
        return jsonify({"data": data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)})

    finally:
        mycursor.close()

@app.route('/check_pub')
def check_pub():
   mycursor.execute("SELECT * FROM Colleges WHERE Institutional_Control = 'public'")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)


@app.route('/check_priv')
def check_priv():
   mycursor.execute("SELECT * FROM Colleges WHERE Institutional_Control = 'private'")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)


@app.route('/check_prop')
def check_prop():
   mycursor.execute("SELECT * FROM Colleges WHERE Institutional_Control = 'proprietary'")
   data = mycursor.fetchall()
   return render_template('table.html', data=data)

@app.route('/mycolleges')
def mycollege():
   mycursor.execute("SELECT * FROM myColleges")
   data = mycursor.fetchall()
   return render_template('mycolleges.html', data=data)


@app.route('/add_to_mycolleges', methods=['POST'])
def add_to_mycolleges():
    try:
        data = request.get_json()
        college_name = request.json.get('collegeName')
        # Modify this to insert the received data into the MyColleges table
        insert_query = """
            INSERT INTO MyColleges (
                college_name, state, act_avg, sat_avg, enrollment,
                acceptance_rate, cost, percent_receiving_aid,
                national_rank, hs_gpa, institutional_control
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data['collegeName'], data['state'], data['actAvg'], data['satAvg'],
            data['classSize'], data['acceptanceRate'], data['cost'],
            data['percentReceivingAid'], data['nationalRank'], data['hsGPA'],
            data['institutionalControl']
        )

        mycursor.execute(insert_query, values)
        conn.commit()

        return jsonify({"message": f"Added {college_name} to My Colleges successfully"})

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return jsonify({"error": str(e)})


@app.route('/remove_college', methods=['POST'])
def remove_college():
    try:
        college_name = request.json.get('collegeName')

        # Your SQL DELETE query here
        delete_query = "DELETE FROM MyColleges WHERE college_name = %s"
        mycursor = conn.cursor()
        mycursor.execute(delete_query, (college_name,))
        conn.commit()

        # Return a success message
        return jsonify({"message": f"Removed {college_name} from MyColleges"})

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return jsonify({"error": str(e)})

    finally:
        mycursor.close()


if __name__ == '__main__':
    app.run(debug=True)


s = HTMLSession()
app.run(host="127.0.0.1", port=9999, debug=True, threaded=True)