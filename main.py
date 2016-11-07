import csvs
import db
if __name__ == '__main__':
    ing_records = csvs.load_ing_records(r'')
    db.accumulate_records(ing_records)