from vncorenlp import VnCoreNLP

client = VnCoreNLP(address="http://127.0.0.1", port=9000)


def rule1(sent):
    doc1 = client.annotate(sent)
    dict_ie = {'infors': [], 'characterictics': []}
    for token in doc1["sentences"]:
        for s in range(len(token)):
            for v in range(s + 1, len(token) - 3):
                infor = ''
                characterictic = ''
                if token[v]["head"] == token[s]["index"]:
                    if (token[v]["posTag"] == 'N' and token[v]["depLabel"] == 'nmod') and (
                            token[s]["depLabel"] == 'sub' and token[s]["posTag"] == 'N'):
                        if (token[v + 1]["posTag"] == 'A' and token[v + 1]["depLabel"] == 'dep') and token[s][
                            "head"] == token[v + 1]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            dict_ie['characterictics'].append(characterictic)
                            dict_ie['infors'].append(infor)
                    # # V N A (V ->N, V ->A)
                    if (token[v]["posTag"] == 'N' and token[v]["depLabel"] == 'dob') and (
                            token[s]["depLabel"] == 'nmod'
                            and token[s]["posTag"] == 'V'):
                        if (token[v + 1]["posTag"] == 'A' and token[v + 1]["depLabel"] == 'nmod') and token[v + 1][
                            "head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            dict_ie['infors'].append(infor)
                            dict_ie['characterictics'].append(characterictic)
                    # # N A CH A Cc A
                    if ((token[s]["posTag"] == 'N' and token[s]["depLabel"] in ['root']) and
                            (token[v]["posTag"] in ['A'] and token[v]["depLabel"] in ['nmod'])):
                        if token[v + 1]["posTag"] == "CH" and token[v + 1]["depLabel"] == "punct" and token[v + 1][
                            "head"] == \
                                token[v]["index"]:
                            infor += token[s]["form"]
                            characterictic += token[v]["form"]
                            characterictic += '' + token[v + 1]["form"]
                            if token[v + 2]["posTag"] == "A" and token[v + 2]["depLabel"] == "amod" and token[v + 2][
                                "head"] \
                                    == token[v]["index"]:
                                characterictic += ' ' + token[v + 2]["form"]
                                if token[v + 3]["posTag"] == "Cc" and token[v + 3]["depLabel"] == "coord" and \
                                        token[v + 3]["head"] \
                                        == token[v]["index"]:
                                    characterictic += ' ' + token[v + 3]["form"]
                                    if token[v + 4]["posTag"] == "A" and token[v + 4]["depLabel"] == "conj" and \
                                            token[v + 4]["head"] == \
                                            token[v + 3]["index"]:
                                        characterictic += ' ' + token[v + 4]["form"]
                                        dict_ie['characterictics'].append(characterictic)
                                        dict_ie['infors'].append(infor)
                    # V R A Cc A
                    if ((token[s]["posTag"] == 'V' and token[s]["depLabel"] in ['vmod']) and
                            (token[v]["posTag"] in ['A'] and token[v]["depLabel"] in ['vmod'])):
                        if token[v - 1]["posTag"] == "R" and token[v - 1]["depLabel"] == "amod" and token[v - 1][
                            "head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            characterictic += token[v - 1]["form"]
                            characterictic += ' ' + token[v]["form"]
                            if token[v + 1]["posTag"] == "Cc" and token[v + 1]["head"] == token[v]["index"]:
                                characterictic += ' ' + token[v + 1]["form"]
                                if (token[v + 2]["posTag"] == "A" and token[v + 2]["depLabel"] == "conj") and \
                                        token[v + 2]["head"] == token[v + 1]["index"]:
                                    characterictic += ' ' + token[v + 2]["form"]
                                    dict_ie['characterictics'].append(characterictic)
                                    dict_ie['infors'].append(infor)
                    # N1 V M N2 A (N1 -> V, N2->M, N2 ->A, N1 -> N2)
                    if ((token[s]["posTag"] == 'N' and token[s]["depLabel"] in ['root']) and
                            (token[v]["posTag"] in ['V'] and token[v]["depLabel"] in ['nmod'])):
                        if token[v + 1]["posTag"] == "M" and token[v + 1]["depLabel"] == "det" and token[v + 1][
                            "head"] == token[v + 2]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            infor += ' ' + token[v + 1]["form"]
                            if token[v + 2]["posTag"] == "N" and token[v + 2]["head"] == token[s]["index"]:
                                characterictic += token[v + 2]["form"]
                                if (token[v + 3]["posTag"] == "A" and token[v + 3]["depLabel"] == "nmod") and \
                                        token[v + 3]["head"] == token[v + 2]["index"]:
                                    characterictic += ' ' + token[v + 3]["form"]
                                    dict_ie['characterictics'].append(characterictic)
                                    dict_ie['infors'].append(infor)
                    #  N N V A N
                    if ((token[s]["posTag"] == 'N' and token[s]["depLabel"] in ['sub']) and
                            (token[v]["posTag"] in ['N'] and token[v]["depLabel"] in ['nmod'])):
                        if token[v + 1]["posTag"] == "V" and token[v + 1]["depLabel"] == "root" and token[s][
                            "head"] == token[v + 1]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            if token[v + 2]["posTag"] == "A" and token[v + 2]["head"] == token[v + 1]["index"]:
                                characterictic += ' ' + token[v + 2]["form"]
                                if (token[v + 3]["posTag"] == "N" and token[v + 3]["depLabel"] == "amod") and \
                                        token[v + 3]["head"] == token[v + 2]["index"]:
                                    characterictic += ' ' + token[v + 3]["form"]
                                    dict_ie['infors'].append(infor)
                                    dict_ie['characterictics'].append(characterictic)
                    # V1 V2 N R V3 A
                    if ((token[s]["posTag"] == 'V' and token[s]["depLabel"] in ['root']) and
                            (token[v]["posTag"] in ['V'] and token[v]["depLabel"] in ['vmod'])):
                        if token[v + 1]["posTag"] == "N" and token[v + 1]["depLabel"] == "dob" and token[v + 1][
                            "head"] == token[s]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            infor += ' ' + token[v + 1]["form"]
                            if token[v + 2]["posTag"] == "R" and token[v + 2]["head"] == token[v + 3]["index"]:
                                characterictic += token[v + 2]["form"]
                                if (token[v + 4]["posTag"] == "A" and token[v + 4]["depLabel"] == "nmod") and \
                                        token[v + 4]["head"] == token[v + 3]["index"]:
                                    characterictic += ' ' + token[v + 4]["form"]
                                    dict_ie['infors'].append(infor)
                                    dict_ie['characterictics'].append(characterictic)
                    # V1 A V2 N ( V1 -> A, V1 -> V2, V2 ->N)
                    if (token[v]["posTag"] == 'A' and token[v]["depLabel"] == 'tmp') and (
                            token[s]["depLabel"] == 'dep' and token[s]["posTag"] == 'V'):
                        if (token[v + 1]["posTag"] == 'V' and token[v + 1]["depLabel"] == 'vmod') and token[v + 1][
                            "head"] == token[s]["index"]:
                            if (token[v + 2]["posTag"] == 'N' and token[v + 2]["depLabel"] == 'dob') and \
                                    token[v + 2]["head"] == token[v + 1]["index"]:
                                characterictic += token[v]["form"]
                                characterictic += ' ' + token[v + 1]["form"]
                                infor += token[v + 2]["form"]
                                dict_ie['characterictics'].append(characterictic)
                                dict_ie['infors'].append(infor)
                    # # V N R A (V -> N, N ->A, A ->R )
                    if (token[s]["posTag"] == 'V' and token[s]["depLabel"] in ['vmod']) and (
                            token[v]["depLabel"] == 'vmod' and token[v]["posTag"] == 'N'):
                        if (token[v + 1]["posTag"] == 'R' and token[v + 1]["depLabel"] == 'amod') and token[v + 1][
                            "head"] == token[v + 2]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            if (token[v + 2]["posTag"] == 'A' and token[v + 2]["depLabel"] == 'nmod') and token[v + 2][
                                "head"] == token[v]["index"]:
                                characterictic += ' ' + token[v + 2]["form"]
                                dict_ie['infors'].append(infor)
                                dict_ie['characterictics'].append(characterictic)
                    # N A1 Z A2 (N -> A1, N ->A2, A2 -> Z)
                    if (token[s]["posTag"] == 'N' and token[s]["depLabel"] in ['sub']) and (
                            token[v]["depLabel"] == 'nmod' and
                            token[v]["posTag"] == 'A'):
                        if (token[v + 1]["posTag"] == 'Z' and token[v + 1]["depLabel"] == 'amod') and token[v + 1][
                            "head"] == token[v + 2]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            if (token[v + 2]["posTag"] == 'A' and token[v + 2]["depLabel"] == 'nmod') and token[v + 2][
                                "head"] == token[s]["index"]:
                                characterictic += ' ' + token[v + 2]["form"]
                                dict_ie['infors'].append(infor)
                                dict_ie['characterictics'].append(characterictic)
                    #  N1 V N2 A (N1 -> V, V-> N2, A -> N1)
                    if (token[s]["posTag"] in ['N'] and token[s]["depLabel"] in ['sub']) and (
                            token[v]["depLabel"] in ['nmod'] and token[v]["posTag"] in ['V']):
                        if (token[v + 1]["posTag"] in ['N'] and token[v + 1]["depLabel"] in ['vmod']) and token[v + 1][
                            "head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            if (token[v + 2]["posTag"] in ['A'] and token[v + 2]["depLabel"] in ['root']) and token[s][
                                "head"] == token[v + 2]["index"]:
                                characterictic += ' ' + token[v + 2]["form"]
                                dict_ie['infors'].append(infor)
                                dict_ie['characterictics'].append(characterictic)
                    # V1 v2 R A (V1 -> V2, A, N-> R, V1-> A, N)
                    if (token[s]["posTag"] in ['V', 'N'] and token[s]["depLabel"] in ['root', 'dob', 'dep']) and (
                            token[v]["depLabel"] in ['vmod', 'nmod'] and token[v]["posTag"] in ['V', 'A']):
                        if (token[v + 1]["posTag"] in ['R'] and token[v + 1]["depLabel"] in ['amod', 'nmod']) and \
                                token[v + 1][
                                    "head"] == token[v + 2]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            if (token[v + 2]["posTag"] in ['A', 'N'] and token[v + 2]["depLabel"] in ['prd', 'dob']) and \
                                    (token[v + 2]["head"] == token[s]["index"] or token[s]["head"] == token[v + 2][
                                        "index"]):
                                characterictic += ' ' + token[v + 2]["form"]
                                dict_ie['infors'].append(infor)
                                dict_ie['characterictics'].append(characterictic)
                    # N1 CH N2 V A (N1 ->CH, N1 ->N2, V -> N1, V ->A)
                    if (token[s]["posTag"] in ['N'] and token[s]["depLabel"] in ['sub']) and (
                            token[v]["depLabel"] in ['punct'] and token[v]["posTag"] in ['CH']):
                        if (token[v + 1]["posTag"] in ['N'] and token[v + 1]["depLabel"] in ['nmod']) and token[v + 1][
                            "head"] == token[s]["index"]:
                            infor += token[s]["form"]
                            characterictic += token[v]["form"]
                            characterictic += ' ' + token[v + 1]["form"]
                            if (token[v + 2]["posTag"] in ['V'] and token[v + 2]["depLabel"] in ['root']) and token[s][
                                "head"] == token[v + 2]["index"]:
                                characterictic += ' ' + token[v + 2]["form"]
                                if (token[v + 3]["posTag"] in ['A'] and token[v + 3]["depLabel"] in ['vmod']) and \
                                        token[v + 3]["head"] == token[v + 2]["index"]:
                                    characterictic += ' ' + token[v + 3]["form"]
                                    dict_ie['characterictics'].append(characterictic)
                                    dict_ie['infors'].append(infor)
                    # N1 N2 V N3 A (N1 ->N2, V ->N1, V -> N3, N3 ->A)
                    if (token[s]["posTag"] in ['N'] and token[s]["depLabel"] in ['sub']) and (
                            token[v]["depLabel"] in ['nmod'] and token[v]["posTag"] in ['N2']):
                        if (token[v + 1]["posTag"] in ['V'] and token[v + 1]["depLabel"] in ['dep']) and token[s][
                            "head"] == token[v + 1]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            if (token[v + 2]["posTag"] in ['N'] and token[v + 2]["depLabel"] in ['dob']) and \
                                    token[v + 2][
                                        "head"] == token[v + 1]["index"]:
                                characterictic += ' ' + token[v + 2]["form"]
                                if (token[v + 3]["posTag"] in ['A'] and token[v + 3]["depLabel"] in ['nmod']) and \
                                        token[v + 3]["head"] == token[v + 2]["index"]:
                                    characterictic += ' ' + token[v + 3]["form"]
                                    dict_ie['characterictics'].append(characterictic)
                                    dict_ie['infors'].append(infor)
                    # N1  A  E N2 N3 (N1 ->A, N1 -> E, E -> N2, N2 ->N3)
                    if (token[s]["posTag"] in ['N'] and token[s]["depLabel"] in ['sub']) and (
                            token[v]["depLabel"] in ['nmod'] and token[v]["posTag"] in ['A']):
                        if (token[v + 1]["posTag"] in ['E'] and token[v + 1]["depLabel"] in ['nmod']) and token[v + 1][
                            "head"] == token[s]["index"]:
                            infor += token[s]["form"]
                            characterictic += token[v]["form"]
                            characterictic += ' ' + token[v + 1]["form"]
                            if (token[v + 2]["posTag"] in ['N'] and token[v + 2]["depLabel"] in ['pob']) and \
                                    token[v + 2][
                                        "head"] == token[v + 1]["index"]:
                                characterictic += ' ' + token[v + 2]["form"]
                                if (token[v + 3]["posTag"] in ['N'] and token[v + 3]["depLabel"] in ['nmod']) and \
                                        token[v + 3]["head"] == token[v + 2]["index"]:
                                    characterictic += ' ' + token[v + 3]["form"]
                                    dict_ie['characterictics'].append(characterictic)
                                    dict_ie['infors'].append(infor)
                    # V Nb N1 A N2 (V -> Nb, Nb-> N1, Nb-> A, A ->N2)
                    if (token[s]["posTag"] in ['V'] and token[s]["depLabel"] in ['vmod']) and (
                            token[v]["depLabel"] in ['dob'] and token[v]["posTag"] in ['Nb']):
                        if (token[v + 1]["posTag"] in ['N'] and token[v + 1]["depLabel"] in ['nmod']) and token[v + 1][
                            "head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            if (token[v + 2]["posTag"] in ['A'] and token[v + 2]["depLabel"] in ['nmod']) and \
                                    token[v + 2][
                                        "head"] == token[v]["index"]:
                                characterictic += ' ' + token[v + 2]["form"]
                                if (token[v + 3]["posTag"] in ['N'] and token[v + 3]["depLabel"] in ['amod']) and \
                                        token[v + 3]["head"] == token[v + 2]["index"]:
                                    characterictic += ' ' + token[v + 3]["form"]
                                    dict_ie['characterictics'].append(characterictic)
                                    dict_ie['infors'].append(infor)
                    # V X (V -> X)
                    if (token[v]["posTag"] == 'X' and token[v]["depLabel"] in ['x']) and (
                            token[s]["depLabel"] == 'vmod' and token[s]["posTag"] in ['V']):
                        infor += token[s]["form"]
                        characterictic += token[v]["form"]
                        dict_ie['characterictics'].append(characterictic)
                        dict_ie['infors'].append(infor)
                    # N V R A (N -> V, A -> N, A -> R)
                    if (token[v]["posTag"] == 'V' and token[v]["depLabel"] in ['nmod']) and (
                            token[s]["depLabel"] == 'sub' and token[s]["posTag"] in ['N']):
                        if (token[v + 1]["posTag"] == 'R' and token[v + 1]["depLabel"] == 'amod') and token[v + 1][
                            "head"] == token[v + 2]["index"] and (
                                token[v + 2]["posTag"] == 'A' and token[v + 2]["depLabel"] == 'dep') and token[s][
                            "head"] == token[v + 2]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v + 1]["form"]
                            characterictic += ' ' + token[v + 2]["form"]
                            dict_ie['characterictics'].append(characterictic)
                            dict_ie['infors'].append(infor)

                if token[s]["head"] == token[v]["index"]:
                    # Np V A1 A2 (V -> Np, V -> A, V -> A1, V -> A2)
                    if (token[v]["posTag"] == 'V' and token[v]["depLabel"] in ['root', 'dep']) and (
                            token[s]["depLabel"] == 'sub' and
                            token[s]["posTag"] == 'Np'):
                        if (token[v + 1]["posTag"] == 'A' and token[v + 1]["depLabel"] == 'vmod') and token[v + 1][
                            "head"] == token[v]["index"]:
                            if (token[v + 2]["posTag"] == 'A' and token[v + 2]["depLabel"] == 'vmod') and token[v + 2][
                                "head"] == token[v]["index"]:
                                infor += token[s]["form"]
                                infor += ' ' + token[v]["form"]
                                characterictic += token[v + 1]["form"]
                                characterictic += ' ' + token[v + 2]["form"]
                                dict_ie['infors'].append(infor)
                                dict_ie['characterictics'].append(characterictic)
                        # A1 V N A2 (V -> A1, V -> N, N -> A)
                    if (token[v]["posTag"] == 'V' and token[v]["depLabel"] in ['vmod']) and (
                            token[s]["depLabel"] == 'vmod' and token[s]["posTag"] == 'A'):
                        if (token[v + 1]["posTag"] == 'N' and token[v + 1]["depLabel"] == 'dob') and token[v + 1][
                            "head"] == token[v]["index"]:
                            if (token[v + 2]["posTag"] == 'A' and token[v + 2]["depLabel"] == 'nmod') and token[v + 2][
                                "head"] == token[v + 1]["index"]:
                                characterictic += token[s]["form"]
                                characterictic += ' '+token[v]["form"]
                                characterictic += ' ' + token[v + 2]["form"]
                                infor += token[v + 1]["form"]
                                dict_ie['infors'].append(infor)
                                dict_ie['characterictics'].append(characterictic)
                    # N C R A (A-> N, A->C, A -> R)
                    if (token[v]["posTag"] == 'A' and token[v]["depLabel"] in ['root', 'dep']) and (
                            token[s]["depLabel"] == 'sub' and
                            token[s]["posTag"] in ['Nb', 'N']):
                        if (token[v - 1]["posTag"] == 'R' and token[v - 1]["depLabel"] == 'amod') and token[v - 1][
                            "head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            characterictic += token[v - 1]["form"]
                            characterictic += ' ' + token[v]["form"]
                            dict_ie['infors'].append(infor)
                            dict_ie['characterictics'].append(characterictic)
                    # N R A (A -> N, A -> R)
                    if (token[v]["posTag"] == 'A' and token[v]["depLabel"] in ['root']) and (
                            token[s]["depLabel"] == 'sub' and token[s]["posTag"] in ['N']):
                        if (token[v - 1]["posTag"] == 'A' and token[v - 1]["depLabel"] == 'vmod') and token[v - 1][
                            "head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            characterictic += token[v - 1]["form"]
                            characterictic += ' ' + token[v]["form"]
                            dict_ie['characterictics'].append(characterictic)
                            dict_ie['infors'].append(infor)
                    # V R A (V -> A, A -> R)
                    if (token[v]["posTag"] == 'A' and token[v]["depLabel"] in ['vmod']) and (
                            token[s]["depLabel"] == 'amod' and token[s]["posTag"] in ['R']):
                        if (token[v - 2]["posTag"] == 'V' and token[v - 2]["depLabel"] == 'root') and token[v][
                            "head"] == token[v - 2]["index"]:
                            infor += token[v - 2]["form"]
                            characterictic += token[s]["form"]
                            characterictic += ' ' + token[v]["form"]
                            dict_ie['characterictics'].append(characterictic)
                            dict_ie['infors'].append(infor)
                    # N V R A ( V-> N, V -> A, A -> R)
                    if (token[v]["posTag"] == 'A' and token[v]["depLabel"] in ['root']) and (
                            token[s]["depLabel"] == 'sub' and token[s]["posTag"] in ['N']):
                        if (token[v + 1]["posTag"] == 'R' and token[v + 1]["depLabel"] == 'amod') and token[v + 1][
                            "head"] == token[v + 2]["index"]:
                            if (token[v + 2]["posTag"] == 'A' and token[v + 2]["depLabel"] == 'vmod') and token[v + 2][
                                "head"] == token[v]["index"]:
                                infor += token[s]["form"]
                                characterictic += token[v + 1]["form"]
                                characterictic = ' ' + token[v + 2]["form"]
                                dict_ie['characterictics'].append(characterictic)
                                dict_ie['infors'].append(infor)
                    # N R V A,N ( V-> N, V -> A,N, V -> N)
                    if (token[v]["posTag"] == 'V' and token[v]["depLabel"] in ['vmod', 'dep']) and (
                            token[s]["depLabel"] == 'sub' and token[s]["posTag"] in ['N']):
                        if (token[v - 1]["posTag"] == 'R' and token[v - 1]["depLabel"] == 'adv') and token[v - 1][
                            "head"] == token[v]["index"]:
                            if (token[v + 1]["posTag"] in ['A', 'N'] and token[v + 1]["depLabel"] in ['vmod',
                                                                                                      'dob']) and \
                                    token[v + 1][
                                        "head"] == token[v]["index"]:
                                infor += token[s]["form"]
                                characterictic += token[v - 1]["form"]
                                characterictic = ' ' + token[v]["form"]
                                characterictic = ' ' + token[v + 1]["form"]
                                dict_ie['characterictics'].append(characterictic)
                                dict_ie['infors'].append(infor)
                    # N V A ( V->N, V -> A)
                    if (token[v]["posTag"] == 'V' and token[v]["depLabel"] in ['root']) and (
                            token[s]["depLabel"] == 'sub' and token[s]["posTag"] in ['N']):
                        if (token[v + 1]["posTag"] == 'A' and token[v +1]["depLabel"] == 'vmod') and token[v+1][
                            "head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            infor += ' ' + token[v]["form"]
                            characterictic += token[v+1]["form"]
                            dict_ie['characterictics'].append(characterictic)
                            dict_ie['infors'].append(infor)
    return dict_ie


def rule2(sent):
    doc1 = client.annotate(sent)
    dict_ie_2 = {'infors': [], 'characterictics': []}
    for token in doc1["sentences"]:
        for s in range(len(token)):
            for v in range(s + 1, len(token) - 2):
                infor = ''
                characterictic = ''
                if token[v]["head"] == token[s]["index"]:
                    if (token[v]["posTag"] in ['Z'] and token[v]["depLabel"] in ['nmod']) and (
                            token[s]["depLabel"] in ['dob']
                            and token[s]["posTag"] in ['N']):
                        if (token[v + 1]["posTag"] == 'A' and token[v + 1]["depLabel"] in ['nmod']) and \
                                token[v + 1]["head"] == token[s]["index"]:
                            infor += token[s]["form"]
                            characterictic += token[v]["form"]
                            characterictic += ' ' + token[v + 1]["form"]
                            dict_ie_2['characterictics'].append(characterictic)
                            dict_ie_2['infors'].append(infor)
                    # V Nb N1 A N2 (V -> Nb, Nb-> N1, Nb-> A, A ->N2)
                    if (token[s]["posTag"] in ['V'] and token[s]["depLabel"] in ['vmod']) and (
                            token[v]["depLabel"] in ['dob'] and token[v]["posTag"] in ['Nb']):
                        if (token[v + 1]["posTag"] in ['N'] and token[v + 1]["depLabel"] in ['nmod']) and token[v + 1][
                            "head"] == token[v]["index"]:
                            if (token[v + 2]["posTag"] in ['A'] and token[v + 2]["depLabel"] in ['nmod']) and \
                                    token[v + 2][
                                        "head"] == token[v]["index"]:
                                if (token[v + 3]["posTag"] in ['N'] and token[v + 3]["depLabel"] in ['amod']) and \
                                        token[v + 3]["head"] == token[v + 2]["index"]:
                                    infor += token[s]["form"]
                                    infor += ' ' + token[v]["form"]
                                    characterictic += token[v + 1]["form"]
                                    characterictic += ' ' + token[v + 2]["form"]
                                    characterictic += ' ' + token[v + 3]["form"]
                                    dict_ie_2['characterictics'].append(characterictic)
                                    dict_ie_2['infors'].append(infor)

                    # V Nb A1 A2 (V -> Nb, Nb->A1, A1->A2)
                    if (token[v]["posTag"] in ['Nb'] and token[v]["depLabel"] in ['dob']) and (
                            token[s]["depLabel"] in ['vmod'] and token[s]["posTag"] in ['V']):
                        if (token[v + 1]["posTag"] in ['A'] and token[v + 1]["depLabel"] in ['nmod']) and token[v + 1][
                            "head"] == token[v]["index"]:
                            if (token[v + 2]["posTag"] in ['A'] and token[v + 1]["depLabel"] in ['amod']) and \
                                    token[v + 2][
                                        "head"] == token[v + 1]["index"]:
                                infor += token[s]["form"]
                                infor += ' ' + token[v]["form"]
                                characterictic += token[v + 1]['form']
                                characterictic += ' ' + token[v + 2]['form']
                                dict_ie_2['characterictics'].append(characterictic)
                                dict_ie_2['infors'].append(infor)
                    #  N V R A (N -> V, A-> R, A -> N)
                    if (token[s]["posTag"] in ['N'] and token[s]["depLabel"] in ['sub']) and (
                            token[v]["depLabel"] in ['nmod'] and token[v]["posTag"] in ['V']):
                        if (token[v + 1]["posTag"] in ['R'] and token[v + 1]["depLabel"] in ['amod']) and token[v + 1][
                            "head"] == token[v + 2]["index"]:
                            if (token[v + 2]["posTag"] in ['A'] and token[v + 2]["depLabel"] in ['root']) and token[s][
                                "head"] == token[v + 2]["index"]:
                                infor += token[s]["form"]
                                infor += ' ' + token[v]["form"]
                                characterictic += token[v + 1]["form"]
                                characterictic += ' ' + token[v + 2]["form"]
                                dict_ie_2['characterictics'].append(characterictic)
                                dict_ie_2['infors'].append(infor)
                    #  N R A1 A2 (N -> A1, A1-> R, A1 -> A2)
                    if (token[s]["posTag"] in ['N'] and token[s]["depLabel"] in ['sub']) and (
                            token[v]["depLabel"] in ['nmod'] and token[v]["posTag"] in ['A']):
                        if (token[v - 1]["posTag"] in ['R'] and token[v - 1]["depLabel"] in ['amod']) and token[v - 1][
                            "head"] == token[v]["index"]:
                            if (token[v + 1]["posTag"] in ['A'] and token[v + 1]["depLabel"] in ['amod']) and \
                                    token[v + 1][
                                        "head"] == token[v]["index"]:
                                infor += token[s]["form"]
                                characterictic += token[v - 1]["form"]
                                characterictic += ' ' + token[v]["form"]
                                characterictic += ' ' + token[v + 1]["form"]
                                dict_ie_2['characterictics'].append(characterictic)
                                dict_ie_2['infors'].append(infor)
                    # N A1 A2 (N ->A1, A1->A2)
                    if (token[s]["posTag"] in ['N'] and token[s]["depLabel"] in ['dob']) and (
                            token[v]["depLabel"] in ['nmod'] and token[v]["posTag"] in ['A']):
                        if (token[v + 1]["posTag"] in ['A'] and token[v + 1]["depLabel"] in ['amod']) and token[v + 1][
                            "head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            characterictic += token[v]["form"]
                            dict_ie_2['characterictics'].append(characterictic)
                            dict_ie_2['infors'].append(infor)
                    # V N1 N2 A (V->N, N1 ->N2, N1 -> A)
                    if (token[s]["posTag"] in ['V'] and token[s]["depLabel"] in ['root']) and (
                            token[v]["depLabel"] in ['dob'] and token[v]["posTag"] in ['N']):
                        if (token[v + 1]["posTag"] in ['N'] and token[v + 1]["depLabel"] in ['nmod']) and token[v + 1][
                            "head"] == token[v]["index"]:
                            if (token[v + 2]["posTag"] in ['A'] and token[v + 2]["depLabel"] in ['nmod']) and \
                                    token[v + 1][
                                        "head"] == token[v]["index"]:
                                infor += token[s]["form"]
                                infor += ' ' + token[v]["form"]
                                infor += ' ' + token[v + 1]["form"]
                                characterictic += token[v + 2]["form"]
                                dict_ie_2['characterictics'].append(characterictic)
                                dict_ie_2['infors'].append(infor)
                    # V A E M ( V->A, V -> E, V -> M)
                    if (token[s]["posTag"] in ['V'] and token[s]["depLabel"] in ['vmod']) and (
                            token[v]["depLabel"] in ['vmod'] and token[v]["posTag"] in ['A']):
                        if (token[v + 1]["posTag"] in ['E'] and token[v + 1]["depLabel"] in ['dir']) and token[v + 1][
                            "head"] == token[s]["index"]:
                            if (token[v + 2]["posTag"] in ['M'] and token[v + 2]["depLabel"] in ['vmod']) and \
                                    token[v + 2][
                                        "head"] == token[s]["index"]:
                                infor += token[s]["form"]
                                infor += ' ' + token[v]["form"]
                                characterictic += token[v + 1]["form"]
                                characterictic += ' ' + token[v + 2]["form"]
                                dict_ie_2['characterictics'].append(characterictic)
                                dict_ie_2['infors'].append(infor)
                    # N1 N2 R A V (N1 -> N2, N1-> A, N1-> V, A ->R)
                    if (token[s]["posTag"] in ['N'] and token[s]["depLabel"] in ['dob']) and (
                            token[v]["depLabel"] in ['nmod'] and token[v]["posTag"] in ['N']):
                        if (token[v + 1]["posTag"] in ['R'] and token[v + 1]["depLabel"] in ['amod']) and token[v + 1][
                            "head"] == token[v+2]["index"]:
                            if (token[v + 2]["posTag"] in ['A'] and token[v + 2]["depLabel"] in ['nmod']) and \
                                    token[v + 2][
                                        "head"] == token[s]["index"]:
                                if (token[v + 3]["posTag"] in ['V'] and token[v + 3]["depLabel"] in ['nmod']) and \
                                        token[v + 3]["head"] == token[s]["index"]:
                                    infor += token[v+3]["form"]

                                    characterictic += token[s]["form"]
                                    characterictic += ' ' + token[v]["form"]
                                    characterictic += ' ' + token[v + 1]["form"]
                                    characterictic += ' ' + token[v + 2]["form"]
                                    dict_ie_2['characterictics'].append(characterictic)
                                    dict_ie_2['infors'].append(infor)

                if token[s]["head"] == token[v]["index"]:

                    # N A (A -> N)
                    if (token[v]["posTag"] in ['A'] and token[v]["depLabel"] in ['root']) and (
                            token[s]["depLabel"] in ['sub']
                            and token[s]["posTag"] in ['N']):
                        if (token[v - 1]["posTag"] in ['C'] and token[v - 1]["depLabel"] in ['dep']) and \
                                token[v - 1]["head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            characterictic +=  token[v]["form"]
                            dict_ie_2['characterictics'].append(characterictic)
                            dict_ie_2['infors'].append(infor)
                    # Nb V A (V -> Nb, V -> A)
                    if (token[v]["posTag"] in ['V'] and token[v]["depLabel"] in ['root']) and (
                            token[s]["depLabel"] in ['sub', 'adv']
                            and token[s]["posTag"] in ['R', 'Np']):
                        if (token[v + 1]["posTag"] in ['A', 'Nb'] and token[v + 1]["depLabel"] in ['dob', 'vmod']) and \
                                token[v + 1]["head"] == token[v]["index"]:
                            infor += token[s]["form"]
                            characterictic += token[v]["form"]
                            characterictic += ' ' + token[v + 1]["form"]
                            dict_ie_2['characterictics'].append(characterictic)
                            dict_ie_2['infors'].append(infor)
                    if (token[v]["posTag"] in ['V'] and token[v]["depLabel"] in ['root', 'dep']) and (
                            token[s]["depLabel"] in ['adv', 'sub'] and token[s]["posTag"] in ['R', 'N']) and (
                            token[s]["form"] not in ['nhân_viên']):
                        if ((token[v + 1]["posTag"] in ['N', 'Nb'] and token[v + 1]["depLabel"] in ['dob']) and \
                            token[v + 1]["head"] == token[v]["index"]) and (token[v + 2]["depLabel"] == 'nmod' and
                                                                            token[v + 2]["posTag"] == 'R'):
                            infor += token[s]["form"]
                            characterictic += token[v]["form"]
                            characterictic += ' ' + token[v + 1]["form"]
                            dict_ie_2["infors"].append(infor)
                            dict_ie_2['characterictics'].append(characterictic)
                        # A1 V N A2 (V -> A1, V -> N, N -> A)
                    if (token[v]["posTag"] == 'V' and token[v]["depLabel"] in ['vmod']) and (
                            token[s]["depLabel"] == 'vmod' and token[s]["posTag"] == 'A'):
                        if (token[v + 1]["posTag"] == 'N' and token[v + 1]["depLabel"] == 'dob') and token[v + 1][
                            "head"] == token[v]["index"]:
                            infor += token[v]["form"]
                            infor += ' ' + token[v + 1]["form"]
                            if (token[v + 2]["posTag"] == 'A' and token[v + 2]["depLabel"] == 'nmod') and token[v + 2][
                                "head"] == token[v + 1]["index"]:
                                characterictic += token[v + 2]["form"]
                                dict_ie_2['characterictics'].append(characterictic)
                                dict_ie_2['infors'].append(infor)
                        # C V1 V2 V3 (V1 -> C, V1 -> V2, V2 -> V3)
                    if (token[v]["posTag"] == 'V' and token[v]["depLabel"] in ['dep']) and (
                            token[s]["depLabel"] == 'dep' and token[s]["posTag"] == 'C'):
                        if (token[v + 1]["posTag"] == 'V' and token[v + 1]["depLabel"] == 'vmod') and token[v + 1][
                            "head"] == token[v]["index"]:

                            if (token[v + 2]["posTag"] == 'V' and token[v + 2]["depLabel"] == 'vmod') and token[v + 2][
                                "head"] == token[v + 1]["index"]:
                                characterictic += token[v]["form"]
                                characterictic += ' ' + token[v + 1]["form"]
                                infor += token[v + 2]["form"]
                                dict_ie_2['characterictics'].append(characterictic)
                                dict_ie_2['infors'].append(infor)
                    # R1 V1 R2 N1 V2 N2 (V1 -> R1, V1-> R2, V1->N1, N1 ->V2, V2->N2)
                    if (token[s]["posTag"] in ['R'] and token[s]["depLabel"] in ['adv']) and (
                            token[v]["depLabel"] in ['root'] and token[v]["posTag"] in ['V']):
                        if (token[v + 1]["posTag"] in ['R'] and token[v + 1]["depLabel"] in ['adv']) and token[v + 1][
                            "head"] == token[v]["index"]:
                            if (token[v + 2]["posTag"] in ['N'] and token[v + 2]["depLabel"] in ['dob']) and \
                                    token[v + 2]["head"] == token[v]["index"]:
                                if (token[v + 3]["posTag"] in ['V'] and token[v + 3]["depLabel"] in ['nmod']) and \
                                        token[v + 3]["head"] == token[v + 2]["index"]:
                                    if (token[v + 4]["posTag"] in ['N'] and token[v + 4]["depLabel"] in ['dob']) and \
                                            token[v + 4]["head"] == token[v + 3]["index"]:
                                        characterictic += token[s]["form"]
                                        characterictic += ' ' + token[v]["form"]
                                        characterictic += ' ' + token[v + 1]["form"]
                                        infor += token[v + 2]["form"]
                                        infor += ' ' + token[v + 3]["form"]
                                        infor += ' ' + token[v + 4]["form"]
                                        dict_ie_2['infors'].append(infor)
                                        dict_ie_2['characterictics'].append(characterictic)
                    # N C A V ( A ->N, A -> C, A ->V)
                    if (token[v]["posTag"] == 'A' and token[v]["depLabel"] in ['dep']) and (
                            token[s]["depLabel"] == 'sub' and token[s]["posTag"] == 'N'):
                        if (token[v - 1]["posTag"] == 'C' and token[v - 1]["depLabel"] == 'dep') and token[v - 1][
                            "head"] == token[v]["index"]:
                            if (token[v + 1]["posTag"] == 'V' and token[v + 1]["depLabel"] == 'vmod') and token[v + 1][
                                "head"] == token[v]["index"]:
                                infor += token[s]["form"]
                                infor += ' ' + token[v - 1]["form"]
                                characterictic += token[v]["form"]
                                characterictic += ' ' + token[v + 1]["form"]
                                dict_ie_2['characterictics'].append(characterictic)
                                dict_ie_2['infors'].append(infor)
                    # M Nu R A (Nu ->M, Nu -> A, A ->R)
                    if (token[v]["posTag"] == 'Nu' and token[v]["depLabel"] in ['conj']) and (
                            token[s]["depLabel"] == 'det' and token[s]["posTag"] == 'M'):
                        if (token[v + 1]["posTag"] == 'R' and token[v + 1]["depLabel"] == 'amod') and token[v + 1][
                            "head"] == token[v + 2]["index"]:
                            if (token[v + 2]["posTag"] == 'A' and token[v + 2]["depLabel"] == 'nmod') and token[v + 2][
                                "head"] == token[v]["index"]:
                                infor += token[s]["form"]
                                infor += '' + token[v]["form"]
                                characterictic += token[v + 1]["form"]
                                characterictic += ' ' + token[v + 2]["form"]
                                dict_ie_2['characterictics'].append(characterictic)
                                dict_ie_2['infors'].append(infor)
    return dict_ie_2
