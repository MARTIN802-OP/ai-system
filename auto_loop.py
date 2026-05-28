from tool_server import run_command

MAX_RETRIES = 3

def execute_project(project_path):

    attempts = 0

    while attempts < MAX_RETRIES:

        result = run_command(
            "python main.py",
            project_path
        )

        if result["code"] == 0:
            print("SUCCESS")
            return True

        print("ERROR:")
        print(result["stderr"])

        # AI should fix files here

        attempts += 1

    return False