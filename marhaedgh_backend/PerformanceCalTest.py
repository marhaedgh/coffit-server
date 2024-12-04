import asyncio
import aiohttp
import time
from datetime import datetime
import csv
import json

API_URL = "http://localhost:9000/api/v1/infer/chat"
REQUEST_TIMEOUT = 30
NUM_USERS = 10
LOG_FILE = "performance_cal_test_log.csv"
EXIT_FAILURE_THRESHOLD = 5

failure_count = 0
logs = []

def load_basic_prompt():
    path = "/home/guest/marhaedgh/marhaedgh_backend/prompt/chatting.json"
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data


basic_prompt = load_basic_prompt()


async def send_request(session, user_id):
    global failure_count

    question = f"대학교에서 수업을 듣고 싶은데, 나같은 사업자를 위해 제공되는 강의 관련 지원사업이나 정책이 없을까?"
    final_prompt = basic_prompt["content"].format(
        question=question,
        nodes="{nodes}",
        messages=json.dumps([], ensure_ascii=False)
    )

    payload = {
        "question": question,
        "prompt": [{
            "role": "system",
            "content": final_prompt
        }]
    }

    start_time = datetime.now()
    start_timestamp = time.time()

    try:
        async with session.post(
            API_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT
        ) as response:
            if response.status == 200:
                content_length = 0
                ttft = None
                # Wait until the entire response is received
                async for line in response.content:
                    if ttft is None: 
                        ttft = time.time() - start_timestamp
                    content_length += len(line)

                # Calculate TPOT and Latency
                tpot = (time.time() - (start_timestamp - 3)) / content_length
                latency = 3 + (content_length * tpot)

                log_entry = {
                    "request_id": user_id,
                    "request_time": start_time.isoformat(),
                    "duration": time.time() - start_timestamp,
                    "data_length": len(json.dumps(payload)),
                    "output_length": content_length,
                    "ttft": ttft,
                    "tpot": tpot,
                    "latency": latency,
                    "status": "yes",
                    "error": None,
                }
                logs.append(log_entry)
                print(log_entry)
            else:
                failure_count += 1
                log_entry = {
                    "request_id": user_id,
                    "request_time": start_time.isoformat(),
                    "duration": time.time() - start_timestamp,
                    "data_length": len(json.dumps(payload)),
                    "output_length": None,
                    "ttft": None,
                    "tpot": None,
                    "latency": None,
                    "status": "no",
                    "error": f"HTTP {response.status}",
                }
                logs.append(log_entry)
                print(log_entry)

    except asyncio.TimeoutError:
        failure_count += 1
        log_entry = {
            "request_id": user_id,
            "request_time": start_time.isoformat(),
            "duration": time.time() - start_timestamp,
            "data_length": len(json.dumps(payload)),
            "output_length": None,
            "ttft": None,
            "tpot": None,
            "latency": None,
            "status": "no",
            "error": "Timeout",
        }
        logs.append(log_entry)
        print(log_entry)
    except Exception as e:
        failure_count += 1
        log_entry = {
            "request_id": user_id,
            "request_time": start_time.isoformat(),
            "duration": time.time() - start_timestamp,
            "data_length": len(json.dumps(payload)),
            "output_length": None,
            "ttft": None,
            "tpot": None,
            "latency": None,
            "status": "no",
            "error": str(e),
        }
        logs.append(log_entry)
        print(log_entry)


async def stress_test():
    global failure_count
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        tasks = [
            send_request(session, user_id)
            for user_id in range(NUM_USERS)
        ]
        await asyncio.gather(*tasks)


def save_logs_to_csv():
    fieldnames = [
        "request_id", "request_time", "duration", "data_length","output_length",
        "ttft", "tpot", "latency", "status", "error"
    ]
    with open(LOG_FILE, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(logs)
    print(f"Logs saved to {LOG_FILE}")


if __name__ == "__main__":
    try:
        asyncio.run(stress_test())
        if failure_count > EXIT_FAILURE_THRESHOLD:
            print("Too many failures. Exiting...")
    except KeyboardInterrupt:
        print("Stress test interrupted by user.")
    finally:
        save_logs_to_csv()
