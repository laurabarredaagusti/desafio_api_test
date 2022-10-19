cons_prod_fam_products = '''SELECT "Consumption", "Product_family", "Label" FROM products WHERE ("Brand" = %s AND "Model" = %s) OR ("Brand" = %s AND "Model" = %s);'''

brand_model_product = '''SELECT "Brand", "Model" FROM products WHERE "Product_family" = %s;'''

consum_type_prodfamily = '''SELECT "Consumption_type" FROM product_family WHERE "Product_family" = %s;'''

brand_model_prodfam_productid = '''SELECT "Brand", "Model", "Type" FROM products_id WHERE ("Id" = %s) OR ("Id" = %s);'''

price_kwh_date = '''SELECT "Price" FROM price_kwh WHERE "Date" = %s;'''

insert_date_price_kwh = '''INSERT INTO price_kwh ("Date", "Price") VALUES (%s, %s);'''

insert_sessionid_usersearch = '''INSERT INTO user_search ("Session_id") VALUES (%s);'''

brands_models_usersearch = '''SELECT "Brand1", "Model1", "Brand2", "Model2" FROM user_search WHERE "Session_id" = %s;'''

cost_usersearch = '''SELECT "Cost1", "Cost2" FROM user_search WHERE "Session_id" = %s;'''

update_calculate = '''UPDATE user_search SET "Brand1" = %s, "Model1" = %s, "Brand2" = %s, "Model2" = %s, "Hours_day" = %s, "Price_kwh" = %s, "Datetime" = %s, "Cost1" = %s, "Cost2" = %s, "Product_family" = %s WHERE "Session_id" = %s;'''

update_usersearch_brandmodel = '''UPDATE user_search SET "Brand1" = %s, "Model1" = %s, "Brand2" = %s, "Model2" = %s WHERE "Session_id" = %s;'''

update_usersearch_advanced = '''UPDATE user_search SET "Crossing_year" = %s, "Crossing_cost" = %s WHERE "Session_id" = %s;'''