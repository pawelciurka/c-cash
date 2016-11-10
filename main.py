import csvs
import db
if __name__ == '__main__':
    ing_records = csvs.read_ing_csv(r'C:\Users\Pawel\PycharmProjects\finanse\csv_files\history (2).csv')
    db.accumulate_records(ing_records)