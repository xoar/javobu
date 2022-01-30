# javobu

A simple japanese vocabulary list builder:
Reads from stdin and prints out a vocabulary list.

## Usage

just feed in text from stdin e.g.

```
python javobu.py < someTextFile.txt
```

Of course you can use curl or other tools to pipe in your online novel or things like that.

You can sort the list by the number of occurrence or by given categories like noun, etc.
See javobu.py --help for further informations.
```
python javobu.py --count < someTextFile.txt
python javobu.py -c Noun -c Verb < someTextFile.txt
```

## Installation

For now javobu only runs with Python 3.9.
Python 3.10 has currently problems with the mecab-python3 bindings.

Suggestion: it could be helpful to install the following dependencies in a virtual enviroment.

Javobu heavily relies on the great tools of Paul McCann (fugashi, cutlet), the Jamdict, UniDic and MeCab project and we have to install these dependencies by:


```
pip install mecab-python3==1.0.4
pip install fugashi[unidic]
python -m unidic download

pip install cutlet

pip install wheel
pip install jamdict jamdict-data

pip install click
```

Notice: we install the mecab bindings to use the shipped mecab binary of this lib.
Of course you can install the mecab library instead, see https://github.com/SamuraiT/mecab-python3.
Then you can use python 3.10 for javobu.

Of course you could use another dictionary with fugashi.
Please check the fugashi site for this: https://github.com/polm/fugashi


## License:

My code BSD-3 but be aware of the license of the used projects.