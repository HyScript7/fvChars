import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=os.environ.get("FLASK_ENV", "Production").lower().startswith("dev"),
    )
