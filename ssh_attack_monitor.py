import subprocess
import security_engine as sec

attempts={}

print("BixGuardX SSH Monitor Started...")

process = subprocess.Popen(
    ["journalctl","-u","ssh","-f"],
    stdout=subprocess.PIPE,
    text=True
)

for line in process.stdout:

    if "Failed password" in line:

        try:
            ip=line.split("from")[1].split()[0]

            attempts[ip]=attempts.get(ip,0)+1

            sec.record_attack(ip,"SSH Login",attempts[ip],"SSH")

            print(f"SSH attack detected from {ip} attempt {attempts[ip]}")

        except:
            pass
