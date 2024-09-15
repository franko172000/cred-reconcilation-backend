import os
from typing import List

import dateparser
import pandas as pd
from django.core.files.storage import default_storage

from app.models import Upload, Record


class ReconciliationService:

    def __init__(self):
        self.upload_model = Upload.objects
        self.record_model = Record.objects
        pass

    def reconcile(self, data):
        source_file = data['source_file']
        target_file = data['target_file']
        source_file_path = default_storage.save('uploads/' + source_file.name, source_file)
        target_file_path = default_storage.save('uploads/' + target_file.name, target_file)

        # Read CSV files into pandas DataFrames
        source_df = pd.read_csv(source_file_path)
        target_df = pd.read_csv(target_file_path)

        upload = self.upload_model.create(source_file=source_file_path, target_file=target_file_path, title=data['title'],
                                 description=data['description'])
        # Perform reconciliation
        report = self.reconcile_data(upload.id,source_df, target_df)

        # update upload record
        upload.refresh_from_db()
        upload.missing_in_target = report['missing_in_target']
        upload.missing_in_source = report['missing_in_source']
        upload.discrepancies = report['discrepancies']
        upload.save(update_fields=['missing_in_target', 'missing_in_source', 'discrepancies'])

        # upload.update_report(report)
        # print(report);

        # Clean up the files after processing
        os.remove(source_file_path)
        os.remove(target_file_path)

        return report

    def reconcile_data(self, upload_id, source, target):
        source_df = pd.DataFrame(self.__normalise_data(source))
        target_df = pd.DataFrame(self.__normalise_data(target))

        # Assuming 'id' is the primary key for identifying records
        source_ids = set(source_df['id'])
        target_ids = set(target_df['id'])

        # find records in both
        reconciled_records = []

        # Find records missing in the target
        missing_in_target = source_df[~source_df['id'].isin(target_ids)].to_dict(orient='records')

        # Find records missing in the source
        missing_in_source = target_df[~target_df['id'].isin(source_ids)].to_dict(orient='records')

        # Find discrepancies (comparing rows with the same ID)
        discrepancies = []
        for common_id in source_ids.intersection(target_ids):
            source_row = source_df[source_df['id'] == common_id].to_dict(orient='records')[0]
            target_row = target_df[target_df['id'] == common_id].to_dict(orient='records')[0]

            diff = {}
            for col in source_row.keys():
                if source_row[col] != target_row[col]:
                    diff[col] = {'source': source_row[col], 'target': target_row[col]}
            if diff:
                discrepancies.append({'id': common_id, 'differences': diff})

            reconciled_records.append({
                'name': source_row['name'],
                'account_number': source_row['account_number'],
                'transaction_date': source_row['transaction_date'],
                'balance': source_row['balance'],
                'description': source_row['description'],
                "upload_id": upload_id,
            })

        # save same records to db
        self.record_model.bulk_create([
            Record(**values) for values in reconciled_records
        ], batch_size=100)

        # Return the reconciliation report
        return {
            "missing_in_target": missing_in_target,
            "missing_in_source": missing_in_source,
            "discrepancies": discrepancies,
        }

    def list_uploads(self) -> List[Upload]:
        return self.upload_model.all().order_by('-id')

    def __normalise_data(self, csv_data):
        data_dict = csv_data.to_dict(orient='records')
        # print(data_dict)
        for index in range(len(data_dict)):
            for col in data_dict[index].keys():
                row = data_dict[index]
                column_data = row[col]
                column_df = pd.DataFrame(row, index=[index])

                # check for is NaN values
                if column_df[col].isna().bool():
                    data_dict[index][col] = 'no data'

                if type(column_data) == str:
                    # trim and strip slashes
                    row[col] = column_data.strip().strip("/").lower()

                # format date
                if col == 'transaction_date':
                    row[col] = self.__format_date(column_data)

                data_dict[index] = row
        return data_dict

    def __format_date(self, date_str) -> str:
        parsed_date = dateparser.parse(date_str)
        return parsed_date.strftime("%Y-%m-%d")

    def __validate_columns(self, columns):
        pass
