# sku_mapper.py

import pandas as pd

class SKUMapping:
    def __init__(self,  msku_file=None, combo_file=None):
        self.sku_to_msku = {}
        self.combo_to_components = {}

        if msku_file:
            self.load_msku_mapping(msku_file)
        if combo_file:
            self.load_combo_mapping(combo_file)

    def load_msku_mapping(self, file_path):
        try:
            df = pd.read_excel(file_path)
            df.columns = [str(col).strip().lower() for col in df.columns]

            grouped = df.groupby('sku')['msku'].apply(lambda x: list(set(x.dropna()))).to_dict()

            for sku, mskus in grouped.items():
                if len(mskus) == 1:
                    self.sku_to_msku[sku] = mskus[0]
                elif len(mskus) > 1:
                    print(f"⚠️ Warning: Multiple MSKUs found for SKU {sku} → {mskus}. Using first.")
                    self.sku_to_msku[sku] = mskus[0]

        except Exception as e:
            print(f"❌ Error loading MSKU mapping: {e}")

    def load_combo_mapping(self, file_path):
        try:
            df = pd.read_excel(file_path)
            df.columns = [str(col).strip().lower() for col in df.columns]

            for _, row in df.iterrows():
                combo = str(row.get("combo", "")).strip()
                if not combo:
                    continue
                skus = []
                for col in df.columns:
                    if col.startswith("sku"):
                        val = str(row.get(col, "")).strip()
                        if val:
                            skus.append(val)
                self.combo_to_components[combo] = skus

        except Exception as e:
            print(f"❌ Error loading combo mapping: {e}")

    def get_msku(self, sku_or_combo, ignore_unknown=True):
        if sku_or_combo in self.combo_to_components:
            mskus = []
            for component in self.combo_to_components[sku_or_combo]:
                msku = self.sku_to_msku.get(component)
                if msku:
                    mskus.append(msku)
                elif not ignore_unknown:
                    mskus.append(f"UNKNOWN({component})")
            return mskus
        else:
            msku = self.sku_to_msku.get(sku_or_combo)
            if msku:
                return [msku]
            elif not ignore_unknown:
                return [f"UNKNOWN({sku_or_combo})"]
            return [] if ignore_unknown else [f"UNKNOWN({sku_or_combo})"]
