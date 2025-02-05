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
                cell_no = cell[val][j][k]
                value = invoice[val][j][k]
                print(k, " ", value, cell_no)
        else:
            cell_no = cell[val][j]
            value = invoice[val][j]
            print(j, " ", value, cell_no)