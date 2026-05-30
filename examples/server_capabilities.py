"""Inspect server capabilities and posting status."""
from usenet import UsenetServer

# Try several servers to show different capability profiles
SERVERS = [
    "news.eternal-september.org",
    "news.aioe.org",
]

for server_url in SERVERS:
    print(f"\n{'='*60}")
    print(f"Server: {server_url}")
    print('='*60)

    try:
        with UsenetServer(server_url, timeout=5) as server:
            print(f"Welcome message:\n  {server.welcome_message}")
            print(f"\nCan post: {server.can_post}")
            print(f"Alive: {server.alive}")

            if server.capabilities:
                print(f"\nCapabilities:")
                for cap, value in server.capabilities.items():
                    print(f"  {cap}: {value}")
            else:
                print(f"\nCapabilities: (none reported)")

    except Exception as e:
        print(f"Connection failed: {e}")
