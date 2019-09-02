Set-Location 'D:\Games\GitHub\tgapi'
Remove-Item -R build
Remove-Item -R dist
Remove-Item -R tgapi.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*
Start-Sleep -Seconds 30
pip install tgapi -U