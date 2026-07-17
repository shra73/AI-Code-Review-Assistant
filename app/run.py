from app import create_app  # or wherever your Flask app is

app = create_app()

if __name__ == "__main__":
    app.run(
    debug=True,
    extra_files=[],
    use_reloader=False
)
