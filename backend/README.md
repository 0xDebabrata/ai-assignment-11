## Getting Started

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Then, run the development server:

```bash
uvicorn main:app
```

The server should run at [http://localhost:8000](http://localhost:8000).

Ensure that the server is running during local development.
