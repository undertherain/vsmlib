letter_codes={"a":1,"b":2,"c":3,"d":4}

def get_test_from_file(name_file):
    result=[]
    for line in open(name_file).readlines():
        tokens = [token.lower() for token in line.split()]
        if len(tokens)<2: continue
        result.append(tokens)
    return (result)

def get_test_from_toefl(name_file):
    result=[]
    words=[]
    for line in open(name_file+".qst").readlines():
        tokens = [token.lower() for token in line.split()]
        if len(tokens)<2: 
            result.append(words)
            words=[]
        else:
            words.append(tokens[1])
    i=0;
    for line in open(name_file+".ans").readlines():
        tokens = [token.lower() for token in line.split()]
        if len(tokens)<2: continue
        key=tokens[-1]
        #print (i,result[i],key)
        result[i].append(result[i][letter_codes[key]])
        i+=1;
    return result