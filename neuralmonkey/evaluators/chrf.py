from typing import List, Optional


# pylint: disable=too-few-public-methods
class ChrFEvaluator(object):
    """Compute ChrF introduced in
    http://www.statmt.org/wmt15/pdf/WMT49.pdf
    """

    def __init__(self, n: int = 6, beta: float = 1,
                 ignored_symbols: Optional[List[str]] = None,
                 name: Optional[str] = None) -> None:
        self.n = n
        # We store the squared value of Beta
        self.beta_2 = beta**2

        if ignored_symbols is not None:
            self.ignored = ignored_symbols
        else:
            self.ignored = [" "]

        if name is not None:
            self.name = name
        else:
            self.name = "ChrF-{}".format(beta)

    # pylint: disable=too-many-locals
    def __call__(self, hypotheses: List[List[str]],
                 references: List[List[str]]) -> float:
        chr_p_all = 0
        chr_p_matched = 0
        chr_r_all = 0
        chr_r_matched = 0

        for hyp, ref in zip(hypotheses, references):
            hyp_joined = " ".join(hyp)
            hyp_chars = list(hyp_joined)
            hyp_chars = [x for x in hyp_chars if x not in self.ignored]

            ref_joined = " ".join(ref)
            ref_chars = list(ref_joined)
            ref_chars = [x for x in ref_chars if x not in self.ignored]

            # ChrP
            for i in range(len(hyp_chars) - self.n + 1):
                chr_p_all = chr_p_all + 1
                if "".join(hyp_chars[i:i + self.n]) in ref_joined:
                    chr_p_matched = chr_p_matched + 1

            # ChrR
            for i in range(len(ref_chars) - self.n + 1):
                chr_r_all = chr_r_all + 1
                if "".join(ref_chars[i:i + self.n]) in hyp_joined:
                    chr_r_matched = chr_r_matched + 1

        # If hyp/ref is too short we need to avoid division by zero
        if len(hyp_chars) < self.n or len(ref_chars) < self.n:
            if hyp_joined == ref_joined:
                return 1
            return 0

        chr_p = chr_p_matched / chr_p_all
        chr_r = chr_r_matched / chr_r_all

        if chr_p == 0 and chr_r == 0:
            return 0

        return ((1 + self.beta_2)
                * ((chr_p * chr_r) / (self.beta_2 * chr_p + chr_r)))


# pylint: disable=invalid-name
ChrF3 = ChrFEvaluator(beta=3)
