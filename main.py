import argparse

import core
import config

parser = argparse.ArgumentParser(prog="latext", description="Create latex assignments.")
subparsers = parser.add_subparsers(dest="command")

course_parser = subparsers.add_parser("c", help="Create a course")
course_parser.add_argument("-c", "--code", help="Course code", required=True)
course_parser.add_argument(
    "-n", "--number", help="Course number", type=int, required=True
)

assignment_parser = subparsers.add_parser("a", help="Create an assignment")

args = parser.parse_args()

if args.command is None:
    parser.print_help()
    exit(1)


if __name__ == "__main__":
    if args.command == "c":
        course = f"{args.code.upper()}-{args.number}"
        if config.create_course(course):
            core.create_course(course)
    elif args.command == "a":
        course = core.select_course()
        assignment = core.get_assignment_name()
        question_count = core.get_question_count()
        if assignment_name := config.create_assignment(
            course, assignment, question_count
        ):
            core.create_assignment(course, assignment_name, question_count)
