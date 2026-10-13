from flask import Flask, request
import security_engine as sec
import smtplib

app = Flask(__name__)

# Store login attempts for each IP address
attempts = {}


# =========================================================
# EMAIL ALERT FUNCTION
# =========================================================

def send_alert(ip, victim_email, attempt_count):

    admin_email = "bixguardx@gmail.com"

    # IMPORTANT:
    # Do NOT put your real Gmail App Password in GitHub.
    # Replace this temporarily with your NEW app password
    # or preferably use an environment variable.
    gmail_app_password = "YOUR_NEW_APP_PASSWORD"

    subject = "BixGuardX Alert: Brute Force Attack Detected"

    message = f"""Subject: {subject}
From: {admin_email}
To: {admin_email}, {victim_email}

Security Alert - BixGuardX

A possible brute-force login attack has been detected.

IP Address: {ip}
Target Email: {victim_email}
Attempt Number: {attempt_count}

Action Taken:
The suspicious IP address has been sent to the BixGuardX
security engine for blocking.

If this login attempt was not made by you, please secure
your account and contact the administrator.

BixGuardX
Adaptive Cybersecurity System
"""

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(admin_email, gmail_app_password)

        # Send alert to administrator
        # and the person whose email was targeted
        recipients = [admin_email]

        if "@" in victim_email:
            if victim_email.lower() != admin_email.lower():
                recipients.append(victim_email)

        server.sendmail(
            admin_email,
            recipients,
            message
        )

        server.quit()

        print("Email alert sent successfully.")
        print("Alert recipients:", recipients)

    except Exception as e:

        print("Email failed:", e)


# =========================================================
# LOGIN PAGE
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # Get IP address of the machine making the request
    ip = request.remote_addr

    # -----------------------------------------------------
    # POST = User submitted login form
    # -----------------------------------------------------

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Count attempts for this IP
        attempts[ip] = attempts.get(ip, 0) + 1

        current_attempt = attempts[ip]

        print("----------------------------------------")
        print("BixGuardX Login Attempt")
        print("IP Address:", ip)
        print("Target Email:", email)
        print("Attempt Number:", current_attempt)
        print("----------------------------------------")

        # -------------------------------------------------
        # Send attack information to security engine
        # -------------------------------------------------

        try:

            sec.record_attack(
                ip,
                email,
                current_attempt,
                "Web Login"
            )

            print("Security engine updated successfully.")

        except Exception as e:

            print("Security engine error:", e)

        # -------------------------------------------------
        # Send email alert
        # -------------------------------------------------

        send_alert(
            ip,
            email,
            current_attempt
        )

        # -------------------------------------------------
        # Display result to browser
        # -------------------------------------------------

        return f"""
        <!DOCTYPE html>

        <html>

        <head>
            <title>BixGuardX Security Alert</title>
        </head>

        <body>

            <h2>BixGuardX Secure Login</h2>

            <h3>Login Failed</h3>

            <p>
                Wrong password attempt detected.
            </p>

            <p>
                Attempt Number:
                <strong>{current_attempt}</strong>
            </p>

            <p>
                IP Address:
                <strong>{ip}</strong>
            </p>

            <p>
                The activity has been recorded by
                BixGuardX.
            </p>

            <br>

            <a href="/login">
                Try Again
            </a>

        </body>

        </html>
        """

    # -----------------------------------------------------
    # GET = Display login page
    # -----------------------------------------------------

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>BixGuardX Secure Login</title>

    </head>

    <body>

        <h2>BixGuardX Secure Login</h2>

        <p>
            Enterprise Web Login Protection
        </p>

        <form method="POST">

            <label>Email:</label>
            <br>

            <input
                type="email"
                name="email"
                required
            >

            <br>
            <br>

            <label>Password:</label>
            <br>

            <input
                type="password"
                name="password"
                required
            >

            <br>
            <br>

            <input
                type="submit"
                value="Login"
            >

        </form>

    </body>

    </html>
    """


# =========================================================
# START FLASK SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5050,
        debug=False
    )



































































