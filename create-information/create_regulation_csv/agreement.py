import psycopg2
import os
import sys
import functions

from application import application

my_agreement = sys.argv[1].lower().strip()
if my_agreement == "canada":
    regulations = ["R1585/17", "R1772/17", "R1781/17", "R1586/17", "D0037/17"]
elif my_agreement == "southkorea":
    regulations = ["R1093/11", "D0265/11"]
elif my_agreement == "switzerland":
    regulations = ["D0123/01", "R2114/99", "R0050/04", "R1565/07", "R0082/13", "R1126/09", "R1223/12", "A0003/73", "D0093/06", "D0309/02", "D0559/86", "D0955/05"]
elif my_agreement == "sadc":
    regulations = ["R2253/16", "D1623/16", "R0882/17"]
elif my_agreement == "cariforum":
    regulations = ["D0805/08"]
elif my_agreement == "esa":
    regulations = ["D1923/17", "D0196/12"]
elif my_agreement == "ghana":
    regulations = ["D1850/16"]
elif my_agreement == "pacific":
    regulations = ["D0729/09"]
elif my_agreement == "chile":
    regulations = ["D0792/06", "R0610/09", "D0979/02", "R0312/03"]
elif my_agreement == "israel":
    regulations = ["R1474/00", "R1338/07", "R1153/09", "R1154/09", "R1831/96", "D0066/13"]
elif my_agreement == "palestine":
    regulations = ["D0430/97", "D0824/11"]
elif my_agreement == "singapore":
    regulations = []
elif my_agreement == "centralamerica":
    regulations = ["D120734", "R130974", "R130975", "R130976", "R130977", "R131011", "R131012", "R130922", "R130923", "R131366"]
elif my_agreement == "tunisia":
    regulations = ["R010747", "R061918", "R060973", "D980238", "D000822"]
elif my_agreement == "jordan":
    regulations = ["D060067", "D020357", "R060019"]
elif my_agreement == "kosovo":
    regulations = ["R120374", "R090891", "R171466", "D160342", "R171464", "R120374", "R090891"]
elif my_agreement == "montenegro":
    regulations = ["R080053", "R080497", "R101255", "D100224"]
elif my_agreement == "macedonia":
    regulations = ["R012597", "R120374", "R090891", "R101255", "D040239"]
elif my_agreement == "albania":
    regulations = ["R090891", "D090332", "R061742", "R061916"]
elif my_agreement == "cotedivoire":
    regulations = ["R161076"]
elif my_agreement == "cameroon":
    regulations = ["D090152"]
elif my_agreement == "faroeislands":
    regulations = ["R090054", "R071381", "R992471", "D970126", "D990456", "D060561"]
elif my_agreement == "andean":
    regulations = ["R130405", "R130741", "R170754", "R170120", "R130404", "R130740"]
elif my_agreement == "eac":
    regulations = []
elif my_agreement == "morocco":
    regulations = ["R120812", "D000204", "D120497", "D030914"]
elif my_agreement == "lebanon":
    regulations = ["R030209", "R060973", "R961831", "D060356"]
elif my_agreement == "egypt":
    regulations = ["D100240", "D040635", "R100449", "R071338"]
elif my_agreement == "serbia":
    regulations = ["R150781", "R090891", "R101255", "D100036", "D130490", "R110059", "R120374"]
elif my_agreement == "ukraine":
    regulations = ["R152076", "R152077", "R152078", "R152079", "R152081", "R152405", "D140295", "R171566"]
elif my_agreement == "georgia":
    regulations = ["D140494", "R140989"]
elif my_agreement == "mexico":
    regulations = ["R080821", "D000415"]
elif my_agreement == "turkey":
    regulations = ["R070816", "R061712", "R090933", "R141335", "D960142", "D980223", "D960528"]
elif my_agreement == "japan":
    regulations = []
elif my_agreement == "algeria":
    regulations = ["R051460", "R051653", "D050690"]
elif my_agreement == "moldova":
    regulations = ["D140492", "R140988", "R152080"]
elif my_agreement == "vietnam":
    regulations = []
elif my_agreement == "bosnia":
    regulations = ["R110343", "R110354", "R090891", "R101255", "D080474"]


app = functions.app
for regulation in regulations:
    app.reinitialise()
    app.create_agreement(my_agreement) 
    regulation_id = functions.mangle(regulation)
    print ("Creating documents for " + my_agreement + " agreement using regulation " + regulation_id)
    app.createRegulationCSV(regulation_id)