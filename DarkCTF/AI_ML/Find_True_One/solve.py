import requests
import time

url = "http://ai2.crack-on.live/api/timeline/verify"
session_id = "your_session_id_here"  # Replace with your actual session ID
# Starting with the user's initial captured timeline
current_timeline = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def get_stats(timeline):
    resp = requests.post(url, json={"session_id": session_id, "timeline": timeline})
    try:
        data = resp.json()
    except ValueError:
        print("[!] Server returned invalid JSON:", resp.text)
        return None, None

    if resp.status_code != 200:
        print(f"[!] Unexpected status code {resp.status_code} (body={data})")

    correct = data.get("correct")
    flag = data.get("flag")

    if correct is None:
        print("[!] Missing 'correct' field in response:", data)

    return correct, flag

current_correct, flag = get_stats(current_timeline)

if current_correct is None:
    raise SystemExit("Failed to retrieve initial 'correct' value. Check the endpoint/session or network.")

for i in range(30):
    if flag:
        break

    current_timeline[i] = 1 - current_timeline[i]  # Flip bit
    new_correct, flag = get_stats(current_timeline)

    if new_correct is None:
        raise SystemExit("Failed to retrieve 'correct' during bit-flip attempt. Stopping.")

    if new_correct > current_correct:
        current_correct = new_correct
        print(f"Bit {i} correct! New accuracy: {current_correct}/30")
    else:
        current_timeline[i] = 1 - current_timeline[i]  # Revert

    time.sleep(0.1)

print(f"Final Flag: {flag}")
