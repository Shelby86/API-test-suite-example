# Gemini-API-Tests


Hello and welcome to the Gemini API automation

Set Up:

- To run these tests, in the conftest.py file, change the username after the return

To run a test by marker: cd to the tests directory, then python3 -m pytest -m mark_name -s

To run with print statements:

pytest -m marker --log-cli-level=DEBUG -s

or as a whole

pytest --log-cli-level=DEBUG -s

or simply pytest -s

to install the requirements:

pip3 -r requirements.txt

Pyodbc import on new Mac:

The following was used to install the pyodbc module:

- pip3 install --no-binary :all: pyodbc
- pip3 install pyodbc==4.0.34
- export LDFLAGS="-L/opt/homebrew/Cellar/unixodbc/your-version/lib"
  export CPPFLAGS="-I/opt/homebrew/Cellar/unixodbc/your-version/include"
  pip3 install --no-binary :all: pyodbc

  - brew update
  brew install pyenv

- If not in .zhrsc, open .zhrsc and add the following:
  export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"

if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

Now install the pyodbc driver:
- brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18

Now you should be able to run

- pip3 install pyodbc

Link to complete documentation:
- https://github.com/mkleehammer/pyodbc/issues/1124