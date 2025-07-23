import pandas as pd
from collections import defaultdict

class SalesProcessor:
    def __init__(self, mapper):
        self.mapper = mapper
        self.msku_sales = defaultdict(int)

    def process_file(self, filepath, source):
        df = pd.read_excel(filepath)
        df.columns = [str(col).strip().lower() for col in df.columns]

        # Source-specific SKU/Qty column mapping
        if source == "cste_amazon":
            sku_col, qty_col = "msku", "quantity"
        elif source == "cste_fk":
            sku_col, qty_col = "sku", "quantity"
        elif source == "cste_meesho":
            sku_col, qty_col = "sku", "quantity"
        elif source == "gi_fk":
            sku_col, qty_col = "sku", "quantity"
        elif source == "rudra_meesho":
            sku_col, qty_col = "sku", "quantity"
        else:
            print(f"❌ Unknown source: {source}")
            return

        for _, row in df.iterrows():
            sku = str(row.get(sku_col, "")).strip()
            quantity = row.get(qty_col, 0)

            if not sku or pd.isna(quantity):
                continue

            mskus = self.mapper.get_msku(sku)
            if mskus:
                for msku in mskus:
                    self.msku_sales[msku] += int(quantity)

    def get_sales_summary(self):
        return pd.DataFrame([
            {"msku": msku, "quantity_sold": qty}
            for msku, qty in self.msku_sales.items()
        ])
