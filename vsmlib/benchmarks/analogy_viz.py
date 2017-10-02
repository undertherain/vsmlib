import pandas
from pandas.io.json import json_normalize
from vsmlib.misc.data import load_json

path = "/mnt/storage/Data/linguistic/outs/BATS_3.0/LRCos_C1.0/w2v_bnc_vsm_w5_ns_normalized/D01 [noun+less_reg].json"


def df_from_file(path):
    data = load_json(path)
    df=pandas.DataFrame(data["results"], columns=["expected answer",
                                                  "rank",
                                                  "b",
                                                  "b in neighbourhood of b_prime",
                                                  "b_prime in neighbourhood of b",
                                                  "distance a to a_prime euclidean",
                                                  "distance a_prime to b_prime euclidean",
                                                  "similarity a to a_prime cosine",
                                                  "similarity a_prime to b_prime cosine",
                                                  "similarity b to b_prime cosine",
                                                  "similarity predicted to b_prime cosine",
                                                  "similarity to b_prime neighbor 5",
                                                  "similarity to b_prime neighbor 10",
                                                  "landing_a",
                                                  "landing_a_prime",
                                                  "landing_b",
                                                  "landing_b_prime"
                                                 ])
    #df["embeddings"] = data["experiment setup"]["embeddings"]
    #df["category"] = data["experiment setup"]["category"]
    #df["method"] = data["experiment setup"]["method"]
    #for i in range(0, 6):
        #df["hit" + str(i)] = ((df["rank"]<i)) & (df["rank"]>=0)
    #df["reciprocal_rank"] = 1 / df["rank"]
    return df


#df = df_from_file(path)
data = load_json(path)
#df = json_normalize(data, 'counties', ['state', 'shortname', ['info', 'governor']])
df = json_normalize(data, ['experiment setup', ['dataset']])

print(df)
