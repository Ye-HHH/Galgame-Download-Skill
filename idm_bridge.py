"""
IDM COM Bridge — send download tasks to Internet Download Manager.
Pure mechanical bridge, no AI logic here.
"""
import sys
import comtypes.client
from comtypes.client import GetModule
from pathlib import Path

_TLB_PATH = Path("C:/Program Files (x86)/Internet Download Manager/idmantypeinfo.tlb")
_TLB_LOADED = False


def _ensure_tlb():
    global _TLB_LOADED
    if not _TLB_LOADED:
        GetModule(str(_TLB_PATH))
        _TLB_LOADED = True


def send(url: str, referer: str = "", path: str = "", filename: str = "",
         cookie: str = "", silent: bool = True) -> bool:
    """
    Send a download to IDM via COM API.

    Returns True on success, False on failure.
    """
    _ensure_tlb()
    from comtypes.gen import IDManLib

    if not path:
        path = str(Path.home() / "Downloads")

    flag = 1 if silent else 0

    try:
        idm = comtypes.client.CreateObject(
            "IDMan.CIDMLinkTransmitter",
            interface=IDManLib.ICIDMLinkTransmitter
        )
        result = idm.SendLinkToIDM(url, referer, cookie, "", "", "", path, filename, flag)
        return result == 0
    except Exception as e:
        print(f"[idm_bridge] COM error: {e}", file=sys.stderr)
        return False


def send_batch(links: list[dict], referer: str = "", silent: bool = True) -> int:
    """
    Send multiple downloads to IDM. Each dict: {url, filename, path, cookie}
    Returns count of successfully queued downloads.
    """
    success = 0
    for link in links:
        if send(
            url=link["url"],
            referer=referer,
            path=link.get("path", ""),
            filename=link.get("filename", ""),
            cookie=link.get("cookie", ""),
            silent=silent
        ):
            success += 1
    return success


if __name__ == "__main__":
    silent = "--silent" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    url = args[0] if len(args) > 0 else ""
    referer = args[1] if len(args) > 1 else ""
    path = args[2] if len(args) > 2 else ""
    filename = args[3] if len(args) > 3 else ""

    if not url:
        print("Usage: python idm_bridge.py <url> [referer] [path] [filename] [--silent]")
        sys.exit(1)

    ok = send(url, referer, path, filename, silent=silent)
    mode = "silent" if silent else "normal"
    print(f"IDM [{mode}]: {'OK' if ok else 'FAILED'}")
    sys.exit(0 if ok else 1)