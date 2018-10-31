import csv

# Kalkulasi hutang
# banyak hutang
def hutangBanyak(n): 
    if n >= 80:
        return 1
    elif n <= 60:
        return 0
    else:
        return (n - 60) / (80 - 60)

# hutang yg normal
def hutangNormal(n): 
    if 50 <= n <= 70:
        return 1
    elif 30 < n < 50:
        return (n - 30) / (50 - 30)
    elif 70 < n < 80:
        return (80 - n) / (80 - 70)
    else:
        return 0

# hutang rendah
def hutangRendah(n): 
    if n <= 30:
        return 1
    elif n >= 50:
        return 0
    else:
        return (50 - n) / (50 - 30)

#nilai hutang
def nilaiHutang(n):
    Banyak = hutangBanyak(n)
    Normal = hutangNormal(n)
    Rendah = hutangRendah(n)
    return Banyak, Normal, Rendah

# Untuk kalkulasi penghasilan
# Untuk yang penghasilan tinggi
def penghasilanTinggi(n): 
    if n >= 1.7:
        return 1
    elif n <= 1.2:
        return 0
    else:
        return (n - 1.2) / (1.7 - 1.2)

# untuk penghasilan rata-rata
def penghasilanRata(n): 
    if 1.0 <= n <= 1.4:
        return 1
    elif 0.8 < n < 1.0:
        return (n - 0.8) / (1.0 - 0.8)
    elif 1.4 < n < 1.6:
        return (1.6 - n) / (1.6 - 1.4)
    else:
        return 0

# Untuk pendapatan di bawah rata rata
def penghasilanBawahRata(n): 
    if 0.6 <= n <= 1:
        return 1
    elif 0.4 < n < 0.6:
        return (n - 0.4) / (0.6 - 0.4)
    elif 1 < n < 1.2:
        return (1.2 - n) / (1.2 - 1)
    else:
        return 0
        
# untuk yang penghasilan rendah
def penghasilanRendah(n): 
    if n <= 0.3:
        return 1
    elif n >= 0.8:
        return 0
    else:
        return (0.8 - n) / (0.8 - 0.3)

# Nilai pendapatan
def nilaiPenghasilan(n):
    Tinggi = penghasilanTinggi(n)
    PengRata = penghasilanRata(n)
    BawahRata = penghasilanBawahRata(n)
    Rendah = penghasilanRendah(n)
    return Tinggi, PengRata, BawahRata, Rendah

# Aturan Inference
def inferenceModel(Rendah, Bawah, Rata, Tinggi, S, N, B):
    aturan = [[min(Rendah, S), 'Mungkin'], [min(Bawah, S), 'Mungkin'], [min(Rata, S), 'Tidak'], [min(Tinggi, S), 'Tidak'], [min(Rendah, N), 'Ya'], [min(Bawah, N), 'Mungkin'],
        [min(Rata, N), 'Mungkin'], [min(Tinggi, N), 'Tidak'], [min(Rendah, B), 'Ya'], [min(Bawah, B), 'Ya'], [min(Rata, B), 'Mungkin'], [min(Tinggi, B), 'Mungkin']]
    
    # inisialisasi data array kosong untuk menampung setiap kemungkinan 
    mungkin = [] 
    tidak = [] 
    ya = [] 

    # iterasi setiap aturan kemudian masukan datanya ke array yg sesuai dengan nilai yg didapat
    for i in range(len(aturan)):
        if aturan[i][1] == 'Mungkin':
            mungkin.append(aturan[i][0])
        elif aturan[i][1] == 'Tidak':
            tidak.append(aturan[i][0])
        elif aturan[i][1] == 'Ya':
            ya.append(aturan[i][0])
    return max(ya), max(mungkin), max(tidak)

# Aturan Defuzifikasi
def defuzifikasi(ya, tidak, mungkin):     
    return ((ya * 87) + (mungkin * 70) + (tidak * 52)) / (ya + mungkin + tidak)

# Inisialisasi array untuk penghasilan, hutang, skorBanruan dan skorAkhir
penghasilan = []                                               
hutang = []                                                   
skorBantuan = []                                             
skorAkhir = []                                            

# Baca file csv dari DataTugas2.csv
with open('DataTugas2.csv', mode='r') as csv_input:  
    dataBantuan = csv.reader(csv_input)
    next(dataBantuan)                               
    for row in dataBantuan:
        penghasilan.append(float(row[1]))  # masukan data kolom ke 2 ke array penghasilan                     
        hutang.append(float(row[2])) # masukan data kolom ke 3 ke array hutang                          

# iterasi data untuk setiap orang
for i in range(len(penghasilan)):                     
    Rendah, Bawah, Rata, Tinggi = nilaiPenghasilan(penghasilan[i]) # kalkulasi kategori penhasilan
    S, N, B = nilaiHutang(hutang[i])  # kalkulasi kategori nilai hutang
    ya, mungkin, tidak = inferenceModel(Rendah, Bawah, Rata, Tinggi, S, N, B)    
    nilai = defuzifikasi(ya, tidak, mungkin)                
    skorBantuan.append([nilai, (i + 1)])  # masukan data hasil akhir ke array skorBantuan                
skorBantuan.sort(reverse=True)                   

# iterasi hanya 20 data yg valid saja
for i in range(0, 20):
     # Masukan data yang valid ke array skorAkir 
    skorAkhir.append(skorBantuan[i][1]) 

 # hasil akhir dimasukan ke dalam file .csv
with open('TebakanTugas2.csv', mode="w") as csv_output:    
    bantuanAkhir = csv.writer(csv_output, lineterminator='\n')
    # iterasi data yg valid dari array skorAkhir
    for data in skorAkhir: 
        bantuanAkhir.writerow([data])  # masukan data yg valid ke file csv

print("======= File TebakanTugas2.csv Berhasil di Generate =======")
print(skorAkhir)