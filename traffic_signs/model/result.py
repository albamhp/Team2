class Result:

    """
    We define and initialize the different variables for the evaluation
    of the results
    """
    tp: float
    fp: float
    tn: float
    fn: float
    time: float

    def __init__(self, tp=0, fp=0, tn=0, fn=0, time=0):
        self.tp = tp
        self.fp = fp
        self.tn = tn
        self.fn = fn
        self.time = time

    def get_precision(self):
        return float(self.tp) / float(self.tp + self.fp)

    def get_accuracy(self):
        return float(self.tp + self.tn) / float(self.tp + self.fp + self.fn + self.tn)

    def get_specificity(self):
        return float(self.tn) / float(self.tn + self.fp)

    def get_recall(self):
        return float(self.tp) / float(self.tp + self.fn)
