@echo off
REM Replace myenv with your conda environment name
set ENV_NAME=fetch-help
REM List of agent subdirectories
set AGENTS=admin api_spec architecture data_model devops project_overview requirement router testing_strategy user_stories
for %%d in (%AGENTS%) do (
    if exist "agents\%%d\%%d.py" (
        echo Opening new cmd for agents.%%d.%%d
        start cmd /k "conda activate %ENV_NAME% && python -m agents.%%d.%%d"
    )
)
