import subprocess
import os,sys
from pathlib import Path
import hashlib
from colorama import Fore
def bash(command: str):
    return subprocess.run(
        ["bash", "-c", command],
        capture_output=True,
        text=True
    )


def Terminal(username, password):
    dir_ = Path(Path.cwd())
    file = [f for f in dir_ .iterdir() if f.is_file()]
    filename = f"{username}.zcc"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            file_content = f.read()
        if file_content == hashlib.sha512(password.encode("utf-8")).hexdigest():
            print("Permission granted")
        else:
            print("Refused permission [Incorrect password]")
        return 0
    else:
        with open(filename, "w") as f:
            f.write(hashlib.sha512(password.encode("utf-8")).hexdigest())
            f.flush()
            f.write(username)
    history = []
    
    
    attr = [
        "us",
        "pw",
        "clr"
    ]

    sys_ = []
    prcs = Fore.RED+ f"[{username}]{Fore.GREEN}...@ {Fore.BLUE}\n--${Fore.CYAN} "
    print("Press exit to quit: ")
    while True:
        command = input(prcs).strip()
        history.append(command)
        if not command:
            continue

        if command.lower() in ("exit", "quit"):
            break

        part = command.split()

        if part[0].lower() == "nbash":
            
            if len(part) >= 3 and part[1].lower() == "help" and part[2] == "-a":
                print("Help:")
                print("Regular bash commands help wizard: [help]")
                print("Advance:")
                print("\"-a\": all the information about the tool for zter")
                print("\"-c\": change the attribute")
                print("\"-!\": delete the file or directory")
                print("\"-g\": create a new file/directory")
                print("struct: structure of the input process")
                print("Inbuilt attributes:")
                print("us: username")
                print("pw: password")
                print("clr: color")
                print("Inbuilt features:")
                print("pyint: python integration [-e: execute]")
                print("")

            elif len(part) >= 3 and part[1] == "us" and part[2] == "-c":
                if input(f"Password for {username}: ") == password:
                    username = input(f"New username for {username}: ")
                    prcs = f"{username} --$ "
                else:
                    print("Incorrect password")
            elif len(part) >= 3 and part[1] == "pw" and part[2] == "c":
                if input(f"Password for {username}: ") == password:
                    password = input(f"New password for {username}: ")
                else:
                    print("Incorrect password.")
            elif(len(part) >=3 and part[1] == 'write' and part[2]):
                if not(part[2] in file):
                    bash(f"touch {part[2]}")
                else:
                    continue
                while True:
                    x = input("")
                    bash(f"echo {x} >> {part[2]}")
                    if(x == 'ex'): break
                
            elif command.endswith("-!"):
                if len(part) < 3:
                    print("Usage: nbash <file/directory> -!")
                    continue

                command = " ".join(part[1:-1]).strip()

                if command in attr:
                    print("Error, The value is an attribute and cannot be deleted...")
                    continue

                if not os.path.exists(command):
                    print(f"Error, [{command}] does not exist...")
                    continue

                try:
                    if os.path.isdir(command):
                        os.rmdir(command)
                    else:
                        os.remove(command)
                except OSError as e:
                    print(f"Error deleting [{command}]: {e}")

            elif command.endswith("-g"):
                if len(part) < 3:
                    print("Usage: nbash <name> -g")
                    continue

                command = " ".join(part[1:-1]).strip()

                if command in attr:
                    print(f"Error, [{command}] is an attribute...")
                    continue

                if os.path.exists(command):
                    print(f"Error, [{command}] already exists...")
                    continue

                try:
                    os.mkdir(command)
                except OSError as e:
                    print(f"Error creating [{command}]: {e}")

            elif len(part) >= 5 and part[1] == "var_s":
                if part[3] != "=":
                    print("Usage: nbash var_s <name> = <value>")
                    continue

                sys_.append(f"{part[2]} = {part[4]!r}")

            elif len(part) >= 5 and part[1] == "var_i":
                if part[3] != "=":
                    print("Usage: nbash var_i <name> = <value>")
                    continue

                try:
                    int(part[4])
                except ValueError:
                    print("Error: value must be an integer.")
                    continue

                sys_.append(f"{part[2]} = {part[4]}")

            elif len(part) >= 5 and part[1] == "var_f":
                if part[3] != "=":
                    print("Usage: nbash var_f <name> = <value>")
                    continue

                try:
                    float(part[4])
                except ValueError:
                    print("Error: value must be a float.")
                    continue

                sys_.append(f"{part[2]} = {part[4]}") 

            if(len(part) >= 3 and part[1] == 'pyint' and part[2] == 'print'):
                sys_.append(f"{command.lstrip("nbash").lstrip("pyint")}")
            elif len(part) >= 3 and part[1] == "pyint" and part[2] == "-e":
                try:
                    exec("\n".join(sys_))
                except Exception as e:
                    print(f"Python execution error: {e}")

            elif len(part) >= 2 and part[1] == "struct":
                if input(f"Password for {username}: ") == password:
                    x = input("New process: ")

                    if "dir" in x:
                    
                        prcs = f"{os.getcwd()}{username} --$ "
                    else:
                        prcs = f"{username} --$ "

                else:
                    print("Incorrect password.")
            
            else:
                print("Unknown nbash command.")

        else:
            result = bash(command)

            if result.stdout:
                print(result.stdout, end="")

            if result.stderr:
                print(result.stderr, end="")
        with open(f"{username}info.zcc",'w') as f:
                f.write(f"{history}")
        
Terminal(input("Username: "), input("Password: "))
