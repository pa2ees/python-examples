open_session -name "D:/Altera Projects/Enterprise/adc_x/adc.stp"
run -data_log log1
export_data_log -data_log log1 -filename "D:/Google Drive/data2/barf.csv" -format csv
close_session