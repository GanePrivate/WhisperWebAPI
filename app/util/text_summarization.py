from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor


class Summarizer:
    def __init__(self, text):
        self.text = text
        # 自動要約のオブジェクトを生成
        auto_abstractor = AutoAbstractor()
        # トークナイザー（単語分割）にMeCabを指定
        auto_abstractor.tokenizable_doc = MeCabTokenizer()
        # 文書の区切り文字を指定
        auto_abstractor.delimiter_list = ["。", "\n", " "]
        # キュメントの抽象化、フィルタリングを行うオブジェクトを生成
        abstractable_doc = TopNRankAbstractor()
        # 文書の要約を実行
        result_dict = auto_abstractor.summarize(text, abstractable_doc)
        # result_dict["summarize_result"]に需要度が高い順に要約結果が入っている
        print(result_dict["summarize_result"])
        self.summary_text = result_dict["summarize_result"][0]


    def get_summary_text(self):
        return self.summary_text