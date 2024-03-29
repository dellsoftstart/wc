from enum import unique
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View,ListView
from django.shortcuts import render, redirect
from .models import *
import re
from collections import Counter
from django.db.models import Avg
from django.contrib import messages
from langdetect import detect

class HomeView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'kg/home.html')


def clean_word(text):

    text_without_numbers = re.sub(r'\d+\.', '', text)
    # Чистим текст от пунктуации
    regex = r"(\w+-\w+)|-+"
    punctuation = '''!()[]{};:'"\,<>./?@#$%^&*_~'''
    txt_clean = re.sub(r"[¬]+\ *", "", text).lower()
    w_clean = re.sub(r"[–—‒−]+\ *", "-", txt_clean).lower()
    result = re.sub(r"[,.;@#?!&$»«+=…“”•●■]+\ *", " ", w_clean).lower()
    f_result = re.sub(regex, r"\1", result)
        
    final_string = ''
    for ch in f_result:
        if ch not in punctuation:
            final_string = final_string + ch

    return final_string.split()

def find_compound_words(text, compound_words):
    compound_words_found = []
    non_compound_words = []

    words = text   # <-- Замените это на words = text

    i = 0
    while i < len(words):
        word = words[i]
        compound = " ".join(words[i:i+2])
        if compound in compound_words and len(compound.split()) == 2:
            compound_words_found.append(compound)
            i += 2  # пропускаем второе слово составного слова
        else:
            non_compound_words.append(word)
            i += 1

    # Если нет составных слов, просто считаем слова как обычно
    if not compound_words_found:
        non_compound_words = words

    return compound_words_found, non_compound_words


def clean_sentences(str):  # sourcery skip: list-comprehension, remove-pass-body
    
        str_result = re.sub(r"([0-9]+[,.]+| [,.]+)", "", str)
        clean_str = str_result.strip()
        
        sentences = re.split(r'[//.|//!|//?]+|(?<!\.)\.(?!\.)', clean_str.replace('\n',''))

        long_s = []
        for word in sentences:
            if word.isdigit() and len(word)<=2:
                pass
            else:
                long_s.append(word)
        
        return long_s[:-1]




def count_syllables_kyrgyz(word):
    vowels = "аеёиоуыэюяөү"
    syllable_count = 0
    is_vowel = False

    for letter in word:
        if letter in vowels:
            if not is_vowel:
                syllable_count += 1
                is_vowel = True
        else:
            is_vowel = False
    
    return syllable_count

def total_syllable_count(text):
    words = text
    total_count = sum(count_syllables_kyrgyz(word) for word in words)
    return total_count

