import os
from jinja2 import Environment, FileSystemLoader
import shutil

from config import get_config


def select_course():
    config = get_config()
    courses = list(config["courses"].keys())
    for i, course in enumerate(courses):
        print(f"{i + 1} - {course}")
    return courses[int(input("Select course: ")) - 1]


def get_question_count():
    return int(input("Input question count: "))


def get_assignment_name():
    return input("Input assignment name: ")


def list_template_files(template_dir):
    template_files = []
    for root, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".jinja"):
                rel_path = os.path.relpath(root, template_dir)
                if rel_path == ".":
                    rel_path = ""
                template_files.append(os.path.join(rel_path, file).replace("\\", "/"))
    return template_files


def create_course(course: str):
    config = get_config()
    course_folder = f"{course.lower()}-latex"
    course_dir = os.path.join(config["path"], course_folder)
    citation_title = f"{course} Assignments"
    bib_ref = f"El-Deeb_{citation_title.replace(" ", "_")}"
    github_repo = f"{course_folder}"

    variables = {
        "citation_title": citation_title,
        "bib_ref": bib_ref,
        "github_repo": github_repo,
    }

    course_template_path = os.path.join("templates", "course")
    templates = list_template_files(course_template_path)

    env = Environment(loader=FileSystemLoader(course_template_path))

    for template_file in templates:
        template = env.get_template(template_file)
        rendered_content = template.render(variables)

        output_path = os.path.join(course_dir, template_file.replace(".jinja", ""))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as file:
            file.write(rendered_content)


def process_name(template_file: str, replacements: dict) -> str:
    template_file = template_file.replace(".jinja", "")

    for old, new in replacements.items():
        if isinstance(new, str):
            template_file = template_file.replace(f"{{{{{old}}}}}", new)

    return template_file


def create_assignment(course: str, assignment_name: str, question_count: int) -> bool:
    config = get_config()
    course_folder = os.path.join(config["path"], f"{course.lower()}-latex")
    assignment_folder = os.path.join(course_folder, assignment_name)

    tex_file = f"{course.lower()}_{assignment_name.replace(" ", "-")}_201900052_Mohamed-Hussien-El-Deeb.tex"
    assignment_title = f"{course} {assignment_name}"
    problems = [f"Problem {i}" for i in range(1, question_count + 1)]
    citation_title = f"{course} Assignments"
    bib_ref = f"El-Deeb_{citation_title.replace(" ", "_")}"

    variables = {
        "tex_file": tex_file,
        "course": course,
        "assignment_title": assignment_title,
        "problems": problems,
        "bib_ref": bib_ref,
    }

    assignment_template_path = os.path.join("templates", "assignment")
    templates = list_template_files(assignment_template_path)

    env = Environment(loader=FileSystemLoader(assignment_template_path))

    for template_file in templates:
        output_file = process_name(template_file, variables)
        output_path = os.path.join(assignment_folder, output_file)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as file:
            file.write(env.get_template(template_file).render(variables))

    shutil.copy(os.path.join(course_folder, "references.bib"), assignment_folder)

    return True
