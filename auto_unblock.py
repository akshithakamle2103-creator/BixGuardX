import time
import sqlite3
import subprocess
from datetime import datetime

while True:

    conn = sqlite3.connect("bixguardx.db")
    c = conn.cursor()

    rows = c.execute("SELECT ip, block_time, timestamp FROM attacks").fetchall()

    for ip, block_time, timestamp in rows:

        start = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()

        seconds = (now - start).total_seconds()

        if block_time == "15 minutes" and seconds > 900:
            subprocess.run(["iptables","-D","INPUT","-s",ip,"-j","DROP"])
            c.execute("DELETE FROM attacks WHERE ip=?", (ip,))

        elif block_time == "30 minutes" and seconds > 1800:
            subprocess.run(["iptables","-D","INPUT","-s",ip,"-j","DROP"])
            c.execute("DELETE FROM attacks WHERE ip=?", (ip,))

        elif block_time == "1 hour" and seconds > 3600:
            subprocess.run(["iptables","-D","INPUT","-s",ip,"-j","DROP"])
            c.execute("DELETE FROM attacks WHERE ip=?", (ip,))

    conn.commit()
    conn.close()

    time.sleep(10)  # check every 10 seconds
