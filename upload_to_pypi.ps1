Set-Location 'D:\Games\GitHub\tgapi'
python setup.py sdist bdist_wheel
twine upload dist/*
Start-Sleep -Seconds 30
pip install tgapi -U -i https://pypi.org/simple/
Remove-Item -R build
Remove-Item -R dist
Remove-Item -R tgapi.egg-info
