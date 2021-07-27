import os

def extract_mention_from_sentence(drug, set_toks, ys_bio, section, start, leng, segment="BIO"):
    data_drug = []
    data_toks = []
    data_ys = []
    data_sec = []
    data_start = []
    data_len = []
    if segment == "BIO":
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
                    else: 
                        for k,j in enumerate(ys[i+1:]):
                            if j.startswith('I-'):
                                tok_txt += ' ' + tok[i+k+1]
                                len_text = le[i+k+1] 

                            else:
                                break
                        len_t = len_text
                        temp_toks.append(tok_txt)
                        temp_ys.append(ys_txt)
                        temp_sec.append(sec_txt)
                        temp_start.append(start_txt)
                        temp_len.append(len_t)
                        temp_drug.append(drug_text)
            data_toks.append(temp_toks)
            data_ys.append(temp_ys)
            data_sec.append(temp_sec)
            data_start.append(temp_start)
            data_len.append(temp_len)
            data_drug.append(temp_drug)
    elif segment == "BILOU":
        for d, tok, ys, sec, st, le in zip(drug, set_toks, ys_bio, section, start, leng):
            temp_toks = []
            temp_ys = []
            temp_sec = []
            temp_start = []
            temp_len = []
            temp_drug = []
            for i, (t, yb, s, a, b, e) in enumerate(zip(tok, ys, sec, st, le, d)):

                if yb.startswith('U-'):
                    temp_toks.append(t)
                    temp_ys.append(yb[2:])
                    temp_sec.append(s)
                    temp_start.append(a)
                    temp_len.append(b)
                    temp_drug.append(e)
                elif yb.startswith('B-'):
                    tok_txt = t
                    ys_txt = yb[2:]
                    sec_txt = s
                    start_txt = a
                    len_text = b
                    drug_text = e
                    if (i+1) == len(ys_bio):
                        break
                    else: 
                        start_n = a
                        for k,j in enumerate(ys[i+1:]):
                            if j.startswith('I-'):
                                tok_txt += ' ' + tok[i+k+1]
                                len_text = le[i+k+1] 
                                start_n = st[i+k+1]

                            elif j.startswith('L-'):
                                tok_txt += ' ' + tok[i+k+1]
                                len_text = le[i+k+1] 
                                start_n = st[i+k+1]
                                break
                        len_t = (start_n-start_txt)+len_text
                        temp_toks.append(tok_txt)
                        temp_ys.append(ys_txt)
                        temp_sec.append(sec_txt)
                        temp_start.append(start_txt)
                        temp_len.append(len_t)
                        temp_drug.append(drug_text)
            data_toks.append(temp_toks)
            data_ys.append(temp_ys)
            data_sec.append(temp_sec)
            data_start.append(temp_start)
            data_len.append(temp_len)
            data_drug.append(temp_drug)

    return data_drug, data_toks, data_ys, data_sec, data_start, data_len

def write_brat_files(guess_dir, 
                     dict_ade, 
                     dict_modifiers, 
                     dict_relations):
    for key in os.listdir(guess_dir):
        if key.endswith('.txt'):
            key = key.replace('.txt', '')
            file = open(os.path.join(guess_dir, key + '.ann'),"w") 

            for m in dict_ade[key]:
                file.write(m[4] + '\t' + m[2] + ' ' + m[1] + ' ' + m[0] + '\t' + m[3] + '\n')

            for m in dict_modifiers[key]:
                file.write(m[4] + '\t' + m[2] + ' ' + m[1] + ' ' + m[0] + '\t' + m[3] + '\n')

            for m in dict_relations[key]:

                file.write(m[0] + '\t' + m[3] + ' Arg1:' + m[2] + ' Arg2:' + m[1] + '\n')
            file.close()