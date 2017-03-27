@echo off
REM script executed from windows scheduler
REM Assuming your project is located under "C:\<path to your project>\" Change to appropriate location
cd /d "C:\<path to your project>"
<path to your python exec or virtualenv>\python.exe main.py --collection enhanced --wallpaper --now
		
IF %ERRORLEVEL% NEQ 0 (
	ECHO "Batch file return code: %ERRORLEVEL%"
	IF %ERRORLEVEL% EQU 2 (
		ECHO "dscovr-epic-wallpaper batch execution failed. Check Internet Connectivity."
		)
	PAUSE
	)

EXIT %ERRORLEVEL%