import os
from ckiptagger import data_utils, WS, POS

# Install the model.
if not os.path.exists("data"):
    data_utils.download_data_gdown("./")

ws = WS("./data")
pos = POS("./data")

def extract_keyword(sentence: list[str]) -> list[str]:
    word_sentence_list: list[list[str]] = ws(sentence)
    pos_sentence_list: list[list[str]] = pos(word_sentence_list)

    return list(set(map(
        lambda wordpos: wordpos[0],
        filter(
            lambda wordpos: wordpos[1] in ["Na", "Nb"],
            zip(
                (word for sentence in word_sentence_list for word in sentence),
                (pos for sentence in pos_sentence_list for pos in sentence),
            )
        )
    )))
