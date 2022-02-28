sudo apt update

if [ -z "$(which python)" ]; then
    sudo apt install python
fi

python --version
echo "python installed"

if ! [ -x "$(command -v pip)" ]; then
  echo 'pip not installed'
  sudo apt-get install python3-pip
  pip --version
  echo 'pip installed'
else
  echo 'pip already installed'
  pip --version
fi


python -m venv venv
echo "Virtual environment created"
source venv/bin/activate
pip install -r requirements.txt
echo "Setup complete"
