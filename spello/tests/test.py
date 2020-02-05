import pandas as pd
from pathlib import Path

from spello.utils import get_clean_text
from spello.model import SpellCorrectionModel

def automatedtestforspellcheck(languages):
    for language in languages:
        sp = SpellCorrectionModel(language=language)
        sp.load(f'C:\\Users\\LAP\\{language}.pkl')
        dir = Path(__file__).resolve().parent
        test_data = pd.read_csv(dir / f"{language}.csv")

        def correct(text):
            try:
                spello_out = sp.spell_correct(text)
                return spello_out["spell_corrected_text"]
            except Exception as e:
                return e

        test_data["Output"] = test_data["Sentence with Mistake"].apply(correct)
        test_data["Clean_original"] = test_data["Original Sentence"].apply(get_clean_text)
        test_data["Status"] = test_data["Clean_original"] == test_data["Output"]
        out_path = dir / f"{language}_out.csv"
        results = test_data['Status'].value_counts()
        print(f"Results for {language} are \n{results}\n")
        print(f"Dumping results for {language} at {out_path} ...")
        test_data.to_csv(out_path, index=False)


if __name__ == "__main__":
    languages = ["en"]
    automatedtestforspellcheck(languages)