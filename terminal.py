import subprocess
import os,sys
from pathlib import Path
import hashlib
import shlex
from colorama import Fore, Style

def bash(command: str):
    return subprocess.run(
        ["bash", "-c", command],
        capture_output=True,
        text=True
    )
bash("python3 -m ensurepip --upgrade")
bash("pip install colorama")
def Terminal(username, password):
    try:
        dir_ = Path.cwd()
        filename = f"{username}.zcc"
        filepath = dir_ / filename

        if filepath.exists():
            with open(filepath, "r") as f:
                file_content = f.read().strip()

            if file_content != hashlib.sha512(password.encode("utf-8")).hexdigest():
                print("Refused permission [Incorrect password]")
                return 0
        else:
            with open(filepath, "w") as f:
                f.write(hashlib.sha512(password.encode("utf-8")).hexdigest())

        history = []

        attr = [
            "us",
            "pw",
            "clr"
        ]

        sys_ = []

        prcs = (
    Fore.RED + f"[{username}]"
    + Fore.WHITE + "──"
    + Fore.GREEN + "@"
    + Fore.BLUE + " \n╰─"
    + Fore.RED + ""
    + Fore.BLUE + "$"
    + Fore.CYAN + " "
    + Style.RESET_ALL
)

        print("Press exit to quit, help for help and 'nbash help -a' for nbash help")
        print("Terminal")
        while True:
            try:
                command = input(prcs).strip()
            except KeyboardInterrupt:
                print()
                break
            except EOFError:
                print()
                break

            if not command:
                continue

            history.append(command)

            if command.lower() in ("exit", "quit"):
                break

            part = command.split()

            if not part:
                continue

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
                        old_username = username
                        username = input(f"New username for {username}: ").strip()

                        if not username:
                            print("Error: username cannot be empty.")
                            username = old_username
                            continue

                        if username != old_username:
                            old_filepath = dir_ / f"{old_username}.zcc"
                            new_filepath = dir_ / f"{username}.zcc"

                            if new_filepath.exists():
                                print(f"Error: username [{username}] already exists.")
                                username = old_username
                                continue

                            if old_filepath.exists():
                                old_filepath.rename(new_filepath)

                        prcs = (
                            Fore.RED + f"[{username}]"
                            + Fore.GREEN + "...@ "
                            + Fore.BLUE + "\n--$"
                            + Fore.CYAN + " "
                        )
                    else:
                        print("Incorrect password")

                elif len(part) >= 3 and part[1] == "pw" and part[2] == "c":
                    if input(f"Password for {username}: ") == password:
                        password = input(f"New password for {username}: ")

                        if not password:
                            print("Error: password cannot be empty.")
                            continue

                        filepath = dir_ / f"{username}.zcc"

                        with open(filepath, "w") as f:
                            f.write(
                                hashlib.sha512(
                                    password.encode("utf-8")
                                ).hexdigest()
                            )
                    else:
                        print("Incorrect password.")

                elif len(part) >= 3 and part[1] == "write":
                    command = " ".join(part[2:]).strip()

                    if not command:
                        print("Usage: nbash write <file>")
                        continue

                    filepath_ = dir_ / command

                    if not filepath_.exists():
                        filepath_.touch()

                    while True:
                        x = input("")

                        if x == "ex":
                            break

                        with open(filepath_, "a") as f:
                            f.write(x + "\n")

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

                elif len(part) >= 3 and part[1] == "pyint" and part[2] == "print":
                    py_command = command.split(" ", 3)

                    if len(py_command) >= 4:
                        sys_.append(f"print({py_command[3]!r})")
                    else:
                        print("Usage: nbash pyint print <value>")

                elif len(part) >= 3 and part[1] == "pyint" and part[2] == "-e":
                    try:
                        exec("\n".join(sys_))
                    except Exception as e:
                        print(f"Python execution error: {e}")

                elif len(part) >= 2 and part[1] == "struct":
                    if input(f"Password for {username}: ") == password:
                        x = input("New process: ")

                        if "dir" in x:
                            prcs = (
                                Fore.RED + f"[{os.getcwd()}\\{username}]"
                                + Fore.GREEN + "...@ "
                                + Fore.BLUE + "\n--$"
                                + Fore.CYAN + " "
                            )
                        else:
                            prcs = (
                                Fore.RED + f"[{username}]"
                                + Fore.GREEN + "...@ "
                                + Fore.BLUE + "\n--$"
                                + Fore.CYAN + " "
                            )

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

            with open(f"{username}info.zcc", "w") as f:
                f.write(f"{history}")

    except KeyboardInterrupt:
        print()
        return 0

    except Exception as e:
        print(f"Error: {e}")


Terminal(input("Username: "), input("Password: "))
