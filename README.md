<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="static//images/favicon.ico" alt="Project logo"></a>
</p>

<h3 align="center">Flask Link Shortener</h3>


---

<p align="center"> Website link shortener
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)
- [Additional](#additional)

## 🧐 About <a name = "about"></a>

Just a small project for casual use.

## 🏁 Getting Started <a name = "getting_started"></a>

```$ git clone https://github.com/MurilloMB/FlaskLinkShortener.git```

## Prerequisites

1. **Python 3.13 or newer**
2. **Git**

## Installing

All you need is inside the *requirements.txt* file. 

Just clone the repository, create a virtual envinronment in python with 
```
$ python -m venv venv
```

After that get into the virtual envinronment according your operational system

___

### Windows
```
$ .\venv\Scripts\activate.bat
```
*Need execution policy set to unrestricted to work*

### Linux
```
$ source ./venv/bin/activate
```
___

And at final
```
$ pip install -r requirements.txt
```


## 🎈 Usage <a name="usage"></a>

First of all enter into your virtual envinroment, if you don't know how go to - [Getting Started](#getting_started)

Use that command for initialize the database
```
$ flask initdb
```

Use the correctly startup for your operational system
### Windows
```
$ .\run.bat
```

### Linux
```
$ ./run
```

## ⛏️ Built Using <a name = "built_using"></a>

- [Python] (https://www.python.org/) - Language
- [SQLite3] (https://sqlite.org/) - Database
- [Waitress] (https://pypi.org/project/waitress/) - Server provider

## ✍️ Authors <a name = "authors"></a>

- [@MurilloMB](https://github.com/MurilloMB)


## Aditional <a name = "additional"></a>
- [@thomascsd](https://github.com/thomascsd) Thanks for VSCode Readme Pattern Extension
