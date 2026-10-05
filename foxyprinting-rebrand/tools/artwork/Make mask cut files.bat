@echo off
rem Foxy Printing - face mask cut files (Windows).
rem Drag one or more face images (JPG/PNG) onto this file.
rem It makes "<image name>.pdf/.svg" (layers Artwork + CUT) and "<name> - check.png"
rem in a "mask-cut-files" folder next to the first image.
rem Needs Python 3 from python.org (tick "Add python.exe to PATH" when installing).
rem mask_cutline.py must be in the same folder as this .bat file.

if "%~1"=="" (
  echo Drag face images onto this file to make the cut files.
  pause
  exit /b
)

python -c "import cv2, numpy, reportlab, pikepdf" 2>nul || (
  echo First run: installing the parts it needs...
  python -m pip install --quiet numpy "opencv-python-headless<5" reportlab pikepdf
)

python "%~dp0mask_cutline.py" %* --out "%~dp1mask-cut-files"
echo.
echo Done. Files are in: %~dp1mask-cut-files
echo Open each "check.png" and check the eye holes before cutting.
pause
