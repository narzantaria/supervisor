import logging
import os
import psutil
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

# Read configuration file and get required data
config = {}
with open("supervisor.cfg", "r") as file:
  for line in file:
    key, value = line.strip().split(": ", 1)
    config[key.strip()] = value.strip()

release_dir = config.get("release_dir", "release")
release_binary = config.get("release_binary", "main")
command = config.get("command", "")
ignore = [item.strip() for item in config.get("ignore", "").split(",")]

'''
Наконец-то сама функция компиляции. Именно она запускается
после всех проверок и триггеров
'''
def compile_handler(command, release_dir, release_binary):
  # Проверяем, запущено ли окно с тем же именем
  for proc in psutil.process_iter(["name"]):
    if proc.info["name"] == release_binary:
      proc.kill()

  # Создаем/очищаем папку release
  if os.path.exists(release_dir):
    for root, dirs, files in os.walk(release_dir):
      for file in files:
        os.remove(os.path.join(root, file))
      for dir in dirs:
        os.rmdir(os.path.join(root, dir))
  else:
    os.makedirs(release_dir)

  # Осуществляем компиляцию
  try:
    retcode = subprocess.call(command, shell=True)
    if retcode == 0:
      print("Компиляция успешно завершена")
      subprocess.Popen([os.path.join(release_dir, release_binary)])
    else:
      print("Произошла ошибка при компиляции")
  except OSError as e:
    print("Ошибка при вызове g++:", e)

# Detect that one event occurs
def event_parser(event):  
  event_type=event.event_type
  src_path=event.src_path
  splitted_path=src_path.split("/")
  for item in splitted_path:
    if(item in ignore):
      return
  print(event)
  is_directory=event.is_directory
  if(is_directory and event_type=='modified'):
    compile_handler(command, release_dir, release_binary)

# Event handler passed to observer
class EventHandler(FileSystemEventHandler):
  def on_created(self, event):
    event_parser(event)

  def on_deleted(self, event):
    event_parser(event)

  def on_modified(self, event):
    event_parser(event)

# Main watchdog observer
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')
  path = sys.argv[1] if len(sys.argv) > 1 else '.'
  event_handler = EventHandler()
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
    while True:
      time.sleep(1)
  finally:
    observer.stop()
    observer.join()