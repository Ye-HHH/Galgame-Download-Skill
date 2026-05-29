"""
Wait for a download to complete by polling file size.

Usage:
  python wait_download.py <file_path> <expected_size> [--interval SEC] [--timeout SEC]

Expected size can be:
  - Bytes (integer): 3758096384
  - Human-readable: "3.5 GB", "1.2 GB", "500 MB"

Exits 0 when done, 1 on timeout.
"""
import os
import sys
import time


def parse_size(s: str) -> int:
    """Parse human-readable size to bytes. '3.5 GB' -> 3758096384"""
    s = s.strip()
    # Try pure integer first
    try:
        return int(s)
    except ValueError:
        pass

    units = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3, 'TB': 1024 ** 4}
    upper = s.upper().replace(' ', '')
    for unit, mult in sorted(units.items(), key=lambda x: -len(x[0])):
        if upper.endswith(unit):
            num = float(upper[:-len(unit)])
            return int(num * mult)
    raise ValueError(f"Cannot parse size: {s}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]

    if len(args) < 2:
        print("Usage: python wait_download.py <file_path> <expected_size> [--interval SEC] [--timeout SEC]")
        sys.exit(2)

    file_path = args[0]
    expected = parse_size(args[1])

    interval = 30
    timeout = 7200  # 2 hours

    for f in flags:
        if f.startswith('--interval='):
            interval = int(f.split('=')[1])
        elif f.startswith('--timeout='):
            timeout = int(f.split('=')[1])

    print(f"Waiting for: {file_path}")
    print(f"Expected: {expected} bytes ({expected / 1024**3:.1f} GB)")
    print(f"Poll every {interval}s, timeout {timeout}s")
    print()

    elapsed = 0
    while elapsed < timeout:
        try:
            size = os.path.getsize(file_path)
        except OSError:
            size = 0

        if size >= expected:
            print(f"DONE: {size} bytes >= {expected} bytes")
            sys.exit(0)

        pct = (size * 100 // expected) if expected > 0 else 0
        print(f"[{elapsed}s] {size:,} / {expected:,} bytes ({pct}%)")
        time.sleep(interval)
        elapsed += interval

    try:
        size = os.path.getsize(file_path)
    except OSError:
        size = 0
    print(f"TIMEOUT after {elapsed}s. Final size: {size:,} bytes")
    sys.exit(1)


if __name__ == '__main__':
    main()
