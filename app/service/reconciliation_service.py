from django.core.files.storage import default_storage
import pandas as pd
import os


class ReconciliationService:
    def reconcile(self, source_file, target_file):
        source_file_path = default_storage.save('uploads/' + source_file.name, source_file)
        target_file_path = default_storage.save('uploads/' + target_file.name, target_file)
        # Read CSV files into pandas DataFrames
        source_df = pd.read_csv(source_file_path)
        target_df = pd.read_csv(target_file_path)
        return "uploaded"

