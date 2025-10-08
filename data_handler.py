import pandas as pd
class DataHandler:
    def __init__(self, data):
        self.data = pd.DataFrame(data)

    def to_csv(self):
        df = self.data
        df_cleaned = df.drop_duplicates(subset=['RegNo'])
        print("Cleaned DataFrame:")
        print(df_cleaned)
        df = df.sort_values(by='RegNo')
        df.to_csv("grenada_electors.csv", index=False)


    def post_processing(self):
        csv_df = pd.read_csv("grenada_electors.csv")
        sorted_df = csv_df.sort_values(by='RegNo')
        sorted_df.to_csv("grenada_electors_sorted.csv", index=False)