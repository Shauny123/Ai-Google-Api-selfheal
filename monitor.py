import requests
import time

def monitor_service():
    url = "$(gcloud run services describe byword-intake-api --region=us-central1 --format='value(status.url)')"
    while True:
        try:
            response = requests.get(f"{url}/health", timeout=10)
            if response.status_code == 200:
                print("✅ Service healthy")
            else:
                print(f"⚠️ Service issue: {response.status_code}")
        except Exception as e:
            print(f"❌ Service down: {e}")
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    monitor_service()
