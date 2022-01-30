import cutlet
import jaconv
import fileinput
import click

from fugashi import Tagger
from jamdict import Jamdict

from operator import itemgetter

@click.command()
@click.option('--count', is_flag=True, help='Will affect the order. Sort the words by count of apperance. Without this flags words are printed in order as they are appear in the text')
@click.option('--category', '-c', multiple=True, default=[],
              help='Print words of the given categroy first. Valid categories are Verb,Adjective,Noun')
def cli(count,category):
    """
    Parse japanese words from stdin and build a vocabulary list.

    Just feed it with stdin e.g.

        python javobu.py < someTextFile.txt
    """

    parseStdin(count,category)

## parse stdin and print out the vocabulary list
def parseStdin(count,categories):

    tagger = Tagger('-Owakati')

    katsu = cutlet.Cutlet()
    jam = Jamdict()

    #TODO option mergeWords merge words wich are the same but written with different kanjis

    #unwanted suffixes like ta,wa,de etc.
    unwantedSuffixTypes = ['格助','接助','助動','補助','係助','準助','名','副助','終助']

    wordDict = {}

    #get lines from stdin and parse them
    for line in fileinput.input([]):
        for word in tagger(line.strip()):
            
            #extract a inclected word for a lookup.
            #use the inflected version of the word to eliminate past tense(ta) and other inflections
            #TODO: with unidic .lemma sometimes change the kanjis.
            #instead we use orthbase to preserver the meaning of the kanjis
            #Maybe this caused the bugs with wrong meanings in getWord(). inspect this, see later TODOs
            lemma = word.feature.orthBase

            #for now we use the lemma as a key.
            #this leads to two entries for two ways of writing the same word with different kanjis.
            #each way of writing of the word leads to another meaning.
            #therefore with this approach we only want to save a word with its special meaning.
            #instead we could use a hiragana/romaji version for the lookup to eliminate the encoded meaning.
            #TODO: add an option to merge the different ways of writing, by change it to romaji before.
            key = lemma
            if key not in wordDict:
                
                #delete the unwanted suffixes like te,de,wa etc.
                #unk are words unknown to the dict
                if (word.feature.type not in unwantedSuffixTypes) and not word.is_unk:
                    wordDict[key]=[lemma,word.feature.type,0]
            else:
                wordTuple = wordDict[key]
                wordTuple[2]+=1

    #now sort the words depending of their count of appearance in the text
    if count:
        sortedDict = reversed(sorted(wordDict.values(),key=itemgetter(2)))

    #else all values are printed in the order as they were appended.
    #since the dict act like this in python(3.5?)
    else:
        sortedDict = wordDict.values()

    #print the words in the order of the given categories(types)
    #first rebuild the list to match the given types to the types of the dict like
    #if no categries are given this remains an empty list and some actions are skipped
    wantedTypes = []
    for cat in categories:
            if cat == "Noun":
                wantedTypes.append('体')
            if cat == "Verb":
                wantedTypes.append('用')
            if cat == "Adjective":
                wantedTypes.append('相')

    #slow but easy solution. just iterate several times over the words for each categroy
    for wantedType in wantedTypes:
        for oldLemma,oldWordType,count in sortedDict:
            #update the lemma and wordType
            lemmaWord,wordType = getWord(oldLemma,oldWordType,unwantedSuffixTypes,tagger)
            if (lemmaWord is not None) and (wordType == wantedType):
                printWord(lemmaWord,wordType,count,jam,katsu,oldLemma,oldWordType)
        
    #now print the rest. these word types are not given and therefore not in the type list
    #if no categries are given this prints all words.
    for oldLemma,oldWordType,count in sortedDict:
        #update the lemma and wordType
        lemmaWord,wordType = getWord(oldLemma,oldWordType,unwantedSuffixTypes,tagger)
        if (lemmaWord is not None) and (wordType not in wantedTypes):
            printWord(lemmaWord,wordType,count,jam,katsu,oldLemma,oldWordType)


## update the word to get the word kana feature(katakana) to translate it to hiragana.
## check if the word is not a suffix
def getWord(oldLemma,oldWordType,unwantedSuffixTypes,tagger):

    #first query the word again. with this we get a katakan version of the inflected word.
    #if we would have saved the kana version before, this would be the katakana version of the flected word(in past tense etc.)
    #we hopefully have only one entry in the query list
    #TODO: check if this happens sometimes
    queryWord = tagger(oldLemma)

    if queryWord is not None and len(queryWord)>0:

        #the lemma sometimes change a bit.
        #TODO: recheck this, if this still happen
        lemmaWord = queryWord[0]
        
        wordType = lemmaWord.feature.type

        #somtimes suffixes still landing here trough a changed in the lemma form.
        #can track the changes through the old and the new type:
        #oldwordType vs wordType and lemma vs oldLemma.
        #e.g. tan and ta
        #TODO: still have to inspect these breaking words
        if wordType not in unwantedSuffixTypes:
            return (lemmaWord,wordType)

    return (None,None)

## print the word together with hiragana and romaji
def printWord(lemmaWord,wordType,count,jam,katsu,oldLemma,oldWordType):

        lemma = lemmaWord.surface
        katakana = lemmaWord.feature.kana
        try:
                hiragana = jaconv.kata2hira(katakana)
        except:
                #TODO:The libary complains about a NonType
                #trace this bug
                hiragana = "no hiragana"
                romaji = "no romaji"
        else:
                romaji = katsu.map_kana(hiragana)

        #first print the header
        print(hiragana,lemma,romaji,wordType,count,':',oldLemma,oldWordType,':',sep='\t')

        #now lookup the translations.
        #use a pure string for the lookup. therefore we could use surface or lemma.
        result = jam.lookup(lemma)

        for entry in result.entries:
                    #it seems that the only way of printing the kanji with the meaning is over repr
                    #TODO: find a way to get the kanji with the translation to eliminate unwanted meanings
                    print(repr(entry))
                
        #print a footer
        print('_____________________________________________________________\n')



if __name__ == '__main__':
    cli()
