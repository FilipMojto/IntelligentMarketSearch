@echo off

rem Specify the path to your requirements.txt file

if "%1" == "" (
    set requirements_path=.\.venv\uninstall.txt
) else (
    set requirements_path="%1"
)


rem Run the pip install command
pip uninstall -r "%requirements_path%"