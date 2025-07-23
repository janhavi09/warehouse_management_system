# inventory_adjuster.py

import pandas as pd

def adjust_inventory(inventory_file, sales_summary_file, output_file):
    # Load inventory data
    inv_df = pd.read_excel(inventory_file)
    inv_df.columns = [col.strip().lower() for col in inv_df.columns]
    
    inventory = inv_df[['msku', 'opening stock']].copy()
    inventory.columns = ['msku', 'opening_stock']

    # Load sales summary
    sales_df = pd.read_excel(sales_summary_file)
    sales_df.columns = [col.strip().lower() for col in sales_df.columns]

    # Merge both
    merged = pd.merge(inventory, sales_df, on='msku', how='left')

    # Fill missing sales with 0
    merged['quantity_sold'] = merged['quantity_sold'].fillna(0)

    # Calculate final stock
    merged['available_stock'] = merged['opening_stock'] - merged['quantity_sold']

    # Save result
    merged.to_excel(output_file, index=False)
    print(f"✅ Inventory adjusted and saved to {output_file}")
