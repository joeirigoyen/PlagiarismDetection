import os
import subprocess

# Install the package
subprocess.run(["pip", "install", "-e", "."])
# Clear output
os.system("cls")
subprocess.run(["python", "-m", "src.wrapper.demo"])
