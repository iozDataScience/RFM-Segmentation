###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

###############################################################
# 1. İş Problemi (Business Problem)
###############################################################

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.
# An e-commerce company wants to segment its customers and determine marketing strategies according to these segments.

# Değişkenler (Variables)

# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem. (Invoice number. The unique number of each transaction, namely the invoice. Aborted operation if it starts with C.)
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara. (Product code. Unique number for each product.)
# Description: Ürün ismi (Product name)
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir. (Number of products. It expresses how many of the products on the invoices have been sold.)
# InvoiceDate: Fatura tarihi ve zamanı. (Invoice date and time.)
# UnitPrice: Ürün fiyatı (Sterlin cinsinden) (Product price (in GBP))
# CustomerID: Eşsiz müşteri numarası (Unique customer number)
# Country: Ülke ismi. Müşterinin yaşadığı ülke. (Country name. Country where the customer lives.)

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# Görev1 Veriyi Anlama ve Hazırlama (Task1 Understanding and Preparing Data)
# 1. Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz. (Read the 2010-2011 data in the Online Retail II excel. Make a copy of the dataframe you created.)

# 2010-2011 yılı içerisindeki veriler (Data in 2010-2011)
df_ = pd.read_excel("dersler/hafta_3/online_retail_II.xlsx",
                    sheet_name="Year 2010-2011")

df = df_.copy()

# 2. Veri setinin betimsel istatistiklerini inceleyiniz. (Examine the descriptive statistics of the data set.)

df.describe().T
df.shape

# 3. Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır? (Are there any missing observations in the dataset? If yes, how many missing observations in each variable?)

df.isnull().sum()

# 4. Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız. (Remove the missing observations from the data set. Use the 'inplace=True' parameter for subtraction.)

df.dropna(inplace=True)

# 5. Eşsiz ürün sayısı kaçtır? (How many unique products?)

df["StockCode"].nunique()

# 6. Hangi üründen kaçar tane vardır? (How many of each product are there?)

df["StockCode"].value_counts()

# 7. En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız. (Rank the 5 most ordered products from most to least.)

df.groupby("StockCode").agg({"Quantity": "sum"}).reset_index().sort_values("Quantity", ascending=False).head()

# 8. Faturalardaki ‘C’ iptal edilen işlemleri göstermektedir. İptal edilen işlemleri veri setinden çıkartınız. (The 'C' in the invoices shows the canceled transactions. Remove the canceled transactions from the dataset.)

df = df[~df["Invoice"].str.contains("C", na=False)]

# 9. Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz. (Create a variable named 'TotalPrice' that represents the total earnings per invoice.)

df["TotalPrice"] = df["Quantity"] * df["Price"]

# Görev 2: RFM metriklerinin hesaplanması (Calculating RFM metrics)

# Recency, Frequency ve Monetary tanımlarını yapınız. (Make the definitions of Recency, Frequency and Monetary.)
# Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile hesaplayınız. (Calculate customer specific Recency, Frequency and Monetary metrics with groupby, agg and lambda.)
# Hesapladığınız metrikleri rfmisimli bir değişkene atayınız. (Assign your calculated metrics to a variable named rfm.)
# Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz. (Change the names of the metrics you created to recency, frequency and monetary.)

# Not 1: recency değeri için bugünün tarihini (2011, 12, 11) olarak kabul ediniz. (For the recency value, accept today's date as (2011, 12, 11).)
# Not 2: rfm dataframe’ini oluşturduktan sonra veri setini "monetary>0" olacak şekilde filtreleyiniz. (After creating the rfm dataframe, filter the dataset to "monetary>0".)

# Recency (yenilik): Müşterinin son satın almasından bugüne kadar geçen süre (Time from customer's last purchase to date)
# Frequency (Sıklık): Toplam satın alma sayısı. (Total number of transactions.)
# Monetary (Parasal Değer): Müşterinin yaptığı toplam harcama. (Total spend by the customer.)

today_date = dt.datetime(2011, 12, 11)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                     'Invoice': lambda num: num.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.columns = ['recency', 'frequency', 'monetary']

rfm = rfm[rfm["monetary"] > 0]

rfm.reset_index()

