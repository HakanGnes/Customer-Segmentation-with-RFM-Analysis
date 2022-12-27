####################
# RFM Analizi İle Müşteri Segmentayonu
####################

# İş Problemi

# İngiltere merkezli perakende şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istemektedir.
# Ortak davranışlar sergileyen müşteri segmentleri özelinde pazarlama çalışmaları yapmanın gelir artışı sağlayacağını düşünmektedir.
# Segmentlere ayırmak için RFM analizi kullanılacaktır.

# Veri Seti Hikayesi

# Online Retail II isimli veri seti İngiltere merkezli bir perakende şirketinin 01/12/2009 - 09/12/2011 tarihleri
# arasındaki online satış işlemlerini içeriyor. Şirketin ürün kataloğunda hediyelik eşyalar yer almaktadır ve çoğu
# müşterisinin toptancı olduğu bilgisi mevcuttur.

# Degiskenler

#InvoiceNo = Fatura Numarası ( Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder )
# StockCode = Ürün kodu ( Her bir ürün için eşsiz )
# Description = Ürün ismi
# Quantity = Ürün adedi  ( Faturalardaki ürünlerden kaçar tane satıldığı)
# InvoiceDate = Fatura tarihi
# UnitPrice = Fatura fiyatı ( Sterlin )
# CustomerID = Eşsiz müşteri numarası
# Country = Ülke ismi

######################################
# Görev 1: Veriyi Anlama ve Hazırlama
######################################

# Adım 1: Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz.

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width',500)

df_ = pd.read_excel("crmAnalytics/datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()

# Adım 2: Veri setinin betimsel istatistiklerini inceleyiniz.

df.describe().T
df.head()
df.shape

# Adım 3: Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?

df.info()
df.isnull().sum()

# Adım 4: Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.

df.dropna(inplace=True)
df.shape

# Adım 5: Eşsiz ürün sayısı kaçtır?

df.nunique()

# Adım 6: Hangi üründen kaçar tane vardır?
df["Description"].nunique()
df["Description"].value_counts().head()

# Adım 7: En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız

df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity",ascending=False).head()

#Adım 8: Faturalardaki ‘C’ iptal edilen işlemleri göstermektedir. İptal edilen işlemleri veri setinden çıkartınız.

df[df["Invoice"].str.contains("C", na=False)].head()
df = df[~df["Invoice"].str.contains("C", na=False)]

# Adım 9: Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz

df["Total_Price"] = df["Price"] * df["Quantity"]
df.groupby("Invoice").agg({"Total_Price": "sum"}).head()

###############################################################
# Görev 2: RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
###############################################################

# Adım 1: Recency, Frequency ve Monetary tanımlarını yapınız.

# Recency : today_Date - Invoice.date.max()
# Frequency : Invoice.nunique()
# Monetary : Total_Price.sum()

today_date = dt.datetime(2011, 12, 11)
type(today_date)

rfm.columns = ['recency', 'frequency', 'monetary']

rfm.describe().T

rfm = rfm[rfm["monetary"] > 0]
rfm.shape

# Adım 2: Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile hesaplayınız.
rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice: Invoice.nunique(),
                                     'Total_Price': lambda Total_Price: Total_Price.sum()})
rfm.head()

Adım 3: Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.

rfm.columns = ['recency', 'frequency', 'monetary']

rfm.describe().T

# Adım 4: rfm dataframe’ini oluşturduktan sonra veri setini "monetary>0" olacak şekilde filtreleyiniz.

rfm = rfm[rfm["monetary"] > 0]
rfm.shape
rfm.describe().T


################################################
# Görev 3: RFM Skorlarının Oluşturulması ve Tek bir Değişkene Çevrilmesi
################################################

# Adım 1: Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
    # Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])

rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm.head()
# Adım 2: recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz.

rfm["RFM_SCORE"]= (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))

rfm.head()

rfm.describe().T

rfm[rfm["RFM_SCORE"] == "55"].head()

rfm[rfm["RFM_SCORE"] == "11"].head()

#################################################
# Görev 4: RF Skorunun Segment Olarak Tanımlanması
#################################################

# Adım 1: Oluşturulan RF skorları için segment tanımlamaları yapınız.
    # Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.

# RFM isimlendirmesi
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm.head()

# Segment Yorumları

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])


rfm[rfm["segment"] == "cant_loose"].head()
rfm[rfm["segment"] == "cant_loose"].index

rfm[rfm["segment"] == "champions"].head()
rfm[rfm["segment"] == "champions"].index

rfm[rfm["segment"] == "hibernating"].head()
rfm[rfm["segment"] == "hibernating"].index




