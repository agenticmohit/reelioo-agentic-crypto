from flask import Flask, render_template, request, redirect, url_for, session
from agent import agent
import uuid

app = Flask(__name__)
app.secret_key = "reelioo-secret"


@app.route("/")
def index():
    if "thread_id" not in session:
        session["thread_id"] = str(uuid.uuid4())
    if "messages" not in session:
        session["messages"] = []
    return render_template("index.html", messages=session["messages"])


@app.route("/send", methods=["POST"])
def send():
    user_query = request.form["message"]

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_query}]},
        {"configurable": {"thread_id": session["thread_id"]}}
    )

    agent_reply = response["messages"][-1].content
    if isinstance(agent_reply, list):
        agent_reply = agent_reply[0]["text"]

    session["messages"].append({"type": "human", "content": user_query})
    session["messages"].append({"type": "ai",    "content": agent_reply})
    session.modified = True

    return redirect(url_for("index"))


@app.route("/clear")
def clear():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
