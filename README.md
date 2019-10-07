# lpass-get
Command line utility that makes fetching passwords from LastPass simple

```
lpass-get [website] [username]
```

If a unique match is found for the search criteria, the password will be copied to X11 clipboard by default. In case of multiple mathces, all the results are displayed for you to refine your query

### Dependencies
Install the following dependencies using your favorite package manger
* [Python 3](https://www.python.org/download/releases/3.0/)
* [LastPass CLI](https://github.com/lastpass/lastpass-cli)
* [xclip](https://github.com/astrand/xclip)

### Installation
Once you have installed the above dependencies, copy lpass-get.py to any location that is in your path and you can start using it

### Usage

**Full Search**
```
lpass-get gmail.com foo21@gmail.com
```

**Fuzzy Search**
```
lpass-get gm foo
lpass-get gm
lpass-get fo
```

**Print password, don't copy**
```
lpass-get -p gm foo
```
