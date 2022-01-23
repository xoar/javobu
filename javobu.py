import cutlet
import jaconv
import fileinput

from fugashi import Tagger
from jamdict import Jamdict

from operator import itemgetter


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
        lemma = word.feature.lemma

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
sortedDict = sorted(wordDict.values(),key=itemgetter(2))
#print(sortedDict)

for oldLemma,oldWordType,count in reversed(sortedDict):
    
    #get the hiragana and romaji
    #get the word kana feature(katakana) and translate to hiragana and then convert to romaji
    
    #first query the word again. with this we get a katakan version of the infelcted word.
    #if we would have saved the kana version before, this would be the katakana version of the flected word(in past tense etc.)
    #we hopefully have only one entry in the query list
    #TODO: check if this happens sometimes
    queryWord = tagger(oldLemma)

    if queryWord is not None and len(queryWord)>0:

        #the lemma sometimes change a bit.
        #TODO: recheck this, if this still happen
        lemmaWord = queryWord[0]
        
        lemma = lemmaWord.surface
        katakana = lemmaWord.feature.kana
        hiragana = jaconv.kata2hira(katakana)
        romaji = katsu.map_kana(hiragana)
        wordType = lemmaWord.feature.type

        #somtime prefix still landing here trough a changed in the lemma form.
        #can track the changes through the old and the new type:
        #oldwordType vs wordType and lemma vs oldLemma.
        #e.g. tan and ta
        #TODO: still have to inspect these breaking words
        if wordType not in unwantedSuffixTypes:
            print(hiragana,lemma,romaji,wordType,count,':',sep='\t')

            #now lookup the translations.
            #use a pure string for the lookup. therefore we could use surface or lemma.
            result = jam.lookup(lemma)

            for entry in result.entries:
                #it seems that the only way of printing the kanji with the meaning is over repr
                #TODO: find a way to get the kanji with the translation to eliminate unwanted meanings
                print(repr(entry))
            
            #print a footer
            print('_____________________________________________________________\n')

