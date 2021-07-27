import shutil
from xml.etree import ElementTree
from xml.etree import cElementTree as et
from data_utils.tac.drug_label import xml_files, read
import sys
import xml
import os

def extract_mention_from_sentences(drug, set_toks, ys_bio, section, start, leng):
    data_drug = []
    data_toks = []
    data_ys = []
    data_sec = []
    data_start = []
    data_len = []
    for d, tok, ys, sec, st, le in zip(drug, set_toks, ys_bio, section, start, leng):
        temp_toks = []
        temp_ys = []
        temp_sec = []
        temp_start = []
        temp_len = []
        temp_drug = []
        for i, (t, yb, s, a, b, e) in enumerate(zip(tok, ys, sec, st, le, d)):          
            if yb.startswith('B-'):
                tok_txt = t
                ys_txt = yb[2:]
                sec_txt = s
                start_txt = a
                len_text = b
                drug_text = e
                if (i+1) == len(ys):
                    temp_toks.append(t)
                    temp_ys.append(yb[2:])
                    temp_sec.append(s)
                    temp_start.append(a)
                    temp_len.append(b)
                    temp_drug.append(e)
                    break
                elif ys[i+1].startswith('O') and ys[i-1].startswith('O'):
                    temp_toks.append(t)
                    temp_ys.append(yb[2:])
                    temp_sec.append(s)
                    temp_start.append(a)
                    temp_len.append(b)
                    temp_drug.append(e)
                elif ys[i+1].startswith('B-') and ys[i-1].startswith('B-'):
                    temp_toks.append(t)
                    temp_ys.append(yb[2:])
                    temp_sec.append(s)
                    temp_start.append(a)
                    temp_len.append(b)
                    temp_drug.append(e)
                elif ys[i+1].startswith('DB-') and ys[i-1].startswith('DB-'):
                    temp_toks.append(t)
                    temp_ys.append(yb[2:])
                    temp_sec.append(s)
                    temp_start.append(a)
                    temp_len.append(b)
                    temp_drug.append(e)
                elif ys[i+1].startswith('DI-') and ys[i-1].startswith('DI-'):
                    temp_toks.append(t)
                    temp_ys.append(yb[2:])
                    temp_sec.append(s)
                    temp_start.append(a)
                    temp_len.append(b)
                    temp_drug.append(e)
                elif ys[i+1].startswith('DB-') and ys[i-1].startswith('DI-'):
                    temp_toks.append(t)
                    temp_ys.append(yb[2:])
                    temp_sec.append(s)
                    temp_start.append(a)
                    temp_len.append(b)
                    temp_drug.append(e)
                elif ys[i+1].startswith('DI-') and ys[i-1].startswith('DB-'):
                    temp_toks.append(t)
                    temp_ys.append(yb[2:])
                    temp_sec.append(s)
                    temp_start.append(a)
                    temp_len.append(b)
                    temp_drug.append(e)
                else: 
                    start_n = a
                    for k,j in enumerate(ys[i+1:]):
                        if j.startswith('I-'):
                            tok_txt += ' ' + tok[i+k+1]
                            len_text = le[i+k+1] 
                            start_n = st[i+k+1]
                            
                        else:
                            break
                    len_t = (start_n-start_txt)+len_text
                    temp_toks.append(tok_txt)
                    temp_ys.append(ys_txt)
                    temp_sec.append(sec_txt)
                    temp_start.append(start_txt)
                    temp_len.append(len_t)
                    temp_drug.append(drug_text)
            elif yb.startswith('DB-'):
                tok_txt = t
                ys_txt = yb[3:]
                sec_txt = s
                start_txt = a
                start_t = str(a)
                len_text = b
                drug_text = e
                l = i
                len_text_list = []
                for k,j in enumerate(ys[i+1:]):
                    if j.startswith('DI-'):
                        len_text += le[i+k+1] + 1
                        if (i+k+2) == len(ys):
                            len_text_list.append(len_text)
                    elif j.startswith('DB-'):
                        len_text_list.append(len_text)
                        break
                    else:
                        len_text_list.append(len_text)
                        len_text = 0
                if len(len_text_list)!=0:
                    len_t = str(len_text_list[0])
                    for m in len_text_list[1:]:
                        if m!=0:
                            len_t += ',' + str(m-1)

                    for k,j in enumerate(ys[i+1:]):
                        if j.startswith('DI-'):
                            tok_txt += ' ' + tok[i+k+1]                      
                            if ys[l].startswith('B-') or ys[l].startswith('I-') or ys[l].startswith('O'):
                                start_t += ',' + str(st[i+k+1])                       
                       
                        elif j.startswith('DB-'):
                            break
                        l = l + 1
                    temp_toks.append(tok_txt)
                    temp_ys.append(ys_txt)
                    temp_sec.append(sec_txt)
                    temp_start.append(start_t)
                    temp_len.append(len_t)
                    temp_drug.append(drug_text)
        data_toks.append(temp_toks)
        data_ys.append(temp_ys)
        data_sec.append(temp_sec)
        data_start.append(temp_start)
        data_len.append(temp_len)
        data_drug.append(temp_drug)
    return data_drug, data_toks, data_ys, data_sec, data_start, data_len

def write_guess_xml_files(gold_xml_dir, 
                          guess_xml_dir, 
                          dict_ade, 
                          dict_modifiers, 
                          dict_relations):
    guess_files = xml_files(gold_xml_dir)
    for key, value in zip(guess_files.keys(), guess_files.values()):
        root = ElementTree.parse(value).getroot()
        root.remove(root[1])
        root.remove(root[2])
        root.remove(root[-1])
        Mentions = ElementTree.SubElement(root, "Mentions")
        for m in dict_ade[key]:
            ElementTree.SubElement(Mentions, "Mention", id=m[5], section=m[4], type=m[2], start=m[1], len=m[0], str=m[3])
        for m in dict_modifiers[key]:
            ElementTree.SubElement(Mentions, "Mention", id=m[5], section=m[4], type=m[2], start=m[1], len=m[0], str=m[3])

        Relations = ElementTree.SubElement(root, "Relations")
        for m in dict_relations[key]:
            ElementTree.SubElement(Relations, "Relation", id=m[0], type=m[3], arg1=m[1], arg2=m[2])

        Reactions = ElementTree.SubElement(root, "Reactions")
        tree = ElementTree.ElementTree(root)
        tree.write(os.path.join(guess_xml_dir, key + '.xml'), encoding="utf-8")