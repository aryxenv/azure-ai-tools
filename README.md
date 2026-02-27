Experimenting with Azure AI/Foundry Tools

all env vars are managed in global env in main dir, create `.env` in main dir only.

## Face Detection

`./face` contains the face detection

1. navigate to dir

```pwsh
cd ./face
```

2. add to `.env` (under keys & endpoints in your face resource on azure)

```env
FACE_APIKEY="your_face_api_key"
FACE_ENDPOINT="your_face_endpoint"
```

3. install reqs

```pwsh
uv venv
uv pip install -r requirements.txt
```

4. run the face detection test

```pwsh
uv run python ./main.py
```
