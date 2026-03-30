import requests
from azure.identity import DefaultAzureCredential

ENDPOINT = "https://graphrag-foundry-resource.cognitiveservices.azure.com/"
API_VERSION = "2025-10-01-preview"

credential = DefaultAzureCredential()


def translate_text(text, targets):
    token = credential.get_token("https://cognitiveservices.azure.com/.default").token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    url = f"{ENDPOINT}/translator/text/translate?api-version={API_VERSION}"
    body = {"inputs": [{"Text": text, "targets": targets}]}

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def main():
    text = input("Enter text to translate: ")
    targets = [
        {
            "language": "en",
        },
    ]
    try:
        result = translate_text(text, targets)

        for t in result["value"][0]["translations"]:
            print(f"Translation ({t['language']}): {t['text']}")
    except Exception as e:
        print(f"Translation failed: {e}")


if __name__ == "__main__":
    main()
