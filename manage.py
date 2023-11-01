import os

from dotenv import load_dotenv

from imagocms.app import create_app


if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    app.run(
        debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5050)
    )
