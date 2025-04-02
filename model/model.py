from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getAnni(self):
        anni = DAO.getAnni()
        anni.sort()
        return anni

    def getBrand(self):
        brand = DAO.getBrand()
        brand.sort()
        return brand

    def getRetailers(self):
        retailers = DAO.getRetailers()
        retailers.sort(key=lambda x: x.Retailer_name)
        return retailers

    def getTopVendite(self, anno, brand, retailer):
        return DAO.getTopVendite(anno, brand, retailer)
