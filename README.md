# javobu

A simple japanese vocabulary list builder:
Reads from stdin and prints out a vocabulary list.

## Usage

just feed in text from stdin e.g.

```
python javobu.py < someTextFile.txt
```

Of course you can use curl or other tools to pipe in your online novel or things like that.

## Installation

For now javobu runs with Python 3.9.
Still have to test 3.10.

Suggestion: it could be helpful to install the following dependencies in a virtual enviroment.

Javobu heavily relies on the great tools of Paul McCann (fugashi, cutlet), the Jamdict, UniDic and MeCab project and we have to install these dependencies by:


```
pip install mecab-python3==1.0.4
pip install fugashi[unidic]
python -m unidic download

pip install cutlet

pip install wheel
pip install jamdict jamdict-data
```

Notice: we install the mecab bindings to use the shipped mecab binary of this lib.
Of corse you could use another dictionary with fugashi.
Please check the fugashi site for this: https://github.com/polm/fugashi


## License:

My code BSD-3 but be aware of the license of the used projects.