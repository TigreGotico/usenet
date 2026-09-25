"""Iterate bundled ServerRecord list and inspect fields."""
from usenet import get_known_servers, ServerRecord

print("Known NNTP servers from bundled list\n")

count = 0
for server_record in get_known_servers():
    count += 1

    print(f"Host:      {server_record.host}")
    print(f"  Port:    {server_record.port}")
    if server_record.tls_port:
        print(f"  TLS:     {server_record.tls_port}")
    print(f"  Post:    {server_record.post}")
    print(f"  Auth:    {server_record.auth}")
    if server_record.notes:
        print(f"  Notes:   {server_record.notes}")
    print()

    if count >= 5:  # show first 5 servers
        break

print(f"... and more (use get_known_servers() to iterate all)")
