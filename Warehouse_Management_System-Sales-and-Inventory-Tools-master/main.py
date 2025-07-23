# this is for generate report based on direct file from master_data and sales_data
import pandas as pd

from sku_mapper import SKUMapping

class SKUMapper:
    def __init__(self, msku_sku_path, combo_path):
        self.sku_to_msku = {}          # For simple SKU mapping
        self.combo_to_components = {}  # For combo mapping

        self.load_msku_mapping(msku_sku_path)
        self.load_combo_mapping(combo_path)

    def load_msku_mapping(self, path):
        try:
            df = pd.read_excel(path)
            df.columns = [str(col).strip().lower() for col in df.columns]

            grouped = df.groupby('sku')['msku'].apply(lambda x: list(set(x.dropna()))).to_dict()

            for sku, mskus in grouped.items():
                if len(mskus) == 1:
                    self.sku_to_msku[sku] = mskus[0]
                elif len(mskus) > 1:
                    print(f"⚠️ Warning: Multiple MSKUs found for SKU {sku} → {mskus}. Using first.")
                    self.sku_to_msku[sku] = mskus[0]  # or skip if unsure
        except Exception as e:
            print(f"Error loading MSKU mapping: {e}")


    def load_combo_mapping(self, path):
        try:
            df = pd.read_excel(path)

            # Normalize column names (strip spaces, lowercase)
            df.columns = [str(col).strip() for col in df.columns]

            for _, row in df.iterrows():
                combo = str(row['Combo']).strip()
                components = [str(row[f'SKU{i}']).strip()
                            for i in range(1, 15)
                            if f'SKU{i}' in row and pd.notna(row[f'SKU{i}'])]
                if combo and components:
                    self.combo_to_components[combo] = components
        except Exception as e:
            print(f"Error loading combo mapping: {e}")


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


# from main import SKUMapper

mapper = SKUMapper("master_data/MSKU_with_SKUs.xlsx", "master_data/Combos_SKUs.xlsx")

print(mapper.get_msku("CSTE_0002_ST_Bts_Pillow_Tata"))     # ➝ Should return MSKU
print(mapper.get_msku("ST-BTS-cooky-koya-rj-tata-FBA"))    # ➝ Should return combo MSKUs

from sales_processor import SalesProcessor

mapper = SKUMapping()
mapper.load_msku_mapping("master_data/MSKU_with_SKUs.xlsx")
mapper.load_combo_mapping("master_data/Combos_skus.xlsx")

processor = SalesProcessor(mapper)

# Provide correct file paths
processor.process_file("sales_data/CSTE_AMAZON.xlsx", "cste_amazon")
processor.process_file("sales_data/CSTE_FK.xlsx", "cste_fk")
processor.process_file("sales_data/CSTE_MEESHO.xlsx", "cste_meesho")
processor.process_file("sales_data/GL_FK.xlsx", "gi_fk")
processor.process_file("sales_data/RUDRA_MEESHO.xlsx", "rudra_meesho")

df_summary = processor.get_sales_summary()
df_summary.to_excel("final_sales_summary.xlsx", index=False)

print("✅ Sales summary exported to final_sales_summary.xlsx")

from inventory_adjuster import adjust_inventory

adjust_inventory(
    inventory_file="master_data/Currency_Inventory.xlsx", 
    sales_summary_file="final_sales_summary.xlsx", 
    output_file="adjusted_inventory_report.xlsx"
)

