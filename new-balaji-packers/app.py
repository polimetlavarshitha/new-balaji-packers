"""
New Balaji Packers and Movers - Application Launcher
This project has been converted to a complete Django project.
You can run:
    python manage.py runserver
or execute this file directly:
    python app.py
"""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "balaji_packers.settings")
    from django.core.management import execute_from_command_line
    args = sys.argv
    if len(args) == 1:
        args = [args[0], "runserver", "127.0.0.1:8000"]
    execute_from_command_line(args)