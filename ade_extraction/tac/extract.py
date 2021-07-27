import os
from sys import path
path.append(os.getcwd())
from data_utils.tac.tagging import generate_source_context
from ade_extraction.tac.utils import extract_mention_from_sentences
from data_utils.tac.drug_label import xml_files, read
from data_utils.tac.tac_corpus import TAC

def generate_contexts_tac(m, 
                          id_mention, 
                          drug_sr, 
                          toks_sr, 
                          type_sr, 
                          sec_sr, 
                          start_sr, 
                          len_sr, 
                          TAC_guess, 
                          tac_rel, 
                          sections):
    ade_source_mention = []   
    ad = dict()
    for dm, tm, tym, sm, stm, lm, tokens, section, start, len_s, drug, start_s, end_s, sentence in zip(drug_sr, toks_sr, type_sr, sec_sr, start_sr, len_sr, TAC_guess.t_toks_mention, TAC_guess.t_section_mention, TAC_guess.t_start_mention, TAC_guess.t_len_mention, TAC_guess.t_drug_mention, TAC_guess.t_start_sentence_mention, TAC_guess.t_len_sentence_mention, TAC_guess.t_sentence_input_mention):
        if len(set(dm))==0:
            continue
        if list(set(dm))[0]==m:
            for tok, typ, sec, st, le in zip(tm, tym, sm, stm, lm):
                ade = (str(le), str(st), "AdverseReaction", tok, sec, "M"+str(id_mention))
                ade_source_mention.append(ade)
                if typ=='AdverseReaction_rel':
                    section_t = ''
                    for s in sections:
                        if s.id==sec:
                            section_t=s.text
                            break
                    ad[(ade[0], ade[1], ade[2], ade[3], ade[4])] = "M"+str(id_mention)
                    sentence_2 = generate_source_context(ade, tokens, start, start_s, end_s, sentence, section_t)
                    tac_rel.t_sentence_relation.append(sentence_2)
                    tac_rel.t_toks_relation.append(tokens)
                    tac_rel.t_segment_relation.append(['O']*len(tokens))
                    tac_rel.t_start_relation.append(start)
                    tac_rel.t_section_relation.append(section)
                    tac_rel.t_len_relation.append(len_s)
                    tac_rel.t_ade.append(ade)
                    tac_rel.t_modifiers.append([])
                    tac_rel.t_drug_relation.append(drug)
                id_mention+=1
    return ade_source_mention, id_mention, tac_rel, ad
	
def extract_source_mention_tac(tac_test, gold_xml="data/ADR/TAC/gold_xml/"): 
    drug_sources, toks_sources, type_sources, sec_sources, start_sources, len_sources = extract_mention_from_sentences(tac_test.t_drug_mention, 
                                                                                                                      tac_test.t_toks_mention, 
                                                                                                                      tac_test.t_segment_mention, 
                                                                                                                      tac_test.t_section_mention, 
                                                                                                                      tac_test.t_start_mention, 
                                                                                                                      tac_test.t_len_mention)

    guess_files = xml_files(gold_xml)
    dict_ade = {}
    tac_rel = TAC()
    list_id_mentions = []
    ade_set = []
    for key, value in zip(guess_files.keys(), guess_files.values()):
        label = read(value)
        sections = label.sections
        ade_source_mention, id_mention, tac_rel, ad = generate_contexts_tac(key, 
                                                                        1, 
                                                                        drug_sources, 
                                                                        toks_sources, 
                                                                        type_sources, 
                                                                        sec_sources, 
                                                                        start_sources, 
                                                                        len_sources, 
                                                                        tac_test, 
                                                                        tac_rel, sections)
        dict_ade[key] = ade_source_mention 
        list_id_mentions.append(id_mention)
        ade_set.append(ad)
    return tac_rel, dict_ade, list_id_mentions, ade_set
	
def extract_modifiers_relation_from_label_tac(m, 
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
    for ade, drug_r, toks_r, type_r, sec_r, start_r, len_r in zip(TAC_guess.t_ade, drug_relation, toks_relation,type_relation, sec_relation, start_relation, len_relation):
        if len(set(drug_r))==0:
            continue
        if list(set(drug_r))[0]==m:
            arg1 = dict_ade[(ade[0], ade[1], ade[2], ade[3], ade[4])]
            for tok, typ, sec, st, le in zip(toks_r, type_r, sec_r, start_r, len_r): 
                
                modifier_type = typ.split('_')[0]
                relation_type = typ.split('_')[1]

                arg2 = "M"+str(id_mention) 

                id_mention = id_mention + 1
                    
                modifier = (str(le), str(st), modifier_type, tok, sec, arg2)
                
                modifiers.append(modifier)
                relations.append(("RL"+str(id_relation), arg1, arg2, relation_type))

                id_relation = id_relation + 1

    return relations, modifiers
	
def extract_att_rel_tac(tac_test, 
                        list_id_mentions, 
                        ade_set, 
                        gold_xml="data/ADR/TAC/gold_xml/"):
    drug_att_rel, toks_att_rel, type_att_rel, sec_att_rel, start_att_rel, len_att_rel = extract_mention_from_sentences(tac_test.t_drug_relation, 
                                                                                                                      tac_test.t_toks_relation, 
                                                                                                                      tac_test.t_segment_relation, 
                                                                                                                      tac_test.t_section_relation, 
                                                                                                                      tac_test.t_start_relation, 
                                                                                                                      tac_test.t_len_relation)

    guess_files = xml_files(gold_xml)
    dict_modifiers = {}
    dict_relations = {}
    for key, value, id_mention, ad in zip(guess_files.keys(), guess_files.values(), list_id_mentions, ade_set):
        relations, modifiers = extract_modifiers_relation_from_label_tac(key, 
                                                                         ad, 
                                                                         id_mention +1, 
                                                                         tac_test, 
                                                                         drug_att_rel, 
                                                                         toks_att_rel, 
                                                                         type_att_rel, 
                                                                         sec_att_rel, 
                                                                         start_att_rel, 
                                                                         len_att_rel)
        dict_modifiers[key] = modifiers
        dict_relations[key] = relations
    return dict_modifiers, dict_relations
