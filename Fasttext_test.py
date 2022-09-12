import fasttext.util

ft = fasttext.load_model(r'cc.pl.300.bin/cc.pl.300.bin')

print(ft.get_dimension())
print(ft.get_nearest_neighbors("talerz"))
