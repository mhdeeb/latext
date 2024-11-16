import json


def get_config() -> dict:
    with open("config.json", "r") as f:
        return json.load(f)


def set_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f)


def create_course(course: str) -> bool:
    config = get_config()
    if course not in config["courses"]:
        config["courses"][course] = {}
        set_config(config)
        return True
    return False


def create_assignment(course: str, assignment: str, question_count: int) -> str:
    config = get_config()
    if course not in config["courses"]:
        return ""
    assignments = config["courses"][course]
    if assignment in assignments:
        return ""
    config["courses"][course][assignment] = question_count
    set_config(config)
    return assignment
