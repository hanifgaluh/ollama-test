import requests

API_URL = "https://worthy-drunk-dude-stevens.trycloudflare.com/chat"

def kirim_prompt(prompt: str):
    payload = {
        "prompt": prompt
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()

        data = response.json()
        print("\nJawaban server:")
        print(data.get("response", "Tidak ada response"))

    except requests.exceptions.HTTPError:
        try:
            print("HTTP Error:", response.json())
        except Exception:
            print("HTTP Error:", response.text)
    except requests.exceptions.ConnectionError:
        print("Gagal terhubung ke server.")
    except requests.exceptions.Timeout:
        print("Request timeout.")
    except requests.exceptions.RequestException as e:
        print("Terjadi error:", e)


def main():
    print("=== Client Chat Ollama ===")
    print("Ketik 'exit' untuk keluar.\n")

    while True:
        prompt = input("Masukkan prompt: ").strip()

        if prompt.lower() == "exit":
            print("Program selesai.")
            break

        if not prompt:
            print("Prompt tidak boleh kosong.\n")
            continue

        kirim_prompt(prompt)
        print()


if __name__ == "__main__":
    main()