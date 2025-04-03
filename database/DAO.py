from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select year(gds.Date) as year
                        from go_daily_sales gds 
                        group by year(gds.Date) """

            cursor.execute(query)

            for row in cursor:
                res.append(row["year"])

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getBrand():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select gp.Product_brand as brand
                        from go_products gp 
                        group by gp.Product_brand"""

            cursor.execute(query)

            for row in cursor:
                res.append(row["brand"])

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getRetailers():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * from go_retailers"""

            cursor.execute(query)

            for row in cursor:
                res.append(Retailer(**row))

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getTopVendite(anno, brand, retailer):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select gds.Date as data, (gds.Quantity * gds.Unit_sale_price) as ricavo, gds.Retailer_code as rCode, gds.Product_number as pNumber
                        from go_daily_sales gds, go_products gp 
                        where gds.Product_number = gp.Product_number and year(gds.Date)=coalesce(%s, year(gds.Date)) and gp.Product_brand=coalesce(%s, Product_brand) and gds.Retailer_code=coalesce(%s, Retailer_code)
                        order by (gds.Quantity * gds.Unit_sale_price) desc
                        limit 5"""

            cursor.execute(query, (anno, brand, retailer))

            for row in cursor:
                #res.append(f"Data: {row["data"]}; Ricavo: {row["ricavo"]}; Retailer: {row["rCode"]}; Product: {row["pNumber"]}")
                res.append((row["data"], row["ricavo"], row["rCode"], row["pNumber"]))

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getAnalizzaVendite(anno, brand, retailer):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select sum(gds.Quantity * gds.Unit_sale_price) as ricavoTot, 
                            count(*) as nVendite, count(distinct gds.Retailer_code) as nRetailer, 
                            count(distinct gp.Product_number) as nProdotti
                        from go_daily_sales gds, go_products gp 
                        where gds.Product_number = gp.Product_number and year(gds.Date)=coalesce(%s, year(gds.Date)) and gp.Product_brand=coalesce(%s, gp.Product_brand) and gds.Retailer_code=coalesce(%s, gds.Retailer_code)"""

            cursor.execute(query, (anno, brand, retailer))

            for row in cursor:
                res.append((row["ricavoTot"], row["nVendite"], row["nRetailer"], row["nProdotti"]))

            cursor.close()
            cnx.close()
            return res