class IndexView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'kg/index.html')
    

    def post(self, request, *args, **kwargs):
      
        title = request.POST['title_name']
        author = request.POST['author']
        message = request.POST['message']

        # Claning & calculating words 
        all_words = clean_word(message)
        # words_q=len(all_words)
        level_result=""
        get_compoundwords = CompoundWord.objects.values_list('compound_words', flat=True). get(id=1)
        compound_words = get_compoundwords.lower()
        
        
        # Поиск составных слов
        compound_words_found, non_compound_words = find_compound_words(all_words, compound_words)
        
        print("compound_words_foundcompound_words_foundcompound_words_found", compound_words_found)

        # Общее количество слов, включая составные слова
        words_q = len(compound_words_found) + len(non_compound_words)
        complex_w_q = len(compound_words_found)
        total_words_count1 = compound_words_found + non_compound_words

        #  frequencies of words
        compound_word_frequencies={}
        for word in compound_words_found:
                 if word in compound_word_frequencies: 
                      compound_word_frequencies[word] += 1
                 else:
                      compound_word_frequencies[word] = 1

        

        


        if words_q >3 and detect(message) !='en':


            # Calculating quantity of polysyllabic words

            punctuation = '''аеёиоуэюяыөү'''
            def count_syllables_based_on_vowels(word):
                return sum(1 for letter in word if letter in punctuation)

            def is_polysyllabic(word, syllable_threshold):
                syllable_count = count_syllables_based_on_vowels(word)
                return syllable_count >= syllable_threshold


            longw = []
            
            
            longw = []

            for word in all_words:
                word_without_hyphen = word.replace('-', '')  # Убираем тире для подсчета слогов и анализа длины
                if len(word_without_hyphen) >= 11 and is_polysyllabic(word_without_hyphen, 3):
                    longw.append((word, len(word_without_hyphen)))

            multisyllabic_wq =len(longw)

            # Calculating frequencies of polysyllabic words
            longw_frequencies={}
            for words in longw:
                if words in longw_frequencies: 
                    longw_frequencies[words] += 1
                else: 
                    longw_frequencies[words] = 1
        


            
            

            
            

            # Cleaning & calculating sentences
            sentence_q = len(clean_sentences(message))

            # Calculsting average numbers of sentences for  text 
            sentence_avg = round((words_q/sentence_q),1)

            # Calculating syllables
            # syllables = len(count_vowels(str(all_words)))
            syllables = total_syllable_count(all_words)
            
            
            # Calculating syllables average
            syllables_avg = round((syllables / words_q),1)


            # Calculating unique words
            unique_words = []
            for words in all_words:
                if words not in unique_words:
                    unique_words.append(words)
            
            unique_words.sort()
            
            uniquew_q = len(unique_words)

            # Calculation of lexical diversity
            lexical_d = round((uniquew_q / words_q),2)
            

            # Calculating frequencies of words in uploaded text
            w_frequencies={}
            for words in all_words:
                if words in w_frequencies: 
                    w_frequencies[words] += 1
                else: 
                    w_frequencies[words] = 1

            # Start -->    Get list of long & compound words from database
            get_lcwords = LCWord.objects.values_list('lc_words', flat=True). get(id=1)
            clean_lcwords = clean_word(get_lcwords)
            



            # Comparing uploaded text with database of long and compound words
            lcwords_compare=list(set(clean_lcwords) & set(all_words))
            
            

            lcword_list = []
            for clean_lcwords in all_words:
                     if clean_lcwords in lcwords_compare:
                         lcword_list.append(clean_lcwords)
            
            
            

            # Calculation os hyphenated words

            hyphenated_w = re.findall(r'\w+-\w+[-\w+]*', str(all_words))
            for words in hyphenated_w:
                     if len(words) > 6:
                            lcword_list.append(words)
                
             
            

            #  Frequencies long & compound words
            lcword_frequencies={}
            for word in lcword_list:
                 if word in lcword_frequencies: 
                    lcword_frequencies[word] += 1
                 else:
                    lcword_frequencies[word] = 1
            
            compound_w_q=len(lcword_list)
            
            
        

            #### END ####d_frequencies

            # Start --> Get list of rare words from database

            get_rarewords = RareWord.objects.values_list('rare_words', flat=True). get(id=1)
            clean_rarewords = clean_word(get_rarewords)

            # Comparing uploaded text with database of long and compound words
            rarewords_compare=list(set(clean_rarewords) & set(all_words))

            rareword_list = []
            for clean_rarewords in all_words:
                 if clean_rarewords in rarewords_compare:
                         rareword_list.append(clean_rarewords)

            
            #  frequencies of words
            rareword_frequencies={}
            for word in rareword_list:
                 if word in rareword_frequencies: 
                      rareword_frequencies[word] += 1
                 else:
                      rareword_frequencies[word] = 1

            
            
            rareword_q = len(rareword_list)
            rareword_p = round(((100/len(all_words)) * rareword_q), 1)
            ######### END ###################

            ### Start --> # Get list of frequent words from database

            get_frequent_words = FreqWord.objects.values_list('freq_words', flat=True). get(id=1)
            
            clean_frequent_words = re.sub(r'[^\w\s]', '', get_frequent_words).lower().split()
            
            # Comparing uploaded text with database of frequent words
            freq_words_compare=list(set(clean_frequent_words) & set(all_words))
            
            freqword_list = []
            for clean_frequent_words in all_words:
                     if clean_frequent_words in freq_words_compare:
                         freqword_list.append(clean_frequent_words)

            #  frequencies of words
            fw_frequencies={}
            for word in freqword_list:
                if word in fw_frequencies: 
                    fw_frequencies[word] += 1
                else:
                    fw_frequencies[word] = 1
                    

            fw_q = len(freqword_list)
            fw_p = round(((100/len(all_words)) * fw_q), 1)
            ###END###



            all_compound_words_p = round(((100/words_q) * (multisyllabic_wq + compound_w_q + rareword_q + complex_w_q)),1)

            print("compound_words_p compound_words_p compound_words_p 111", all_compound_words_p)

            ###Levels for Grade1
            g1_word_q_l1 = g1Level.objects.values_list('g1_word_q_l1', flat=True). get(id=1)
            g1_word_q_l2 = g1Level.objects.values_list('g1_word_q_l2', flat=True). get(id=1)
            g1_word_q_l3 = g1Level.objects.values_list('g1_word_q_l3', flat=True). get(id=1)
            g1_sentence_q_l1 = g1Level.objects.values_list('g1_sentence_q_l1', flat=True). get(id=1)
            g1_sentence_q_l2 = g1Level.objects.values_list('g1_sentence_q_l2', flat=True). get(id=1)
            g1_sentence_q_l3 = g1Level.objects.values_list('g1_sentence_q_l3', flat=True). get(id=1)
            g1_avgwl_insyllables_l1 = g1Level.objects.values_list('g1_avgwl_insyllables_l1', flat=True). get(id=1)
            g1_avgwl_insyllables_l2 = g1Level.objects.values_list('g1_avgwl_insyllables_l2', flat=True). get(id=1)
            g1_avgwl_insyllables_l3 = g1Level.objects.values_list('g1_avgwl_insyllables_l3', flat=True). get(id=1)
            g1_avgl_sentences_inw_l1 = g1Level.objects.values_list('g1_avgl_sentences_inw_l1', flat=True). get(id=1)
            g1_avgl_sentences_inw_l2 = g1Level.objects.values_list('g1_avgl_sentences_inw_l2', flat=True). get(id=1)
            g1_avgl_sentences_inw_l3 = g1Level.objects.values_list('g1_avgl_sentences_inw_l3', flat=True). get(id=1)
            g1_multisyllabic_wq_l1 = g1Level.objects.values_list('g1_multisyllabic_wq_l1', flat=True). get(id=1)
            g1_multisyllabic_wq_l2 = g1Level.objects.values_list('g1_multisyllabic_wq_l2', flat=True). get(id=1)
            g1_multisyllabic_wq_l3 = g1Level.objects.values_list('g1_multisyllabic_wq_l3', flat=True). get(id=1)
            g1_compw_q_l1 = g1Level.objects.values_list('g1_compw_q_l1', flat=True). get(id=1)
            g1_compw_q_l2 = g1Level.objects.values_list('g1_compw_q_l2', flat=True). get(id=1)
            g1_compw_q_l3 = g1Level.objects.values_list('g1_compw_q_l3', flat=True). get(id=1)
            g1_rarew_q_l1 = g1Level.objects.values_list('g1_rarew_q_l1', flat=True). get(id=1)
            g1_rarew_q_l2 = g1Level.objects.values_list('g1_rarew_q_l2', flat=True). get(id=1)
            g1_rarew_q_l3 = g1Level.objects.values_list('g1_rarew_q_l3', flat=True). get(id=1)
            g1_complexw_q_l1 = g1Level.objects.values_list('g1_complexw_q_l1', flat=True). get(id=1)
            g1_complexw_q_l2 = g1Level.objects.values_list('g1_complexw_q_l2', flat=True). get(id=1)
            g1_complexw_q_l3 = g1Level.objects.values_list('g1_complexw_q_l3', flat=True). get(id=1)
            g1_lexical_div_q_l1 = g1Level.objects.values_list('g1_lexical_div_q_l1', flat=True). get(id=1)
            g1_lexical_div_q_l2 = g1Level.objects.values_list('g1_lexical_div_q_l2', flat=True). get(id=1)
            g1_lexical_div_q_l3 = g1Level.objects.values_list('g1_lexical_div_q_l3', flat=True). get(id=1)



            ###Levels for Grade2 ###
            g2_word_q_l1 = g2Level.objects.values_list('g2_word_q_l1', flat=True). get(id=1)
            g2_word_q_l2 = g2Level.objects.values_list('g2_word_q_l2', flat=True). get(id=1)
            g2_sentence_q_l1 = g2Level.objects.values_list('g2_sentence_q_l1', flat=True). get(id=1)
            g2_sentence_q_l2 = g2Level.objects.values_list('g2_sentence_q_l2', flat=True). get(id=1)
            g2_avgwl_insyllables_l1 = g2Level.objects.values_list('g2_avgwl_insyllables_l1', flat=True). get(id=1)
            g2_avgwl_insyllables_l2 = g2Level.objects.values_list('g2_avgwl_insyllables_l2', flat=True). get(id=1)
            g2_avgl_sentences_inw_l1 = g2Level.objects.values_list('g2_avgl_sentences_inw_l1', flat=True). get(id=1)
            g2_avgl_sentences_inw_l2 = g2Level.objects.values_list('g2_avgl_sentences_inw_l2', flat=True). get(id=1)
            g2_multisyllabic_wq_l1 = g2Level.objects.values_list('g2_multisyllabic_wq_l1', flat=True). get(id=1)
            g2_multisyllabic_wq_l2 = g2Level.objects.values_list('g2_multisyllabic_wq_l2', flat=True). get(id=1)
            g2_compw_q_l1 = g2Level.objects.values_list('g2_compw_q_l1', flat=True). get(id=1)
            g2_compw_q_l2 = g2Level.objects.values_list('g2_compw_q_l2', flat=True). get(id=1)
            g2_rarew_q_l1 = g2Level.objects.values_list('g2_rarew_q_l1', flat=True). get(id=1)
            g2_rarew_q_l2 = g2Level.objects.values_list('g2_rarew_q_l2', flat=True). get(id=1)
            g2_complexw_q_l1 = g2Level.objects.values_list('g2_complexw_q_l1', flat=True). get(id=1)
            g2_complexw_q_l2 = g2Level.objects.values_list('g2_complexw_q_l2', flat=True). get(id=1)
            g2_lexical_div_q_l1 = g2Level.objects.values_list('g2_lexical_div_q_l1', flat=True). get(id=1)
            g2_lexical_div_q_l2 = g2Level.objects.values_list('g2_lexical_div_q_l2', flat=True). get(id=1)


            ###Levels for Grade3
            g3_word_q_l1 = g3Level.objects.values_list('g3_word_q_l1', flat=True). get(id=1)
            g3_word_q_l2 = g3Level.objects.values_list('g3_word_q_l2', flat=True). get(id=1)
            g3_sentence_q_l1 = g3Level.objects.values_list('g3_sentence_q_l1', flat=True). get(id=1)
            g3_sentence_q_l2 = g3Level.objects.values_list('g3_sentence_q_l2', flat=True). get(id=1)
            g3_avgwl_insyllables_l1 = g3Level.objects.values_list('g3_avgwl_insyllables_l1', flat=True). get(id=1)
            g3_avgwl_insyllables_l2 = g3Level.objects.values_list('g3_avgwl_insyllables_l2', flat=True). get(id=1)
            g3_avgl_sentences_inw_l1 = g3Level.objects.values_list('g3_avgl_sentences_inw_l1', flat=True). get(id=1)
            g3_avgl_sentences_inw_l2 = g3Level.objects.values_list('g3_avgl_sentences_inw_l2', flat=True). get(id=1)
            g3_multisyllabic_wq_l1 = g3Level.objects.values_list('g3_multisyllabic_wq_l1', flat=True). get(id=1)
            g3_multisyllabic_wq_l2 = g3Level.objects.values_list('g3_multisyllabic_wq_l2', flat=True). get(id=1)
            g3_compw_q_l1 = g3Level.objects.values_list('g3_compw_q_l1', flat=True). get(id=1)
            g3_compw_q_l2 = g3Level.objects.values_list('g3_compw_q_l2', flat=True). get(id=1)
            g3_rarew_q_l1 = g3Level.objects.values_list('g3_rarew_q_l1', flat=True). get(id=1)
            g3_rarew_q_l2 = g3Level.objects.values_list('g3_rarew_q_l2', flat=True). get(id=1)
            g3_complexw_q_l1 = g3Level.objects.values_list('g3_complexw_q_l1', flat=True). get(id=1)
            g3_complexw_q_l2 = g3Level.objects.values_list('g3_complexw_q_l2', flat=True). get(id=1)
            g3_lexical_div_q_l1 = g3Level.objects.values_list('g3_lexical_div_q_l1', flat=True). get(id=1)
            g3_lexical_div_q_l2 = g3Level.objects.values_list('g3_lexical_div_q_l2', flat=True). get(id=1)


            ###Levels for Grade4
            g4_word_q_l1 = g4Level.objects.values_list('g4_word_q_l1', flat=True). get(id=1)
            g4_word_q_l2 = g4Level.objects.values_list('g4_word_q_l2', flat=True). get(id=1)
            g4_sentence_q_l1 = g4Level.objects.values_list('g4_sentence_q_l1', flat=True). get(id=1)
            g4_sentence_q_l2 = g4Level.objects.values_list('g4_sentence_q_l2', flat=True). get(id=1)
            g4_avgwl_insyllables_l1 = g4Level.objects.values_list('g4_avgwl_insyllables_l1', flat=True). get(id=1)
            g4_avgwl_insyllables_l2 = g4Level.objects.values_list('g4_avgwl_insyllables_l2', flat=True). get(id=1)
            g4_avgl_sentences_inw_l1 = g4Level.objects.values_list('g4_avgl_sentences_inw_l1', flat=True). get(id=1)
            g4_avgl_sentences_inw_l2 = g4Level.objects.values_list('g4_avgl_sentences_inw_l2', flat=True). get(id=1)
            g4_multisyllabic_wq_l1 = g4Level.objects.values_list('g4_multisyllabic_wq_l1', flat=True). get(id=1)
            g4_multisyllabic_wq_l2 = g4Level.objects.values_list('g4_multisyllabic_wq_l2', flat=True). get(id=1)
            g4_compw_q_l1 = g4Level.objects.values_list('g4_compw_q_l1', flat=True). get(id=1)
            g4_compw_q_l2 = g4Level.objects.values_list('g4_compw_q_l2', flat=True). get(id=1)
            g4_rarew_q_l1 = g4Level.objects.values_list('g4_rarew_q_l1', flat=True). get(id=1)
            g4_rarew_q_l2 = g4Level.objects.values_list('g4_rarew_q_l2', flat=True). get(id=1)
            g4_complexw_q_l1 = g4Level.objects.values_list('g4_complexw_q_l1', flat=True). get(id=1)
            g4_complexw_q_l2 = g4Level.objects.values_list('g4_complexw_q_l2', flat=True). get(id=1)
            g4_lexical_div_q_l1 = g4Level.objects.values_list('g4_lexical_div_q_l1', flat=True). get(id=1)
            g4_lexical_div_q_l2 = g4Level.objects.values_list('g4_lexical_div_q_l2', flat=True). get(id=1)



            if (syllables_avg <= g1_avgwl_insyllables_l3 and multisyllabic_wq  <= g1_multisyllabic_wq_l3 and complex_w_q <= g1_complexw_q_l3 and compound_w_q <= g1_compw_q_l3) or (syllables_avg > g1_avgwl_insyllables_l3 and syllables_avg <= g2_avgwl_insyllables_l2 and multisyllabic_wq  <= g1_multisyllabic_wq_l3 and rareword_q <= g1_rarew_q_l3) or (syllables_avg <= g1_avgwl_insyllables_l3 and sentence_avg <= g1_avgl_sentences_inw_l3 and compound_w_q <= g1_compw_q_l3):
                    
                    level_result = "1 класс"
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    messages.info(request, 'жүктөлдү')

            elif (syllables_avg > g1_avgwl_insyllables_l3 and multisyllabic_wq  <= g1_multisyllabic_wq_l3 and compound_w_q <= g1_compw_q_l3 and rareword_q <= g1_rarew_q_l3) or (words_q <= g1_word_q_l3 and syllables_avg <= g1_avgwl_insyllables_l3 and compound_w_q <= g1_compw_q_l3 and rareword_q <= g1_rarew_q_l3):
                    
                    level_result = "1 класс"
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    messages.info(request, 'жүктөлдү')

            elif (syllables_avg > g1_avgwl_insyllables_l3 and syllables_avg <= g2_avgwl_insyllables_l2  and rareword_q > g1_rarew_q_l3 and rareword_q <= g2_rarew_q_l2) or (words_q > g1_word_q_l3 and words_q <= g2_word_q_l2 and syllables_avg > g1_avgwl_insyllables_l3 and syllables_avg <= g2_avgwl_insyllables_l2 and multisyllabic_wq > g1_multisyllabic_wq_l3 and multisyllabic_wq  <= g2_multisyllabic_wq_l2) or (multisyllabic_wq > g1_multisyllabic_wq_l3 and multisyllabic_wq  <= g2_multisyllabic_wq_l2 and rareword_q > g1_rarew_q_l3 and rareword_q <= g2_rarew_q_l2 and complex_w_q > g1_complexw_q_l3 and complex_w_q <= g3_complexw_q_l1) or (compound_w_q > g1_compw_q_l3 and compound_w_q <= g2_compw_q_l2 and rareword_q > g1_rarew_q_l3 and rareword_q <= g2_rarew_q_l2):
                    
                    level_result = "2 класс"
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    messages.info(request, 'жүктөлдү')

            elif (multisyllabic_wq > g1_multisyllabic_wq_l3 and multisyllabic_wq  <= g2_multisyllabic_wq_l2 and compound_w_q > g1_compw_q_l3 and compound_w_q <= g2_compw_q_l2) or (words_q > g1_word_q_l3 and words_q <= g2_word_q_l2 and multisyllabic_wq > g1_multisyllabic_wq_l3 and multisyllabic_wq  <= g2_multisyllabic_wq_l2) or (words_q > g1_word_q_l3 and multisyllabic_wq > g1_multisyllabic_wq_l3 and multisyllabic_wq  <= g2_multisyllabic_wq_l2 and compound_w_q > g1_compw_q_l3 and rareword_q > g1_rarew_q_l3 and rareword_q <= g2_rarew_q_l2):
                    
                    level_result = "2 класс"
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    messages.info(request, 'жүктөлдү')

            elif (words_q < g2_word_q_l2  and  sentence_q < g2_sentence_q_l2 and syllables_avg > g1_avgwl_insyllables_l3 and syllables_avg <= g2_avgwl_insyllables_l2 and sentence_avg > g1_avgl_sentences_inw_l3 and sentence_avg <= g2_avgl_sentences_inw_l2 and compound_w_q > g1_compw_q_l3 and compound_w_q <= g2_compw_q_l2 ) or (words_q > g1_word_q_l3 and words_q <= g2_word_q_l2  and  sentence_q >= g2_sentence_q_l2 and syllables_avg > g1_avgwl_insyllables_l3 and syllables_avg <= g2_avgwl_insyllables_l2 and sentence_avg <= g2_avgl_sentences_inw_l2 and compound_w_q <= g2_compw_q_l2 ) or (words_q > g2_word_q_l2  and  sentence_q > g2_sentence_q_l2 and syllables_avg > g1_avgwl_insyllables_l3 and syllables_avg <= g2_avgwl_insyllables_l2 and sentence_avg <= g2_avgl_sentences_inw_l2 and compound_w_q <= g2_compw_q_l2 ) or (words_q > g1_word_q_l3 and words_q <= g2_word_q_l2  and  sentence_q > g2_sentence_q_l2 and syllables_avg > g1_avgwl_insyllables_l3 and syllables_avg <= g2_avgwl_insyllables_l2 and sentence_avg > g1_avgl_sentences_inw_l3 and sentence_avg <= g2_avgl_sentences_inw_l2 and multisyllabic_wq > g1_multisyllabic_wq_l3 and multisyllabic_wq <= g2_multisyllabic_wq_l2 ):
                    
                    level_result = "2 класс: текстти  текшериш керек"
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    messages.info(request, 'жүктөлдү')


            elif (syllables_avg > g2_avgwl_insyllables_l2 and multisyllabic_wq > g2_multisyllabic_wq_l2 and multisyllabic_wq  <= g3_multisyllabic_wq_l2) or (sentence_avg > g2_avgl_sentences_inw_l2 and sentence_avg <= g3_avgl_sentences_inw_l2 and compound_w_q > g2_compw_q_l2 and compound_w_q <= g3_compw_q_l2 and rareword_q > g2_rarew_q_l2 and rareword_q <= g3_rarew_q_l2) or (words_q > g4_word_q_l1 and compound_w_q > g2_compw_q_l2 and compound_w_q <= g3_compw_q_l2 and rareword_q > g2_rarew_q_l2 and rareword_q <= g3_rarew_q_l2):
                    
                    level_result = "3 класс"
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    messages.info(request, 'жүктөлдү')
            
            elif (words_q > g2_word_q_l2 and words_q <= g3_word_q_l2 and  sentence_q > g2_sentence_q_l2 and sentence_q <= g3_sentence_q_l2  and sentence_avg > g2_avgl_sentences_inw_l2  and sentence_avg <= g3_avgl_sentences_inw_l2 and compound_w_q > g2_compw_q_l2 and compound_w_q > g3_compw_q_l2) or (words_q < g2_word_q_l2  and  sentence_q < g2_sentence_q_l2  and sentence_avg > g2_avgl_sentences_inw_l2  and sentence_avg <= g3_avgl_sentences_inw_l2 and multisyllabic_wq > g2_multisyllabic_wq_l2 and multisyllabic_wq <= g3_multisyllabic_wq_l2 ) or (words_q > g3_word_q_l2 and  sentence_q > g3_sentence_q_l2  and sentence_avg > g2_avgl_sentences_inw_l2 and syllables_avg > g2_avgwl_insyllables_l2 and syllables_avg <= g3_avgwl_insyllables_l2 and sentence_avg <= g3_avgl_sentences_inw_l2 and multisyllabic_wq > g2_multisyllabic_wq_l2 and multisyllabic_wq <= g3_multisyllabic_wq_l2 and compound_w_q > g2_compw_q_l2 and compound_w_q <= g3_compw_q_l2) or (words_q < g3_word_q_l1 and  sentence_q < g3_sentence_q_l1  and sentence_avg > g2_avgl_sentences_inw_l2 and sentence_avg <= g3_avgl_sentences_inw_l2 and syllables_avg > g2_avgwl_insyllables_l2 and syllables_avg <= g3_avgwl_insyllables_l2 and compound_w_q > g2_compw_q_l2 and compound_w_q <= g3_compw_q_l2) or (words_q > g2_word_q_l2 and words_q <= g3_word_q_l2 and  sentence_q < g3_sentence_q_l1 and syllables_avg > g2_avgwl_insyllables_l2 and syllables_avg <= g3_avgwl_insyllables_l2  and sentence_avg > g3_avgl_sentences_inw_l2  and multisyllabic_wq > g2_multisyllabic_wq_l2 and multisyllabic_wq <= g3_multisyllabic_wq_l2) or (words_q > g2_word_q_l2 and words_q <= g3_word_q_l2 and  sentence_q > g3_sentence_q_l2 and syllables_avg > g2_avgwl_insyllables_l2 and syllables_avg <= g3_avgwl_insyllables_l2  and multisyllabic_wq > g2_multisyllabic_wq_l2 and multisyllabic_wq <= g3_multisyllabic_wq_l2):
                    
                    level_result = "3 класс: текстти  текшериш керек"
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    messages.info(request, 'жүктөлдү')
            
            elif (syllables_avg > g3_avgwl_insyllables_l2 and multisyllabic_wq > g3_multisyllabic_wq_l2 and  compound_w_q > g3_compw_q_l2) or (words_q > g1_word_q_l2 and syllables_avg > g3_avgwl_insyllables_l2) or (words_q > g3_word_q_l1 and compound_w_q > g3_compw_q_l2  and rareword_q > g3_rarew_q_l2) or (words_q > g3_word_q_l2 and rareword_q > g3_rarew_q_l2):
                    
                    level_result = "4 класс"
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    messages.info(request, 'жүктөлдү')

            elif (words_q > g3_word_q_l1  and words_q < g4_word_q_l1 and  sentence_q > g3_sentence_q_l1 and sentence_q < g4_sentence_q_l1 and syllables_avg > g3_avgwl_insyllables_l2 and multisyllabic_wq > g3_multisyllabic_wq_l2 and rareword_q > g3_rarew_q_l2) or (words_q > g3_word_q_l2  and sentence_q > g3_sentence_q_l2 and multisyllabic_wq > g3_multisyllabic_wq_l2 and compound_w_q > g3_compw_q_l2 and  rareword_q < g4_rarew_q_l1):
                    
                    level_result = "4 класс: текстти  текшериш керек"
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    messages.info(request, 'жүктөлдү')

            
            else:
                    level_result = "Текст  " + str(words_q)+ " сөздөн турат" + " бирок кайра текшерилиши керек ..."
                    book = kgText(book_title=title, book_author=author,book_text=message, sentence_q=sentence_q, words_q=words_q, syllables_avg=syllables_avg, sentence_avg=sentence_avg, multisyllabic_wq=multisyllabic_wq, compound_w_q=compound_w_q, 
                                rareword_q=rareword_q, rareword_p=rareword_p, fw_q=fw_q, fw_p=fw_p, uniq_w=uniquew_q, lexical_div=lexical_d, level_result=level_result, all_compound_words_p = all_compound_words_p, complex_w_q=complex_w_q)
                    book.save()
                    
                    messages.error(request, 'текшерилиш керек')





            

            
            context = {'words_q':words_q, 'sentence_q':sentence_q, 'syllables':syllables, 'syllables_avg':syllables_avg, 'sentence_avg':sentence_avg, 'multisyllabic_wq':multisyllabic_wq, 'longw_frequencies':longw_frequencies, 'uniquew_q':uniquew_q,
                        'w_frequencies': w_frequencies, 'compound_w_q':compound_w_q, 'lcword_frequencies':lcword_frequencies, 'rareword_frequencies':rareword_frequencies, 'lexical_d':lexical_d,
                        'rareword_q':rareword_q, 'fw_frequencies':fw_frequencies,'fw_p':fw_p, 'g1_word_q_l1':g1_word_q_l1, 'g1_word_q_l2':g1_word_q_l2, 'g1_word_q_l3':g1_word_q_l3,
                        'g1_sentence_q_l1':g1_sentence_q_l1, 'g1_sentence_q_l2':g1_sentence_q_l2, 'g1_sentence_q_l3':g1_sentence_q_l3, 'level_result':level_result,
                        'g1_avgwl_insyllables_l1':g1_avgwl_insyllables_l1, 'g1_avgwl_insyllables_l2':g1_avgwl_insyllables_l2, 'g1_avgwl_insyllables_l3':g1_avgwl_insyllables_l3,
                        'g1_avgl_sentences_inw_l1':g1_avgl_sentences_inw_l1, 'g1_avgl_sentences_inw_l2':g1_avgl_sentences_inw_l2, 'g1_avgl_sentences_inw_l3':g1_avgl_sentences_inw_l3,
                        'g1_multisyllabic_wq_l1':g1_multisyllabic_wq_l1, 'g1_multisyllabic_wq_l2':g1_multisyllabic_wq_l2, 'g1_multisyllabic_wq_l3':g1_multisyllabic_wq_l3, 'g1_compw_q_l1':g1_compw_q_l1, 'g1_compw_q_l2':g1_compw_q_l2,
                        'g1_compw_q_l3':g1_compw_q_l3, 'g1_rarew_q_l1':g1_rarew_q_l1, 'g1_rarew_q_l2':g1_rarew_q_l2, 'g1_rarew_q_l3':g1_rarew_q_l3, 'g2_word_q_l1':g2_word_q_l1, 'g2_word_q_l2':g2_word_q_l2,
                        'g2_sentence_q_l1':g2_sentence_q_l1, 'g2_sentence_q_l2':g2_sentence_q_l2, 'g2_avgwl_insyllables_l1':g2_avgwl_insyllables_l1, 'g2_avgwl_insyllables_l2':g2_avgwl_insyllables_l2,
                        'g2_avgl_sentences_inw_l1':g2_avgl_sentences_inw_l1, 'g2_avgl_sentences_inw_l2':g2_avgl_sentences_inw_l2, 'g2_multisyllabic_wq_l1':g2_multisyllabic_wq_l1, 'g2_multisyllabic_wq_l2':g2_multisyllabic_wq_l2, 'g2_compw_q_l1':g2_compw_q_l1, 'g2_compw_q_l2':g2_compw_q_l2, 'g2_rarew_q_l1':g2_rarew_q_l1, 'g2_rarew_q_l2':g2_rarew_q_l2, 'g3_word_q_l1':g3_word_q_l1, 'g3_word_q_l2':g3_word_q_l2,
                        'g3_sentence_q_l1':g3_sentence_q_l1, 'g3_sentence_q_l2':g3_sentence_q_l2, 'g3_avgwl_insyllables_l1':g3_avgwl_insyllables_l1, 'g3_avgwl_insyllables_l2':g3_avgwl_insyllables_l2, 'g3_avgl_sentences_inw_l1':g3_avgl_sentences_inw_l1, 'g3_avgl_sentences_inw_l2':g3_avgl_sentences_inw_l2, 'g3_multisyllabic_wq_l1':g3_multisyllabic_wq_l1, 'g3_multisyllabic_wq_l2':g3_multisyllabic_wq_l2, 'g3_compw_q_l1':g3_compw_q_l1, 'g3_compw_q_l2':g3_compw_q_l2, 'g3_rarew_q_l1':g3_rarew_q_l1, 'g3_rarew_q_l2':g3_rarew_q_l2,
                         'g4_word_q_l1':g4_word_q_l1, 'g4_word_q_l2':g4_word_q_l2, 'g4_sentence_q_l1':g4_sentence_q_l1, 'g4_sentence_q_l2':g4_sentence_q_l2, 'g4_avgwl_insyllables_l1':g4_avgwl_insyllables_l1, 'g4_avgwl_insyllables_l2':g4_avgwl_insyllables_l2,'g4_avgl_sentences_inw_l1':g4_avgl_sentences_inw_l1, 'g4_avgl_sentences_inw_l2':g4_avgl_sentences_inw_l2, 'g4_multisyllabic_wq_l1':g4_multisyllabic_wq_l1, 'g4_multisyllabic_wq_l2':g4_multisyllabic_wq_l2, 'g4_compw_q_l1':g4_compw_q_l1, 'g4_compw_q_l2':g4_compw_q_l2, 'g4_rarew_q_l1':g4_rarew_q_l1, 'g4_rarew_q_l2':g4_rarew_q_l2, 'compound_word_frequencies':compound_word_frequencies, 'complex_w_q':complex_w_q, 'all_compound_words_p':all_compound_words_p,
                         'g1_complexw_q_l1':g1_complexw_q_l1, 'g1_complexw_q_l2':g1_complexw_q_l2, 'g1_complexw_q_l3':g1_complexw_q_l3, 'g2_complexw_q_l1':g2_complexw_q_l1, 'g2_complexw_q_l2':g2_complexw_q_l2, 'g3_complexw_q_l1':g3_complexw_q_l1, 'g3_complexw_q_l2':g3_complexw_q_l2, 'g4_complexw_q_l1':g4_complexw_q_l1, 'g4_complexw_q_l2':g4_complexw_q_l2, 'g1_lexical_div_q_l1':g1_lexical_div_q_l1, 'g1_lexical_div_q_l2':g1_lexical_div_q_l2, 'g1_lexical_div_q_l3':g1_lexical_div_q_l3, 'g2_lexical_div_q_l1':g2_lexical_div_q_l1, 'g2_lexical_div_q_l2':g2_lexical_div_q_l2, 'g3_lexical_div_q_l1':g3_lexical_div_q_l1, 'g3_lexical_div_q_l2':g3_lexical_div_q_l2, 'g4_lexical_div_q_l1':g4_lexical_div_q_l1, 'g4_lexical_div_q_l2':g4_lexical_div_q_l2}
            
            return render(request, 'kg/result.html', context)
             
        
        
        
        
        else:
                messages.error(request, 'Туура эмес: Кыргызча текст жүктөгүлө!!!')
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)