"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        starred_only = request.args.get("filter") == "starred"
        notes = [n for n in app.notes if n.get("starred", False)] if starred_only else app.notes
        return render_template("home.html", notes=notes, show_starred=starred_only)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            # TASK 01 will add validation here.
            app.notes.append({"title": title, "body": body, "starred": False})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    @app.route("/notes/<int:idx>/star", methods=["POST"])
    def toggle_star(idx: int):
        """Toggle the starred state of note at position idx.

        Silently ignores out-of-range indices. Uses .get() so notes created
        before this feature was added (missing the 'starred' key) are treated
        as unstarred rather than raising a KeyError.
        """
        if 0 <= idx < len(app.notes):
            app.notes[idx]["starred"] = not app.notes[idx].get("starred", False)
        return redirect(url_for("home"))

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
