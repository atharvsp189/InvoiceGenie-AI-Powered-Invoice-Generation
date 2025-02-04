import json

with open('invoice.json') as invoicejson:
    invoice = json.load(invoicejson)

with open('cell_no.json') as cell:
    cell = json.load(cell)

# for val in invoice:
#     print(val)

# for val in invoice:
#     for j in invoice[val]:
#         print(j)

# for val in invoice:
#     for j in invoice[val]:
#         if isinstance(invoice[val][j], dict):
#             for k in invoice[val][j]:
#                 print(k)
#         else:
#             print(j)

for val in invoice:
    for j in invoice[val]:
        if isinstance(invoice[val][j], dict):
            for k in invoice[val][j]:
                print(k, " ", invoice[val][j][k], cell[val][j][k])
        else:
            print(j, " ", invoice[val][j], cell[val][j])