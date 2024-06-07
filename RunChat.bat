@echo on
set "python_script=C:\Users\mack.bacarisas\Downloads\rasta\chat.py"
set "log_file=C:\Users\mack.bacarisas\Downloads\rasta\Chatreport.txt"
set "python_process=python.exe"

tasklist /FI "IMAGENAME eq %python_process%" 2>NUL | find /I /N "%python_process%" >NUL
echo [%date% %time%] Service restarting>> "%log_file%"
taskkill /F /IM %python_process%
start "" python "%python_script%"


exit /b 0
