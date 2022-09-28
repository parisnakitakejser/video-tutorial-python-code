from flask import Flask
import requests
import os
import logging

logging.info(f'ENV LB 1: {os.getenv("LB_ONE_DNS_NAME")}')
logging.info(f'ENV LB 2: {os.getenv("LB_TWO_DNS_NAME")}')

app = Flask(__name__)


def request_session_get(url: str):
    req = requests.Session()

    try:
        resp = req.get(
            f"http://{url}",
            timeout=3,
        )
        data = resp.text
    except Exception as e:
        data = e

    return data


def request_get(url: str):
    try:
        resp = requests.get(
            f"http://{url}",
            timeout=3,
        )
        data = resp.text
    except Exception as e:
        data = e

    return data


@app.route("/")
def home():
    return """
    <h1>ECS Cluster - Public NAT !</h1>

    <strong>requests.Session()</strong>
    <ul>
        <li><a href="/vpc-one-session">Check VPC Peering working NAT Public => VPC One</a></li>
        <li><a href="/vpc-two-session">Check VPC Peering failed NAT Public => VPC Two</a></li>
        <li><a href="/vpc-both-session">Check VPC Peering works and failed NAT Public => VPC One & Two</a></li>
    </ul>

    <strong>requests.get</strong>
    <ul>
        <li><a href="/vpc-one-request">Check VPC Peering working NAT Public => VPC One</a></li>
        <li><a href="/vpc-two-request">Check VPC Peering failed NAT Public => VPC Two</a></li>
        <li><a href="/vpc-both-request">Check VPC Peering works and failed NAT Public => VPC One & Two</a></li>
    </ul>
    """


@app.route("/vpc-one-session")
def vpc_one_sessions():
    return f"""
    <h1>Public NAT => VPC One</h1>
    Private LB 1 - Connection testing: {request_session_get(os.getenv("LB_ONE_DNS_NAME"))}<br />
    Private LB 2 - Connection testing: N/A<br />
    """


@app.route("/vpc-two-session")
def vpc_two_sessions():
    return f"""
    <h1>Public NAT => VPC Two</h1>
    Private LB 1 - Connection testing: N/A<br />
    Private LB 2 - Connection testing: {request_session_get(os.getenv("LB_TWO_DNS_NAME"))}<br />
    """


@app.route("/vpc-both-session")
def vpc_both_sessions():
    return f"""
    <h1>Public NAT => Both VPC One & Two</h1>
    Private LB 1 - Connection testing: {request_session_get(os.getenv("LB_ONE_DNS_NAME"))}<br />
    Private LB 2 - Connection testing: {request_session_get(os.getenv("LB_TWO_DNS_NAME"))}<br />
    """


@app.route("/vpc-one-request")
def vpc_one_request():
    return f"""
    <h1>Public NAT => VPC One</h1>
    Private LB 1 - Connection testing: {request_get(os.getenv("LB_ONE_DNS_NAME"))}<br />
    Private LB 2 - Connection testing: N/A<br />
    """


@app.route("/vpc-two-request")
def vpc_two_request():
    return f"""
    <h1>Public NAT => VPC Two</h1>
    Private LB 1 - Connection testing: N/A<br />
    Private LB 2 - Connection testing: {request_get(os.getenv("LB_TWO_DNS_NAME"))}<br />
    """


@app.route("/vpc-both-request")
def vpc_both_request():
    return f"""
    <h1>Public NAT => Both VPC One & Two</h1>
    Private LB 1 - Connection testing: {request_get(os.getenv("LB_ONE_DNS_NAME"))}<br />
    Private LB 2 - Connection testing: {request_get(os.getenv("LB_TWO_DNS_NAME"))}<br />
    """


@app.route("/health_check")
def health_check():
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
