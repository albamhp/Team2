from typing import List, Tuple

from methods import AbstractMethod
from methods.operations import CompareHistograms, CompareHistogramsMethods, HistogramTypes
from model import Picture


class Method3(AbstractMethod):
    compare_histograms: CompareHistograms

    def __init__(self):
        self.compare_histograms = CompareHistograms(CompareHistogramsMethods.FULL_IMAGE, HistogramTypes.YCbCr)

    def query(self, picture: Picture) -> List[Tuple[Picture, float]]:
        res = self.compare_histograms.query(picture)
        return res

    def train(self, images: List[Picture]):
        self.compare_histograms.train(images)


instance = Method3()