import shutil
import os
import time
import argparse

def perform_backup(source, destination):
    try:
        if os.path.exists(destination):
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copytree(source, destination)
        print("Backup completed successfully!")
        return True
    except Exception as e:
        print(f"Error performing backup: {e}")
        return False

def create_log(message, log_path, log_level="INFO"):
    try:
        with open(log_path, "a") as log_file:
            log_file.write(f"{time.ctime()} [{log_level}] - {message}\n")
        print(f"[{log_level}] {message}")
    except Exception as e:
        print(f"Error creating log: {e}")

def perform_backup_and_log(source, destination, log_folder):
    log_path = os.path.join(log_folder, "backup_log.txt")
    if perform_backup(source, destination):
        create_log(f"Backup from {source} to {destination} completed successfully.", log_path)
        cleanup_destination(source, destination, log_folder)
    else:
        create_log(f"Failed to perform backup from {source} to {destination}.", log_path, "ERROR")

def run_backup(source, destination, frequency_minutes, log_folder):
    log_path = os.path.join(log_folder, "backup_log.txt")
    while True:
        perform_backup_and_log(source, destination, log_folder)
        time.sleep(frequency_minutes * 60)

def cleanup_destination(source, destination, log_folder):
    try:
        for root_dir, dirs, files in os.walk(destination, topdown=False):
            for item in files:
                item_path = os.path.join(root_dir, item)
                relative_path = os.path.relpath(item_path, destination)
                source_item_path = os.path.join(source, relative_path)
                if not os.path.exists(source_item_path):
                    os.remove(item_path)
                    create_log(f"Removed file '{relative_path}' from the destination folder.", os.path.join(log_folder, "backup_log.txt"), "INFO")
            for item in dirs:
                item_path = os.path.join(root_dir, item)
                relative_path = os.path.relpath(item_path, destination)
                source_item_path = os.path.join(source, relative_path)
                if not os.path.exists(source_item_path):
                    shutil.rmtree(item_path)
                    create_log(f"Removed directory '{relative_path}' from the destination folder.", os.path.join(log_folder, "backup_log.txt"), "INFO")
    except Exception as e:
        create_log(f"Error cleaning up destination folder: {e}", os.path.join(log_folder, "backup_log.txt"), "ERROR")

def main():
    parser = argparse.ArgumentParser(description="Backup Program")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("destination", help="Destination folder path")
    parser.add_argument("frequency_minutes", type=int, help="Synchronization interval in minutes")
    parser.add_argument("log_folder", help="Log file folder path")
    args = parser.parse_args()

    run_backup(args.source, args.destination, args.frequency_minutes, args.log_folder)

if __name__ == "__main__":
    main()
