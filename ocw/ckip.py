from ckip_transformers.nlp import CkipPosTagger, CkipWordSegmenter

ws_driver = CkipWordSegmenter(model="bert-base")
pos_driver = CkipPosTagger(model="bert-base")


def extract_keyword(sentence: list[str]) -> list[str]:
    word_sentence_list: list[list[str]] = ws_driver(sentence)
    pos_sentence_list: list[list[str]] = pos_driver(word_sentence_list)

    return list(
        set(
            map(
                lambda wordpos: wordpos[0],
                filter(
                    lambda wordpos: wordpos[1] == "Na",
                    zip(
                        (word for sentence in word_sentence_list for word in sentence),
                        (pos for sentence in pos_sentence_list for pos in sentence),
                    ),
                ),
            )
        )
    )
