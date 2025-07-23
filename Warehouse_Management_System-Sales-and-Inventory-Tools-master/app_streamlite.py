import streamlit as st
import pandas as pd
from sku_mapper import SKUMapping
from sales_processor import SalesProcessor
from inventory_adjuster import adjust_inventory
import os
import io
st.set_page_config(page_title="WMS Sales Processor", layout="wide")

st.title("📦 Warehouse Management System - Sales & Inventory Tool")

# --- File Upload ---
st.header("Step 1: Upload Files")

msku_file = st.file_uploader("Upload MSKU with SKUs file", type=["xlsx"])
combo_file = st.file_uploader("Upload Combo SKUs file", type=["xlsx"])
inventory_file = st.file_uploader("Upload Current Inventory file", type=["xlsx"])

sales_files = st.file_uploader("Upload Sales Data Files (multiple allowed)", type=["xlsx"], accept_multiple_files=True)

if msku_file and combo_file and inventory_file and sales_files:
    with st.spinner("🔄 Loading mappings..."):
        mapper = SKUMapping(msku_file, combo_file)

    with st.spinner("🧾 Processing sales files..."):
        processor = SalesProcessor(mapper)
        for uploaded_file in sales_files:
            fname = uploaded_file.name.lower()
            if "amazon" in fname:
                source = "cste_amazon"
            elif "fk" in fname and "gi" in fname:
                source = "gi_fk"
            elif "fk" in fname:
                source = "cste_fk"
            elif "meesho" in fname and "rudra" in fname:
                source = "rudra_meesho"
            elif "meesho" in fname:
                source = "cste_meesho"
            else:
                st.warning(f" Could not identify source for: {fname}")
                continue

            processor.process_file(uploaded_file, source)

        summary_df = processor.get_sales_summary()
        st.success(" Sales summary generated.")

        st.dataframe(summary_df)

        # Convert dataframe to Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            summary_df.to_excel(writer, index=False)
        output.seek(0)

        # Now use download_button with buffer
        st.download_button(
            label="📥 Download Sales Summary",
            data=output,
            file_name="final_sales_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        with st.spinner("🔄 Adjusting inventory..."):
            inventory_file.seek(0)

            # Save sales summary
            summary_df.to_excel("final_sales_summary.xlsx", index=False)

            # Adjust inventory using your existing function
            adjust_inventory(inventory_file, "final_sales_summary.xlsx", "adjusted_inventory_report.xlsx")

            # Read adjusted data
            adjusted_df = pd.read_excel("adjusted_inventory_report.xlsx")
            st.success(" Inventory adjusted.")

            # Display DataFrame
            st.dataframe(adjusted_df)

            # Prepare Excel download via BytesIO
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                adjusted_df.to_excel(writer, index=False)
            output.seek(0)

            # Download button with correct format
            st.download_button(
                label="📥 Download Adjusted Inventory Report",
                data=output,
                file_name="adjusted_inventory_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # --- Dashboard Section ---
        st.subheader("📊 Inventory & Sales Dashboard")

        # Total MSKUs Sold
        total_units_sold = summary_df["quantity_sold"].sum()
        st.metric("Total Units Sold", int(total_units_sold))

        # Top 10 Best-Selling MSKUs
        st.markdown("#### 🔝 Top 10 Best-Selling MSKUs")
        top_selling = summary_df.sort_values(by="quantity_sold", ascending=False).head(10)
        st.bar_chart(top_selling.set_index('msku'))

        # Top 10 by Available Stock
        st.markdown("#### 📦 Top 10 MSKUs by Available Stock")
        stock_chart_data = adjusted_df[['msku', 'available_stock']].sort_values(by='available_stock', ascending=False).head(10)
        st.bar_chart(stock_chart_data.set_index('msku'))

        # Low Stock Alert
        low_stock = adjusted_df[adjusted_df['available_stock'] < 5]
        if not low_stock.empty:
            st.warning("⚠️ Low Stock Alert (Available < 5)")
            st.dataframe(low_stock)
else:
    st.info("Please upload all required files to proceed.")
