import re


class MilliGramConverter:
    valid_ingredient_units = ["mg"]

    def __init__(self, ingredient_unit):
        if ingredient_unit not in self.valid_ingredient_units:
            raise ValueError(f"{ingredient_unit}を{self.__class__.__name__}はサポートしていません")

    def convert(self, med, ingredient_dosage):
        unit_ingredient_gram = IngredientGramEstimator().estimate(med)
        unit_ingredient_mg = unit_ingredient_gram * (10**3)
        return ingredient_dosage / unit_ingredient_mg


class MueGramConverter:
    valid_ingredient_units = ["μg"]

    def __init__(self, ingredient_unit):
        if ingredient_unit not in self.valid_ingredient_units:
            raise ValueError(f"{ingredient_unit}を{self.__class__.__name__}はサポートしていません")

    def convert(self, med, ingredient_dosage):
        unit_ingredient_gram = IngredientGramEstimator().estimate(med)
        unit_ingredient_mueg = unit_ingredient_gram * (10**6)
        return ingredient_dosage / unit_ingredient_mueg


class IngredientGramEstimator:
    # 医薬品に含まれる成分量をgで取得する
    def estimate(self, med):
        ingredient_percent = self._get_ingredient_ratio(med)
        return ingredient_percent / 100

    @staticmethod
    def _get_ingredient_ratio(med):
        if re.search("%.+%.+", med) is not None:
            raise ValueError(f"{med}の成分量パーセントが複数存在します.")

        # 医薬品名に含まれる N% という数字を正規表現で取得する
        search_percent = re.search("[0-9|\\.]+%", med)
        if search_percent is None:
            raise ValueError(f"{med}の成分量パーセントが取得できませんでした")
        percent_str = search_percent.group().strip("%")
        return float(percent_str)


class IngredientDosageConverter:
    # 医薬品の成分量(力価)処方された医薬品用量を標準の薬価収載用量に変換する処理
    # 基本的には(mg or μg)で処方される.
    # 散剤だと出力の単位はg, 液剤だとmlになる.

    # validは通例と変わらない場合は不要
    valid_classes = [MilliGramConverter, MueGramConverter]

    def __init__(self):
        pass

    def convert(self, med, ingredient_dosage, ingredient_unit):
        convert_class = self._select_converter_class(ingredient_unit)  # selectは恣意的なのでgetが良い
        standard_dosage = convert_class(ingredient_unit).convert(med, ingredient_dosage)
        return standard_dosage

    def _select_converter_class(self, ingredient_unit):
        for class_ in self.valid_classes:
            if ingredient_unit in class_.valid_ingredient_units:
                return class_
        else:
            raise ValueError(f"{ingredient_unit}はサポートされていません")
