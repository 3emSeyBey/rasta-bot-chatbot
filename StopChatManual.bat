@echo on

set "python_process=python.exe"

tasklist /FI "IMAGENAME eq %python_process%" 2>NUL | find /I /N "%python_process%" >NUL
if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] Stopping Python script...
    taskkill /F /IM %python_process%
    echo [%date% %time%] Python script has been stopped.
) else (
    echo [%date% %time%] Python script is not running.
)

