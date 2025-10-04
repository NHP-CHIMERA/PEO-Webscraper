import pandas as pd
class DataHandler:
    def __init__(self, data):
        self.data = pd.DataFrame(data)

    def to_csv(self):
        df = self.data
        df_cleaned = df.drop_duplicates(subset=['RegNo'])
        print("Cleaned DataFrame:")
        print(df_cleaned)

        df.to_csv("grenada_electors.csv", index=False)
