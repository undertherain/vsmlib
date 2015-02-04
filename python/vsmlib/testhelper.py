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

def cmp_first_tail(m,l,verbose=False):
    max_score=-1;
    max_element=None
    scores=[]
    if verbose: 
        print (l[0]," vs")
    for i in l[1:]:
        score=m.cmp_words(l[0],i)
        scores.append(score)
        if verbose: print (i.ljust(10)+"\t"+str(score))
    confidence = sorted(scores)[-1]-sorted(scores)[-2]
    return scores,  l[scores.index(max(scores))+1]
    #return l[scores.index(max(scores))+1], confidence

def do_synonyms_test(m,lines):
    output=""
    cnt_all=0;
    cnt_correct=0;
    lst_conf=[]
    for tokens in lines:
        print ("processing",tokens[0])
        #guess,confidence=cmp_first_tail(tokens[:-1],verbose=False)
        scores,guess=cmp_first_tail(m,tokens[:-1],verbose=False)
        #print (scores)
        if guess==tokens[-1]:
            cnt_correct+=1
            #lst_conf.append(confidence)
        cnt_all+=1
        #print (tokens[0],guess,guess==tokens[-1],"\n")
        output+="<b>"+tokens[0]+"</b> : "
        #output+="<b>"+tokens[0]+"</b>[{}] : ".format(get_frequency(get_id(tokens[0])))

        for i in range(len(tokens)-2):
            t=tokens[i+1]
            if t==guess:
                if (t==tokens[-1]):
                    output+=" <span style=\"color:green;\">"+t+"</span>"
                else:
                    output+=" <span style=\"color:red;\">"+t+"</span>"
            else: 
                if (t==tokens[-1]):
                    output+=" <span style=\"text-decoration: underline; border-decoration-color: green; -moz-text-decoration-color: green;\">"+t+"</span>"
                else:
                    output+=" "+t
            #output+="[{}]".format(get_frequency(get_id(t)))
            output+="({:.2f})".format(scores[i])
        output+="<br />\n"
        #related=get_most_related_words(tokens[0])
        #for r in related:
#            output+="{}({:.2f}) ".format(r[0],r[1])
        #if (guess==tokens[-1]):
#            output+="<span style=\"color:green\">correct!</span>"
#        else:
#            output+="<span style=\"color:red\">wrong</span>, should be "+tokens[-1]
        #output+="<br /><br />\n"
    success_rate=cnt_correct/cnt_all
    output+="<br />success rate = " + str( success_rate)+"</br>\n"
    #output+="avg confidence = "+ str( np.mean(lst_conf))+"</br>\n"
    return output