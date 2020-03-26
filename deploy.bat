@ECHO off

CALL :TESTS
IF "%errorlevel%"=="0" CALL :DEPLOY %1

PAUSE > nul
GOTO :EOF


:TESTS
SET PYTHONPATH=%cd%
CD tests
python -m pytest
SET test_result=%errorlevel%
CD ..
EXIT /B %test_result%

:DEPLOY
set env=%1

IF "%env%"=="" SET /p env=(Test/Production)?
IF /I "%env%"=="Test" CALL :DEPLOY_TEST_PYPI
IF /I "%env%"=="Production" CALL :DEPLOY_PYPI
GOTO :EOF


:DEPLOY_PYPI
SET Test=False
python -m pip install --user --upgrade twine
python setup.py sdist bdist_wheel && python -m twine upload --skip-existing -u __token__ -p %pypi_token% dist/*
GOTO :EOF

:DEPLOY_TEST_PYPI
SET Test=True
python -m pip install --user --upgrade twine
python setup.py sdist bdist_wheel && python -m twine upload --repository-url https://test.pypi.org/legacy/ --skip-existing -u __token__ -p %pypi_test_token% dist/*
GOTO :EOF
