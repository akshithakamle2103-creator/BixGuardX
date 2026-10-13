import sqlite3
import datetime
import subprocess

DB = "/opt/bixguardx/bixguardx.db"

def record_attack(ip,email,attempts,source):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    country = "Local"

    if attempts == 1:
        block_time = "15 minutes"
    elif attempts == 2:
        block_time = "30 minutes"
    elif attempts == 3:
        block_time = "1 hour"
    else:
        block_time = "Permanent"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        "INSERT INTO attacks VALUES (?,?,?,?,?,?,?)",
        (ip,email,country,attempts,block_time,timestamp,source)
    )

    conn.commit()
    conn.close()

    # block IP using firewall
    try:
        subprocess.run(["sudo","iptables","-A","INPUT","-s",ip,"-j","DROP"])
    except:
        pass
