import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

def sum(sl):
    if len(sl)>600:
        stopwords = nltk.corpus.stopwords.words('russian')
        stopwords.extend([',', '.', '#'])
        words = word_tokenize(sl)
        freqTable = dict()
        for word in words:
            word = word.lower()
            if word in stopwords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1
        sentences = sent_tokenize(sl)
        sentenceValue = dict()

        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq

        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]

            # Average value of a sentence from the original text
        average = int(sumValues / len(sentenceValue))

        # Storing sentences into our summary.
        summary = ''
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence
        if summary != '':
            return summary
        else:
            return sentence
    else:
        return sl
