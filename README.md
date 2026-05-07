AWS DDoS Mitigation & Private Infrastructure Lab

This project demonstrates a full-lifecycle security implementation: building a containerized web application, simulating a Layer 7 DDoS attack, and re-architecting the network to remove all public entry points using AWS PrivateLink and EICE.
---

🛡️ Phase 1: DDoS Defense & WAF Testing
The initial focus of this project was to establish a resilient perimeter using **AWS Web Application Firewall (WAF)**.
Automated Attack Simulation (`test_attack.py`)
To verify the defense, I developed a Python-based stress tester that:
* **Forces New Connections:** Uses `Connection: close` headers to bypass session reuse and force a clean TCP handshake for every request.
* **Validates Rate-Limiting:** Successfully triggers the WAF rate-limit rule, resulting in an automated **403 Forbidden** block once the threshold is crossed.
---

🔐 Phase 2: Eliminating the Attack Surface
Once the perimeter was secured, the architecture was evolved to a **"Zero Public Access"** model. By removing the Internet Gateway and Public IPs, the workload was moved to a completely private subnet.
### Private Connectivity Architecture
Instead of traditional SSH or Bastion hosts, this lab utilizes:
* **EC2 Instance Connect Endpoint (EICE):** Provides a secure, identity-aware tunnel for SSH without needing public IP addresses.
* **VPC Interface Endpoints (PrivateLink):** Allows the private instance to communicate with AWS Systems Manager (SSM) entirely over the internal AWS backbone.

```text
                     [ Public Internet ]
                              │
             ┌────────────────┴────────────────┐
             │       Application Load Balancer  │ ◄── WAF Rate Limiting
             └────────────────┬────────────────┘
                              │
  ============================│============================
  【 Private VPC Environment 】
                              │
    ┌─────────────────────────┼─────────────────────────┐
    │ Private Subnet (No Internet Gateway)              │
    │                                                   │
    │  ┌─────────────────┐             ┌─────────────┐  │
    │  │  Flask App      │◀────────────│  EC2 EICE   │  │
    │  │  (Target Node)  │  Port 22    │  Endpoint   │  │
    │  └────────┬────────┘             └─────────────┘  │
    │           │                                       │
    │           │ (Internal HTTPS 443)                  │
    │           ▼                                       │
    │  ┌─────────────────────────────────────────────┐  │
    │  │ VPC Interface Endpoints                     │  │
    │  │ (ssm, ssmmessages, ec2messages)              │  │
    │  └─────────────────────────────────────────────┘  │
    └───────────────────────────────────────────────────┘
  =========================================================
