@echo off
CLS

echo Create resource file.
call qrc_to_py

IF ERRORLEVEL 1 ( 
	echo Error in resource file !!!
	GOTO END
)

echo Create source.py file.
crtsource.py

IF ERRORLEVEL 1 ( 
	echo Error in crtsource.py !!!
	GOTO END
)


echo Create prog files.
build.py py2exe

echo Delete temp folder 'build'.
rd /s /q build


:END