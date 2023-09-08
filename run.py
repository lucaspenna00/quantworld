# RUN

from fundstracker import *

yr_i=2019
yr_f=2021
m=3


print("[DEBUG] Update")
update(yr_i, yr_f, m)

print("[DEBUG] update_INF")
update_INF(yr_i, yr_f, m)

print("[DEBUG] Summarize")
summarize(yr_i, yr_f, m)

print("[DEBUG] summarize_INF")
summarize_INF()

print("[DEBUG] summarize_eqt_pos")
summarize_eqt_pos()

print("[DEBUG] update_equities")
update_equities()


print("[DEBUG] rename equities")
rename_equities()