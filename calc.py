import re


class IngredientDosageCalculator:
    # 医薬品の成分量(力価)処方された医薬品用量を標準の薬価収載用量に変換する処理
    # 基本的には(mg or μg)で処方される.
    # 散剤だと出力の単位はg, 液剤だとmlになる.

    def calc(self, med, ingredient_amount, ingredient_unit):
        gram_coefficient = self._get_gram_coefficient(ingredient_unit)
        unit_ingredient_gram = IngredientGramCalculator().calc(med)
        standard_dosage = ingredient_amount / (unit_ingredient_gram * gram_coefficient)
        return standard_dosage

    def _get_gram_coefficient(self, ingredient_unit):
        coefficient_dict = {"mg": 10**3, "μg": 10**6}
        coefficient = coefficient_dict.get(ingredient_unit, None)
        if coefficient is None:
            raise ValueError(f"{ingredient_unit}はサポートされていません.")


class IngredientGramCalculator:
    # 医薬品に含まれる成分量をgで取得する
    def calc(self, med):
        percent = self._get_ingredient_ratio(med)
        return percent / 100

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
