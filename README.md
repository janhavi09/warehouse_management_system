Project Explanation Loom Video :

https://www.loom.com/share/673e8aebca75458ebb0e074d742bd54f?sid=32efdc09-4c3d-4ef0-88d9-3dae6ae3bba7

✅ Part 1: Data Cleaning and Management 🔧 Functionalities Implemented: ✅ Created a SKUMapper class to map SKU → MSKU

✅ Handled combo products by linking multiple SKUs to a combo

✅ Loaded master mapping from Excel files (MSKU_with_SKUs.xlsx and Combos_SKUs.xlsx)

✅ Warnings generated for:

Unknown SKUs

Multiple MSKU matches

✅ Created SalesProcessor class to:

Read sales data from Amazon, Flipkart, Meesho, etc.

Map SKUs to MSKUs

Generate a summary of quantity sold (per MSKU)

✅ inventory_adjuster.py adjusts inventory by subtracting sales from opening stock

✅ Part 2: Relational DB Alternative (Airtable) 🔍 Work Completed: ✅ Evaluated and chose Airtable for non-technical data viewing

✅ Data (like SKUs, sales, inventory) uploaded and saved to Airtable

✅ Confirmed: No need to download separately once uploaded to Airtable

✅ Part 3: Integration & Finalization 🖥️ Built a Web App with Streamlit: ✅ Created a complete Streamlit-based UI app_streamlite.py

✅ Features:

Upload MSKU mapping, combo SKUs, inventory file, and multiple sales files

Process and clean data in browser

Show Sales Summary

Adjust inventory

Download buttons for both final reports

📊 Added Dashboard: ✅ Total units sold

✅ Bar chart for Top 10 best-selling MSKUs

✅ Bar chart for Top 10 available stock

✅ Low stock alert (<5 units)

🔄 Current Status Everything is working:

✅ Backend data processing ✅

✅ Frontend GUI (via Streamlit) ✅

✅ Dashboards & downloads ✅

✅ Airtable integration ✅
