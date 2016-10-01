import db

database_client = db.DatabaseClient()
database_client.insert_contractor(db.ContractorRecord(contractor_name='Ryszard Lubicz'))
database_client.insert_contractor(db.ContractorRecord(contractor_name='Pawel Lubicz'))