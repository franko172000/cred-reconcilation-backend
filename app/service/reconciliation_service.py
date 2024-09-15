from django.core.files.storage import default_storage
import pandas as pd
import os
import dateparser
from rest_framework.exceptions import NotFound


class ReconciliationService:
    def reconcile(self, source_file, target_file):
        source_file_path = default_storage.save('uploads/' + source_file.name, source_file)
        target_file_path = default_storage.save('uploads/' + target_file.name, target_file)

        # Read CSV files into pandas DataFrames
        source_df = pd.read_csv(source_file_path)
        target_df = pd.read_csv(target_file_path)

        # Perform reconciliation
        report = self.reconcile_data(source_df, target_df)
        # print(report);

        # Clean up the files after processing
        os.remove(source_file_path)
        os.remove(target_file_path)
        return report

    def reconcile_data(self, source, target):
        source_df = pd.DataFrame(self.__normalise_data(source))
        target_df = pd.DataFrame(self.__normalise_data(target))

        # Assuming 'id' is the primary key for identifying records
        source_ids = set(source_df['id'])
        target_ids = set(target_df['id'])

        # Find records missing in the target
        missing_in_target = source_df[~source_df['id'].isin(target_ids)].to_dict(orient='records')
        #
        # # Find records missing in the source
        missing_in_source = target_df[~target_df['id'].isin(source_ids)].to_dict(orient='records')

        # Find discrepancies (comparing rows with the same ID)
        discrepancies = []
        for common_id in source_ids.intersection(target_ids):
            source_row = source_df[source_df['id'] == common_id].to_dict(orient='records')[0]
            target_row = target_df[target_df['id'] == common_id].to_dict(orient='records')[0]

            diff = {}
            for col in source_row.keys():
                print(target_row[col])
                if source_row[col] != target_row[col]:
                    diff[col] = {'source': source_row[col], 'target': target_row[col]}
            if diff:
                discrepancies.append({'id': common_id, 'differences': diff})

        # Return the reconciliation report
        return {
            "missing_in_target": missing_in_target,
            "missing_in_source": missing_in_source,
            "discrepancies": discrepancies
        }

    def __normalise_data(self, csv_data):
        data_dict = csv_data.to_dict(orient='records')
        # print(data_dict)
        for index in range(len(data_dict)):
            for col in data_dict[index].keys():
                row = data_dict[index]
                column_data = row[col]
                column_df = pd.DataFrame(row, index=[index])

                if column_df[col].isna().bool():
                    data_dict[index][col] = 'no data'
                if type(column_data) == str:
                    # trim and strip slashes
                    row[col] = column_data.strip().strip("/").lower()
                # format date
                if col == 'created_date':
                    row[col] = self.__format_date(column_data)

                data_dict[index] = row
        return data_dict

    def __format_date(self, date_str) -> str:
        parsed_date = dateparser.parse(date_str)
        return parsed_date.strftime("%a %d, %Y")
