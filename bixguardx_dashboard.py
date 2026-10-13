from flask import Flask, render_template_string, redirect
import sqlite3
import subprocess
from datetime import datetime

app = Flask(__name__)

DB = "/opt/bixguardx/bixguardx.db"

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>BixGuardX SOC Dashboard</title>
<meta http-equiv="refresh" content="5">

<style>
body{
background:#ffffff;
color:#000;
font-family:Arial;
text-align:center;
}

h1{
color:#007bff;
margin-top:30px;
}

.cards{
display:flex;
justify-content:center;
gap:40px;
margin:40px;
}

.card{
background:#f5f5f5;
padding:25px;
border-radius:10px;
width:220px;
box-shadow:0px 0px 10px #ccc;
}

table{
width:90%;
margin:auto;
border-collapse:collapse;
margin-top:20px;
}

th{
background:#ef4444;
color:white;
padding:10px;
}
 
td{
padding:10px;
border-bottom:1px solid #ddd;
}

.blocked{
color:red;
font-weight:bold;
}

button{
background:#f59e0b;
border:none;
padding:6px 12px;
color:white;
cursor:pointer;
border-radius:5px;
}

button:hover{
background:#d97706;
}
</style>

</head>

<body>

<h1>BixGuardX Security Operations Center</h1>

<div class="cards">

<div class="card">
<h3>Total Attacks</h3>
<h2>{{total}}</h2>
</div>

<div class="card">
<h3>System Status</h3>
<h2>Protected</h2>
</div>

</div>

<table>

<tr>
<th>IP Address</th>
<th>Email Target</th>
<th>Country</th>
<th>Attempts</th>
<th>Block Time</th>
<th>Status</th>
<th>Source</th>
<th>Action</th>
</tr>

{% for row in rows %}
<tr>
<td>{{row[0]}}</td>
<td>{{row[1]}}</td>
<td>{{row[2]}}</td>
<td>{{row[3]}}</td>
<td>{{row[4]}}</td>
<td class="blocked">Blocked</td>
<td>{{row[6]}}</td>

<td>
<a href="/unblock/{{row[0]}}">
<button>Unblock</button>
</a>
</td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""

# ---------------------------
# AUTO UNBLOCK FUNCTION
# ---------------------------

def auto_unblock():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = c.execute(
        "SELECT ip, block_time, timestamp FROM attacks"
    ).fetchall()

    now = datetime.now()

    for ip, block_time, timestamp in rows:

        try:
            start = datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")
        except:
            continue

        seconds = (now - start).total_seconds()

        unblock = False

        if block_time == "15 minutes" and seconds > 900:
            unblock = True

        elif block_time == "30 minutes" and seconds > 1800:
            unblock = True

        elif block_time == "1 hour" and seconds > 3600:
            unblock = True

        if unblock:

            # 🔥 remove ALL rules
            while True:
                result = subprocess.run(
                    ["iptables","-D","INPUT","-s",ip,"-j","DROP"],
                    capture_output=True
                )
                if result.returncode != 0:
                    break

            c.execute("DELETE FROM attacks WHERE ip=?", (ip,))

    conn.commit()
    conn.close()

# ---------------------------
# FETCH DATA
# ---------------------------

def get_data():

    auto_unblock()

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = c.execute(
        "SELECT ip,email,country,attempts,block_time,timestamp,source FROM attacks"
    ).fetchall()

    conn.close()

    return rows

# ---------------------------
# DASHBOARD ROUTE
# ---------------------------

@app.route("/")
def dashboard():

    rows = get_data()
    total = len(rows)

    return render_template_string(
        HTML,
        rows=rows,
        total=total
    )

# ---------------------------
# MANUAL UNBLOCK
# ---------------------------

@app.route("/unblock/<ip>")
def unblock(ip):

    print("Manual Unblock:", ip)

    # 🔥 remove ALL rules (important)
    while True:
        result = subprocess.run(
            ["iptables","-D","INPUT","-s",ip,"-j","DROP"],
            capture_output=True
        )
        if result.returncode != 0:
            break

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("DELETE FROM attacks WHERE ip=?", (ip,))
    conn.commit()
    conn.close()

    return redirect("/")

# ---------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051)