# Görev 3: RFM skorlarının oluşturulması ve tek bir değişkene çevrilmesi (Generating and converting RFM scores to a single variable)

# Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz. (Convert Recency, Frequency and Monetary metrics to scores between 1-5 with the help of qcut.)
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz. (Record these scores as recency_score, frequency_score and monetary_score.)
# Oluşan 3 farklı değişkenin değerini tek bir değişken olarak ifade ediniz ve RFM_SCORE olarak kaydediniz. (Express the value of 3 different variables as a single variable and save it as RFM_SCORE.)

# Örneğin; (For example;)
# Ayrı ayrı değişkenlerde sırasıyla 5, 2, 1 olan recency_score, frequency_score ve monetary_score skorlarını RFM_SCORE değişkeni isimlendirmesi ile 521 olarak oluşturunuz.
# (Create the recency_score, frequency_score and monetary_score scores of 5, 2, 1, respectively, in separate variables, as 521 with the naming of the RFM_SCORE variable.)


# Recency
# En son tarih skoru. Burada 1 en yakın, 5 en uzak tarih olmaktadır. (Latest date score. Here 1 is the closest date and 5 is the farthest date.)
# Bizim için en önemli durum en yakın tarih olduğu için 1, 5'ten daha yüksek öneme sahiptir. (For us, the most important case is the most recent date, so 1 is more important than 5.)

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

# Alışveriş sıklığı skoru. Burada 1 en az sıklığı, 5 en fazla sıklığı temsil eder. (Shopping frequency score. Here 1 represents the least frequency, 5 the most frequent.)
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

# Bize bıraktığı para tutarı. Burada 1 en az parayı, 5 en fazla parayı temsil eder. (The amount of money customer left us. Here 1 represents the least amount of money and 5 represents the most money.)
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.describe().T

# Görev 4: RFM skorlarının segment olarak tanımlanması (Task 4: Defining RFM scores as segments)
# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlamaları yapınız. (Make segment definitions so that the generated RFM scores can be explained more clearly.)
# Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz. (Convert the scores into segments with the help of the seg_map below.)

# RFM isimlendirmesi (RFM nomenclature)
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

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)  # birleştirilen skorlar seg_map ile değiştirildi
rfm.head()

# Görev 5: Aksiyon zamanı! (Task 5: Time for action!)

# Önemli bulduğunuz 3 segmenti seçiniz. Bu üç segmenti; (Select the 3 segments you find important.)
    # Hem aksiyon kararları açısından, (Both in terms of action decisions,)
    # Hem de segmentlerin yapısı açısından (ortalama RFM değerleri) yorumlayınız. (Also interpret in terms of the structure of the segments (mean RFM values).)
# "Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız. (Select the customer IDs of the "Loyal Customers" class and get the excel output.)

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# segment1 "champions" segmentindeki müşterilerin frequency ortalaması 12.42 ile en yüksek ortalamaya sahiptir. (Customers in "champions" segment have the highest frequency average of 12.42.)
# segment2 "cant_loose" segmentindeki müşterilerin frequency ortalaması 8.38 ile en yüksek 2. ortalamaya sahiptir. (Customers in "cant_loose" segment have the 2nd highest frequency average with 8.38.)
# segment3 "loyal_customers" segmentindeki müşterilerin frequency ortalaması 6.48 ile en yüksek 2. ortalamaya sahiptir. (Customers in "loyal_customers" segment have the 2nd highest frequency average with 6.48.)
# bu 3 segmente dahil olan müşteriler için stratejiler belirlenmelidir. örneğin bu segment müşterilere son alışverişlerindeki ürünlerin yanında alabilecekleri ürünler önerilen mailler atılabilir. En son aldıkları ürünlerden bazıları için indirim maili atılabilir kupon tanımlanabilir.
# Strategies should be determined for customers included in these 3 segments. For example, customers in this segment can be sent e-mails suggesting products they can buy alongside the products they have purchased. Discount e-mail coupons can be defined for some of the most recent products.

new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "loyal_customers"].index
new_df.head()

new_df.to_excel("dersler/hafta_3/loyal_customers.xlsx", index_label="SıraNo")  # df'i kaydet (save df)
