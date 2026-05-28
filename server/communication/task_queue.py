import uuid


class TaskQueue:

    def __init__(self):

        self.tasks = []

    def create_task(
        self,
        title,
        agent,
        payload,
        priority="normal"
    ):

        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "agent": agent,
            "payload": payload,
            "priority": priority,
            "status": "pending"
        }

        self.tasks.append(task)

        return task

    def get_tasks(self, agent):

        return [
            task for task in self.tasks
            if task["agent"] == agent
        ]

    def update_task(self, task_id, status):

        for task in self.tasks:

            if task["id"] == task_id:

                task["status"] = status

                return task

        return None


queue = TaskQueue()