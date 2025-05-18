from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import signal
import subprocess
import time


load_dotenv()

def execute(command, cwd=None, timeout=1):
    """
    Execute a command with a timeout, returning its output details.
    
    :param command: A list containing the command and its arguments.
    :param cwd: The directory in which to run the command.
    :param timeout: Timeout value in seconds.
    :return: Tuple (returncode, stdout, stderr, elapsed_time).
    """
    start_time = time.time()
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            preexec_fn=os.setsid
        )
        stdout, stderr = process.communicate(timeout=timeout)
        elapsed_time = time.time() - start_time
        return process.returncode, stdout, stderr, elapsed_time
    except subprocess.TimeoutExpired:
        # Kill process tree if timeout is reached.
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        stdout, stderr = process.communicate()
        elapsed_time = time.time() - start_time
        stderr = f"Command time out after {timeout} seconds."
        return process.returncode, stdout, stderr, elapsed_time
    except Exception as e:
        elapsed_time = time.time() - start_time
        return -1, "", str(e), elapsed_time

def parse_code(code):
    code = code.replace("```python", "")
    code = code.replace("```", "")
    return code


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="write a code to print fiboncaci sequence in python",
    config=types.GenerateContentConfig(
        system_instruction="You are a code generation AI assistant. You will be given instructions, you will generate the code in the best and optimal way. Validity and correctness of the code is most important. Then you will be given the response to the code, and you shall correct the code if needed to generate the correct output. Only output the code. The code needs to be able to be plugged in and run without any changes. Do not include any extra information that might break the code -- example: example usage, description, etc. Do not include any commands that require user interaction."
    )
)
print(response)

with open("test.py", "w") as f:
    code = parse_code(response.text)
    f.write(code)


command = ["python", "test.py"]

returncode, stdout, stderr, elapsed_time = execute(command)

print(f"Return code: {returncode} Elapsed time: {elapsed_time} Stdout: {stdout} Stderr: {stderr}")


