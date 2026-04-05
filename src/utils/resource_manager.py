import psutil
import shutil
import os
import logging

logger = logging.getLogger(__name__)

class ResourceManager:
    @staticmethod
    def get_resource_status():
        mem = psutil.virtual_memory()
        disk = shutil.disk_usage("/")
        
        status = {
            "ram_total_gb": round(mem.total / (1024**3), 2),
            "ram_available_gb": round(mem.available / (1024**3), 2),
            "ram_percent": mem.percent,
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_available_gb": round(disk.free / (1024**3), 2),
            "disk_percent": round((disk.used / disk.total) * 100, 2)
        }
        return status

    @staticmethod
    def check_safety(min_ram_gb=0.5, min_disk_gb=1.0):
        status = ResourceManager.get_resource_status()
        if status["ram_available_gb"] < min_ram_gb:
            return False, f"Insufficient RAM: {status["ram_available_gb"]}GB"
        if status["disk_available_gb"] < min_disk_gb:
            return False, f"Insufficient Disk: {status["disk_available_gb"]}GB"
        return True, "Safe"
