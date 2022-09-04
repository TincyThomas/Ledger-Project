import sqlite3 as sql
from flask import Flask, render_template, request

app = Flask(__name__)
conn = sql.connect('database.db')
cursor = conn.cursor()

#cursor.execute('DROP TABLE header_creation')
#command1 = """CREATE TABLE IF NOT EXISTS
#header_creation (Receipt_Number INTEGER PRIMARY KEY AUTOINCREMENT, Header_Name CHARACTER(30))"""
#cursor.execute(command1)

@app.route("/")
@app.route("/finalhtml")
def home():
    return render_template('finalhtml.html')

@app.route('/delete/<id>')
def delete_entry(id):
    conn = sql.connect('database.db')
    sqll = 'DELETE FROM header_creation WHERE Header_Name=?'
    cur = conn.cursor()
    cur.execute(sqll, (id,))
    conn.commit()
    return render_template('success.html')

@app.route('/incomeview')
def income_output():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM income_receipt_entry')
    t = cur.fetchall()
    return render_template("incomeview.html", rows=t)


@app.route('/expenseview')
def expense_output():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM expense_voucher_entry')
    t = cur.fetchall()
    return render_template("expenseview.html", rows=t)

@app.route('/viewheader')
def header_output():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT Header_Name FROM header_creation')
    t = cur.fetchall()
    return render_template("viewheader.html", rows=t)


@app.route('/incomeentry')
def income_input():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    t = cur.execute('SELECT Header_Name FROM header_creation').fetchall()
    r = cur.execute('SELECT * FROM income_receipt_entry ORDER BY Receipt_Number DESC LIMIT 1').fetchall()
    return render_template('incomeentry.html', rows=t, last=r)


@app.route('/saveincomeentry', methods=["POST", "GET"])
def save_income_input():
    msg = "msg"
    if request.method == "POST":
        try:
            head = request.form["hn"]
            rece = request.form["rn"]
            amou = request.form["am"]
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO income_receipt_entry (Date,Header_Name,Name,Amount) VALUES (datetime('now'),'{}', '{}', '{}')".format(
                        head, rece, int(amou)))
                con.commit()
                msg = "Data successfully Added"
        except:
            con.rollback()
            msg = "We can not add transaction to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route('/expenseentry')
def expense_input():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    t = cur.execute('SELECT Header_Name FROM header_creation').fetchall()
    r = cur.execute('SELECT * FROM expense_voucher_entry ORDER BY Receipt_Number DESC LIMIT 2').fetchall()
    return render_template("expenseentry.html", rows=t, last=r)


@app.route('/saveexpenseentry', methods=["POST", "GET"])
def save_expense_input():
    msg = "msg"
    if request.method == "POST":
        try:
            head1 = request.form["hn"]
            rece1 = request.form["rn"]
            amou1 = request.form["am"]
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO expense_voucher_entry (Date,Header_Name,Name,Amount) VALUES (datetime('now'),'{}', '{}', '{}')".format(head1, rece1, int(amou1)))
                con.commit()
                msg = "Data successfully Added"
        except:
            con.rollback()
            msg = "We can not add transaction to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route('/headcreation')
def header_input():
    return render_template('headcreation.html')


@app.route('/saveheadentry', methods=["POST", "GET"])
def save_head_input():
    msg = "msg"
    if request.method == "POST":
        try:
            head = request.form["hn"]
            if head.isalpha() or ' ' in head:
                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO header_creation (Header_Name) VALUES ('{}')".format(head))
                    con.commit()
                    msg = "Data successfully Added"
            else:
                msg = "Header can only be text."
        except:
            con.rollback()
            msg = "We can not add this header to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


if __name__ == '__main__':
    app.run(debug=True)
