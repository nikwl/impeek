rm -r build
rm -r dist
rm -r impeek.egg-info

python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*