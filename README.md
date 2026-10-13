# BixGuardX

**Next-Generation Adaptive Cybersecurity Architecture for Safeguarding Enterprise Business Operations Across Distributed Network Environments**

## About the Project

BixGuardX is a cybersecurity prototype designed to detect and prevent brute-force login attacks against web and SSH services. It monitors repeated failed login attempts, records suspicious activity, applies IP-blocking rules using Linux `iptables`, and presents security events through a Flask dashboard.

## Features

- Web login attack monitoring
- SSH authentication failure monitoring
- IP-based blocking using Linux firewall rules
- Email alerts for suspicious login activity
- Security event dashboard
- Manual and automatic IP unblocking

## Technologies Used

- Python
- Flask
- SQLite
- Linux
- iptables
- SSH
- SMTP

## Project Workflow

1. Monitor login activity.
2. Detect repeated failed login attempts.
3. Record suspicious activity.
4. Apply firewall rules when configured thresholds are reached.
5. Notify the administrator and display events on the dashboard.
6. Allow authorized administrators to review and unblock IP addresses.

## Running the Project

Clone this repository, create a Python virtual environment, install the required dependencies, configure email credentials securely using environment variables, and run the relevant monitoring and dashboard scripts.

See the project source code for implementation details.

## Limitations

This is a prototype. Its effectiveness depends on correct firewall configuration, authentication-log access, and integration between modules. IP changes, VPNs, distributed attacks, and false positives require additional safeguards.

## Disclaimer

Use this project only on systems and networks you own or are authorized to test.
