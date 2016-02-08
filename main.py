from utils.file_runner import FileRunner
import logging

logging.basicConfig(level=logging.INFO)
runner = FileRunner()
tasks = runner.load_file_and_analyze("input.txt")

for task in tasks:
    task.get()

with open("output/output.txt", 'r') as fin:
    print fin.read()
