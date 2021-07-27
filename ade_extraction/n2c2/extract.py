import os
from sys import path
path.append(os.getcwd())
from ade_extraction.n2c2.utils import extract_mention_from_sentence
from data_utils.n2c2.ehr import Corpora
from data_utils.n2c2.n2c2_corpus import N2C2
from data_utils.n2c2.preprocessing import tokenize_sentence
from data_utils.n2c2.tagging import *
from nltk.tokenize import word_tokenize

def replace_tokens_with_ADE_type1(drug, 
                                  tok_text, 
                                  entity_start, 
                                  start, 
                                  end, 
                                  sentence, 
                                  segment="BIO"):
    mstart = int(drug[1])                  
    mend = int(drug[0]) 
    m_str = drug[3]
    sentence_2 = tokenize_sentence(sentence) 
    sentence_2 = tagging_sequence('1', m_str, LABELSET[drug[2]], tok_text, sentence_2, mstart, entity_start, start, end, sentence, '', segment)                                
    return sentence_2
	
def generate_contexts_n2c2(m, 
                           text, 
                           id_mention, 
                           drug_sr, 
                           toks_sr, 
                           type_sr, 
                           sec_sr, 
                           start_sr, 
                           len_sr, 
                           n2c2_guess, 
                           n2c2_rel):
    drug_source_mention = []   
    ad = dict()
    for dm, tm, tym, sm, stm, lm, tokens, section, start, len_s, drug, start_s, end_s, sentence in zip(drug_sr, toks_sr, type_sr, sec_sr, start_sr, len_sr, n2c2_guess.t_toks_mention, n2c2_guess.t_section_mention, n2c2_guess.t_start_mention, n2c2_guess.t_len_mention, n2c2_guess.t_drug_mention, n2c2_guess.t_start_sentence_mention, n2c2_guess.t_len_sentence_mention, n2c2_guess.t_sentence_input_mention):
        if len(set(dm))==0:
            continue
        if list(set(dm))[0]==m:
            for tok, typ, st, le in zip(tm, tym, stm, lm):
                dr = (str(le), str(st), "Drug", ' '.join(word_tokenize(text[int(st):int(le)])), "T"+str(id_mention))
                drug_source_mention.append(dr)
                if typ=='Drug_rel':
                    ad[(dr[0], dr[1], dr[2], dr[3])] = "T"+str(id_mention)
                    sentence_2 = replace_tokens_with_ADE_type1(dr, tokens, start, start_s, end_s, sentence)
                    n2c2_rel.t_sentence_relation.append(sentence_2)
                    n2c2_rel.t_toks_relation.append(tokens)
                    n2c2_rel.t_segment_relation.append(['O']*len(tokens))
                    n2c2_rel.t_start_relation.append(start)
                    n2c2_rel.t_section_relation.append(section)
                    n2c2_rel.t_len_relation.append(len_s)
                    n2c2_rel.t_ade.append(dr)
                    n2c2_rel.t_modifiers.append([])
                    n2c2_rel.t_drug_relation.append(drug)
                id_mention+=1
    return drug_source_mention, id_mention, n2c2_rel, ad
	
def extract_source_mention_n2c2(N2C2_test, gold="data/ADR/N2C2/test/"):
    drug_sources, toks_sources, type_sources, sec_sources, start_sources, len_sources = extract_mention_from_sentence(N2C2_test.t_drug_mention, 
                                                                                                                      N2C2_test.t_toks_mention, 
                                                                                                                      N2C2_test.t_segment_mention, 
                                                                                                                      N2C2_test.t_section_mention, 
                                                                                                                      N2C2_test.t_start_mention, 
                                                                                                                      N2C2_test.t_len_mention)

    dict_drug = {}
    n2c2_rel = N2C2()
    list_id_mentions = {}
    ade_set = {}
    files = Corpora(gold, 2)  
    for i in range(len(files.docs)):       
        sentence_file = files.docs[i].basename
        text = files.docs[i]._get_text()
        key = sentence_file.replace('.ann', '')
        ade_source_mention, id_mention, n2c2_rel, ad = generate_contexts_n2c2(key, 
                                                                              text,
                                                                              1, 
                                                                              drug_sources, 
                                                                              toks_sources, 
                                                                              type_sources, 
                                                                              sec_sources, 
                                                                              start_sources, 
                                                                              len_sources, 
                                                                              N2C2_test, 
                                                                              n2c2_rel)
        dict_drug[key] = ade_source_mention 
        list_id_mentions[key] = id_mention
        ade_set[key] = ad
    return n2c2_rel, dict_drug, list_id_mentions, ade_set
	
def extract_modifiers_relation_from_label_n2c2(m, 
                                               text, 
                                               dict_ade, 
                                               id_mention, 
                                               TAC_guess, 
                                               drug_relation, 
                                               toks_relation, 
                                               type_relation, 
                                               sec_relation, 
                                               start_relation, 
                                               len_relation):
    id_relation = 1
    modifiers = []
    relations = []
    m_dict = []
    for ade, drug_r, toks_r, type_r, sec_r, start_r, len_r in zip(TAC_guess.t_ade, drug_relation, toks_relation,type_relation, sec_relation, start_relation, len_relation):
        if len(set(drug_r))==0:
            continue
        if list(set(drug_r))[0]==m:
            arg1 = dict_ade[(ade[0], ade[1], ade[2], ade[3])]

            for tok, typ, st, le in zip(toks_r, type_r, start_r, len_r): 
                relation_type = typ + '-Drug'
                
                #if (str(le), str(st), modifier_type, tok, sec) not in m_dict:
                arg2 = "T"+str(id_mention) 

                id_mention = id_mention + 1
                    
                modifier = (str(le), str(st), typ, ' '.join(word_tokenize(text[int(st):int(le)])), arg2)
                
                modifiers.append(modifier)
                relations.append(("R"+str(id_relation), arg1, arg2, relation_type))

                id_relation = id_relation + 1
    #print ("==============")
    return relations, modifiers
	
def extract_att_relation_n2c2(N2C2_test, ade_set, list_id_mentions, gold="data/ADR/N2C2/test/"):
    drug_att_rel, toks_att_rel, type_att_rel, sec_att_rel, start_att_rel, len_att_rel = extract_mention_from_sentence(N2C2_test.t_drug_relation, 
                                                                                                                      N2C2_test.t_toks_relation, 
                                                                                                                      N2C2_test.t_segment_relation, 
                                                                                                                      N2C2_test.t_section_relation, 
                                                                                                                      N2C2_test.t_start_relation, 
                                                                                                                      N2C2_test.t_len_relation)

    dict_modifiers = {}
    dict_relations = {}
    files = Corpora(gold, 2)   
    for i in range(len(files.docs)): 
        sentence_file = files.docs[i].basename
        text = files.docs[i]._get_text()
        key = sentence_file.replace('.ann', '')
        relations, modifiers = extract_modifiers_relation_from_label_n2c2(key, 
                                                                          text, 
                                                                          ade_set[key], 
                                                                          list_id_mentions[key] +1, 
                                                                          N2C2_test, 
                                                                          drug_att_rel, 
                                                                          toks_att_rel, 
                                                                          type_att_rel, 
                                                                          sec_att_rel, 
                                                                          start_att_rel, 
                                                                          len_att_rel)
        dict_modifiers[key] = modifiers
        dict_relations[key] = relations
    return dict_modifiers, dict_relations
    
