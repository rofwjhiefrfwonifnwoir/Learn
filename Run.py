import os
import sys

from lightning_sdk import Status, Studio

_TRANSITIONAL = frozenset({Status.Pending, Status.Stopping})


def run():
    studio_name = os.environ.get("LIGHTNING_STUDIO_NAME")
    teamspace = os.environ.get("LIGHTNING_TEAMSPACE")
    user = os.environ.get("LIGHTNING_USERNAME")
    user_id = os.environ.get("LIGHTNING_USER_ID")
    api_key = os.environ.get("LIGHTNING_API_KEY")

    if not all([studio_name, teamspace, user, user_id, api_key]):
        print("ERROR: Missing required environment variables.")
        sys.exit(1)

    try:
        s = Studio(name=studio_name, teamspace=teamspace, user=user, create_ok=False)
        status = s.status
        print("---------------------------------------")
        print("CHECKING STUDIO STATUS...")
        print(f"Current State: {status.value}")
        print("---------------------------------------")
        if status == Status.Running:
            print(">>> STUDIO IS ALIVE. No action needed.")
        elif status in _TRANSITIONAL:
            print(f">>> STUDIO IS {status.value.upper()}. Skipping start.")
        elif status == Status.Stopped:
            print(">>> STUDIO IS DOWN. Sending signal...")
            s.start()
            print(">>> SUCCESS: Wake-up signal.")
        else:
            print(f"ERROR: Studio is in an unstartable state: {status.value}.")
            sys.exit(1)
        print("---------------------------------------")
    except Exception as e:
        print(f"ERROR: failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()