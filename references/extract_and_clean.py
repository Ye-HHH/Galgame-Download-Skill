"""
Extract archive to target directory, then delete the archive on success.

Supports: .7z, .rar, .zip, .lz4 (decrypt first), .tar, .tar.gz

Usage:
  python extract_and_clean.py <archive_path> <output_dir> [--password PWD] [--keep]

  --keep       Don't delete the archive after extraction
  --password   Archive password (for encrypted archives)
  --dry-run    Show what would happen without doing it
"""
import os
import re
import sys
import shutil
import subprocess
from pathlib import Path

# Known ad/junk files to clean up after extraction
JUNK_PATTERNS = [
    r'^.*\.url$',                    # Windows shortcut files
    r'^.*广告.*$',                    # Ad files
    r'^.*推广.*$',
    r'^.*免责声明.*$',
    r'^Thumbs\.db$',
    r'^\.DS_Store$',
    r'^__MACOSX$',
    r'^.*\.txt$',                    # Often ad text files, but could be readme
]


def find_7z() -> str | None:
    """Find 7z.exe on the system."""
    candidates = [
        "C:/Program Files/7-Zip/7z.exe",
        "C:/Program Files (x86)/7-Zip/7z.exe",
        "C:/Program Files/NVIDIA Corporation/NVIDIA app/7z.exe",
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    # Try PATH
    for d in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(d, '7z.exe')
        if os.path.isfile(p):
            return p
    # Try where
    try:
        result = subprocess.run(['where', '7z'], capture_output=True, text=True, shell=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')[0].strip()
    except Exception:
        pass
    return None


def get_ext(archive_path: str) -> str:
    """Get the actual file extension (handle .tar.gz, .7z.001 etc)."""
    name = os.path.basename(archive_path).lower()
    if name.endswith('.tar.gz'):
        return '.tar.gz'
    if name.endswith('.tar.xz'):
        return '.tar.xz'
    # .7z.001 → .7z
    if re.search(r'\.7z\.\d{3}$', name):
        return '.7z'
    if re.search(r'\.rar\.\d{3}$', name):
        return '.rar'
    return os.path.splitext(name)[1]


def is_multipart(archive_path: str) -> bool:
    """Check if this is a multipart archive (.7z.001, .rar.001, etc)."""
    name = os.path.basename(archive_path).lower()
    return bool(re.search(r'\.(7z|rar)\.001$', name))


def delete_file(path: str):
    """Delete a single file."""
    try:
        os.remove(path)
        print(f"  Deleted: {os.path.basename(path)}")
    except OSError as e:
        print(f"  Failed to delete {path}: {e}")


def delete_multipart(base_path: str, ext: str):
    """Delete all parts of a multipart archive."""
    name = os.path.basename(base_path)
    base_name = re.sub(r'\.001$', '', name)
    parent = os.path.dirname(base_path)
    for f in sorted(os.listdir(parent)):
        if f.startswith(base_name) and re.search(rf'\.\d{{3}}$', f):
            fp = os.path.join(parent, f)
            try:
                os.remove(fp)
                print(f"  Deleted: {f}")
            except OSError as e:
                print(f"  Failed to delete {fp}: {e}")


def extract(archive_path: str, output_dir: str, password: str = '') -> bool:
    """Extract archive. Returns True on success."""
    seven_zip = find_7z()
    ext = get_ext(archive_path)

    os.makedirs(output_dir, exist_ok=True)

    # Handle lz4
    if ext == '.lz4':
        return _extract_lz4(archive_path, output_dir)

    if not seven_zip:
        print("ERROR: 7z.exe not found. Cannot extract.")
        return False

    # Build 7z command
    cmd = [seven_zip, 'x', archive_path, f'-o{output_dir}', '-y']
    if password:
        cmd.append(f'-p{password}')
    else:
        cmd.append('-p-')  # No password

    print(f"  Extract: {os.path.basename(archive_path)}")
    print(f"  → {output_dir}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if result.returncode == 0:
            print("  [OK] Extraction OK")
            return True
        else:
            # If -p- failed, retry without password flag (might have no password)
            if not password and 'Wrong password' not in result.stderr:
                cmd2 = [seven_zip, 'x', archive_path, f'-o{output_dir}', '-y']
                result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=3600)
                if result2.returncode == 0:
                    print("  [OK] Extraction OK (no password)")
                    return True

            stderr = result.stderr[-500:] if len(result.stderr) > 500 else result.stderr
            print(f"  [FAIL] Extraction failed: {stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("  [FAIL] Extraction timed out (>1 hour)")
        return False


def _extract_lz4(archive_path: str, output_dir: str) -> bool:
    """Decrypt lz4 then extract."""
    print("  [!] lz4 encrypted archive — decrypting first")
    # lz4 files: first decrypt with lz4 tool, then extract with 7z
    # qingju.org format: lz4 decrypt → .7z → extract
    decrypted = archive_path.replace('.lz4', '.7z')
    if os.path.exists(decrypted):
        os.remove(decrypted)

    try:
        # Try lz4 command line tool
        result = subprocess.run(
            ['lz4', '-d', archive_path, decrypted],
            capture_output=True, text=True, timeout=600
        )
        if result.returncode != 0:
            print(f"  lz4 decrypt failed: {result.stderr}")
            return False

        print("  lz4 decrypted, extracting...")
        return extract(decrypted, output_dir)
    except FileNotFoundError:
        print("  lz4 tool not found. Install lz4 or use qingju tutorial.")
        return False


def cleanup_junk(extracted_dir: str):
    """Remove known junk files from extracted directory."""
    for root, dirs, files in os.walk(extracted_dir):
        for d in dirs[:]:
            for pattern in JUNK_PATTERNS:
                if re.match(pattern, d, re.IGNORECASE):
                    fp = os.path.join(root, d)
                    shutil.rmtree(fp, ignore_errors=True)
                    print(f"  Cleaned: {d}/")
                    dirs.remove(d)
                    break
        for f in files:
            for pattern in JUNK_PATTERNS:
                if re.match(pattern, f, re.IGNORECASE):
                    fp = os.path.join(root, f)
                    try:
                        os.chmod(fp, 0o666)
                        os.remove(fp)
                        print(f"  Cleaned: {f}")
                    except Exception:
                        pass
                    break


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = set(a for a in sys.argv[1:] if a.startswith('--'))

    if len(args) < 2:
        print("Usage: python extract_and_clean.py <archive> <output_dir> [--password PWD] [--keep] [--dry-run]")
        sys.exit(2)

    archive = args[0]
    output_dir = args[1]

    password = ''
    for f in flags:
        if f.startswith('--password='):
            password = f.split('=', 1)[1]
        elif f == '--password' and len(args) > 2:
            password = args[2]

    keep = '--keep' in flags
    dry_run = '--dry-run' in flags

    if not os.path.isfile(archive):
        print(f"ERROR: Archive not found: {archive}")
        sys.exit(1)

    ext = get_ext(archive)
    multipart = is_multipart(archive)

    print(f"Archive: {archive}")
    print(f"Output:  {output_dir}")
    print(f"Type:    {ext}" + (" (multipart)" if multipart else ""))
    if password:
        print(f"Password: {password}")
    print()

    if dry_run:
        print("[DRY RUN] Would extract and" + ("" if keep else " delete") + " archive.")
        return

    # Extract
    ok = extract(archive, output_dir, password)
    if not ok:
        print("Extraction failed — archive kept.")
        sys.exit(1)

    # Clean up junk files
    cleanup_junk(output_dir)

    # Delete archive
    if not keep:
        if multipart:
            delete_multipart(archive, ext)
        else:
            delete_file(archive)

    print("Done.")


if __name__ == '__main__':
    main()
