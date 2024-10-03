aws codeartifact login --region us-east-2 --tool twine --repository CybiricalPyPiRepo --domain cybirical-software-development --domain-owner 151885604979
export TWINE_USERNAME=aws
export TWINE_PASSWORD=`aws codeartifact get-authorization-token --region us-east-2 --domain cybirical-software-development --domain-owner 151885604979 --query authorizationToken --output text`
export TWINE_REPOSITORY_URL=`aws codeartifact get-repository-endpoint --region us-east-2 --domain cybirical-software-development --domain-owner 151885604979 --repository CybiricalPyPiRepo --format pypi --query repositoryEndpoint --output text`
rm -rf dist
python3 -m pip install -U wheel twine setuptools
python3 setup.py sdist
python3 setup.py bdist_wheel
python3 -m twine upload dist/* --verbose