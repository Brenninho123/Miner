import os
import platform
import psutil

def get_scan_paths():
    system = platform.system()
    paths = []

    if system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        localappdata = os.environ.get("LOCALAPPDATA", "")
        temp = os.environ.get("TEMP", "")
        systemroot = os.environ.get("SYSTEMROOT", "C:\\Windows")
        paths = [
            appdata,
            localappdata,
            temp,
            os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup"),
            os.path.join(systemroot, "System32", "Tasks"),
            os.path.join(systemroot, "Temp"),
        ]
    elif system == "Darwin":
        home = os.path.expanduser("~")
        paths = [
            "/tmp",
            "/Library/LaunchAgents",
            "/Library/LaunchDaemons",
            os.path.join(home, "Library", "LaunchAgents"),
            os.path.join(home, "Library", "Application Support"),
        ]
    else:
        home = os.path.expanduser("~")
        paths = [
            "/tmp",
            "/var/tmp",
            os.path.join(home, ".config", "autostart"),
            "/etc/systemd/system",
            "/etc/cron.d",
        ]

    return [p for p in paths if p and os.path.exists(p)]

def get_heavy_processes(cpu_threshold=50.0, mem_threshold=500):
    heavy = []
    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            cpu = proc.cpu_percent(interval=0.1)
            mem = proc.memory_info().rss / (1024 * 1024)
            if cpu >= cpu_threshold or mem >= mem_threshold:
                heavy.append({
                    "pid": proc.info["pid"],
                    "name": proc.info["name"],
                    "exe": proc.info["exe"],
                    "cpu_percent": cpu,
                    "memory_mb": round(mem, 2)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return heavy

def get_gpu_intensive_processes():
    try:
        import subprocess
        result = subprocess.run(
            ["nvidia-smi", "--query-compute-apps=pid,used_memory", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return []
        processes = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            pid_str, mem_str = line.split(", ")
            processes.append({"pid": int(pid_str), "gpu_memory": mem_str})
        return processes
    except (FileNotFoundError, subproc
