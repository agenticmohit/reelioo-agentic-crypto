import os, uuid
from flask import Flask, render_template, request, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from agent import agent

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-in-prod")

limiter = Limiter(get_remote_address, app=app, default_limits=[])


@app.after_request
def security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.route("/")
def index():
    if "thread_id" not in session:
        session["thread_id"] = str(uuid.uuid4())
    if "messages" not in session:
        session["messages"] = []
    return render_template("index.html", messages=session["messages"])


@app.route("/send", methods=["POST"])
@limiter.limit("20 per minute")
def send():
    """
    Returns IMMEDIATELY — no AI call here.
    Renders the user bubble + a thinking indicator that auto-triggers /think.
    """
    user_query = request.form.get("message", "").strip()
    if not user_query or len(user_query) > 500:
        return "", 204

    session.setdefault("messages", [])
    session["messages"].append({"type": "human", "content": user_query})
    session.modified = True

    return render_template("_thinking.html", user_query=user_query)


@app.route("/think", methods=["POST"])
@limiter.limit("10 per minute")
def think():
    """
    Called automatically by HTMX (hx-trigger="load") on the thinking div.
    Runs the agent and returns just the AI bubble HTML.
    """
    user_query = request.form.get("q", "").strip()
    if not user_query or len(user_query) > 500:
        return "", 204

    thread_id = session.get("thread_id", str(uuid.uuid4()))

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_query}]},
        {"configurable": {"thread_id": thread_id}},
    )

    agent_reply = response["messages"][-1].content
    if isinstance(agent_reply, list):
        agent_reply = agent_reply[0]["text"]

    session.setdefault("messages", [])
    session["messages"].append({"type": "ai", "content": agent_reply})
    session.modified = True

    return render_template("_ai_message.html", content=agent_reply)


@app.route("/clear")
def clear():
    session.clear()
    return "", 204


if __name__ == "__main__":
    app.run(debug=False, port=5000)
