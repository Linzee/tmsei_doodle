## Install and launch

### Initial setup

Install [pip](https://pip.pypa.io/en/latest/installing/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

```
pip install virtualenvwrapper
```

Setup your local virtual environment

```
cd <path_to_your_local_git_repo>
virtualenv venv -p python3
source venv/bin/activate
```

Install python dependencies

```
pip install -r requirements.txt
```

### Launch notebooks

Activate virtual environment and start Jupiter server

```
cd <path_to_your_local_git_repo>
source matmat/bin/activate
cd notebooks
jupyter notebook
```

> Most reccent version of this repository is avalaible at [GitHub](https://github.com/Linzee/tmsei_doodle).
