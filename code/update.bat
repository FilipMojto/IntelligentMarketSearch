@echo off

rem Specify the path to your requirements.txt file
set requirements_path=.\myenv\requirements.txt

rem Run the pip install command
pip install -r "%requirements_path%"