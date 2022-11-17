import streamlit as st
from src.scrap import scrap
from src.preprocess_text import clean_text
from src.make_wordcloud import make_wordcloud
from src.forecast_pendapatan import forecast_pendapatan
from src.sentiment_analysis import predict_sentiment

st.title("BCC BASUDARA")
# st.text("Deskripsi blabalbla")
# st.markdown("### Cara pemakaian web")
# st.text("""
# 1. Masukkan URL google review tempat wisata yang diinginkan
# 2. Klik tombol proses
# 3. Baca hasil visualisasi dan ringkasan untuk evaluasi demi meningkatkan mutu
# """)

st.subheader("Forecast Pendapatan Rata-Rata di Jawa Barat")
kota_pilihan = st.selectbox("Pilih Kabupaten/Kota",
                            ('KABUPATEN BOGOR',
                             'KABUPATEN SUKABUMI',
                             'KABUPATEN CIANJUR',
                             'KABUPATEN BANDUNG',
                             'KABUPATEN GARUT',
                             'KABUPATEN TASIKMALAYA',
                             'KABUPATEN CIAMIS',
                             'KABUPATEN KUNINGAN',
                             'KABUPATEN CIREBON',
                             'KABUPATEN MAJALENGKA',
                             'KABUPATEN SUMEDANG',
                             'KABUPATEN INDRAMAYU',
                             'KABUPATEN SUBANG',
                             'KABUPATEN PURWAKARTA',
                             'KABUPATEN KARAWANG',
                             'KABUPATEN BEKASI',
                             'KABUPATEN BANDUNG BARAT',
                             'KOTA BOGOR',
                             'KOTA SUKABUMI',
                             'KOTA BANDUNG',
                             'KOTA CIREBON',
                             'KOTA BEKASI',
                             'KOTA DEPOK',
                             'KOTA CIMAHI',
                             'KOTA TASIKMALAYA',
                             'KOTA BANJAR',
                             'KABUPATEN PANGANDARAN'))
forecast_button = st.button("Forecast Pendapatan")
if forecast_button:
    with st.spinner("Forecasting.."):
        hiburan, rm, hotel = forecast_pendapatan(kota_pilihan)
        st.markdown("##### Pendapatan Hiburan")
        st.line_chart(hiburan, x="tahun", y="pendapatan")
        st.markdown("##### Pendapatan Rumah Makan")
        st.line_chart(rm, x="tahun", y="pendapatan")
        st.markdown("##### Pendapatan Hotel")
        st.line_chart(hotel, x="tahun", y="pendapatan")

st.markdown("---")
st.subheader("Scraper dan Sentiment Analysis")
url = st.text_input("Masukkan URL")
jumlah_scroll = st.number_input(
    "Masukkan jumlah scroll (semakin banyak jumlah scroll, semakin banyak pula data yang didapat)", min_value=1, max_value=200, value=5)
clean_button = st.checkbox("Bersihkan Data")
sentiment_analysis_button = st.checkbox("Sentiment Analysis")
button = st.button("Proses")
hasil_data, hasil_user, hasil_ai, download = st.tabs(
    ["Sample Data", "Hasil User", "Hasil Analisis Sentimen", "Download"])

if button:
    with st.spinner("Scrapping data.."):
        data = scrap(url, "./chromedriver.exe", jumlah_scroll)
    if clean_button:
        with st.spinner("Membersihkan data.."):
            data = clean_text(data)

with hasil_data:
    if not button:
        st.text("masukkan URL terlebih dahulu!")
    else:
        st.table(data.head(10))

with hasil_user:
    if not button:
        st.text("masukkan URL terlebih dahulu!")
    else:
        st.markdown("**Hasil Review Dari User**")
        st.text("Jumlah bintang dari user")
        st.bar_chart(data["bintang"].value_counts())

        bintangs = list(data["bintang"].value_counts().index)
        bintangs.sort(reverse=True)
        for bintang in bintangs:
            texts = " ".join(data[data["bintang"] == bintang]["komentar"])
            if texts.strip() != "":
                st.markdown(f"**Bintang {bintang}**")
                st.pyplot(make_wordcloud(texts))
            else:
                st.markdown(f"**Bintang {bintang}**")
                st.text("Tidak ada komentar")

with hasil_ai:
    if not button:
        st.text("masukkan URL terlebih dahulu!")
    elif sentiment_analysis_button:
        st.markdown("**Hasil Review Dari User Menggunakan analisis sentimen**")
        with st.spinner("Analisis sentimen.."):
            data_ai = predict_sentiment(data, "komentar")
        data_ai = data_ai.dropna()
        st.text("Jumlah bintang dari hasil sentiment analysis")
        st.bar_chart(data_ai["komentar_sentiment"].value_counts())

        different = data_ai[data_ai["komentar_sentiment"]
                            != data_ai["bintang"]]
        st.markdown(
            f"**Jumlah komentar yang berbeda dengan bintang: {len(different)}**")
        st.table(different.dropna().head(10))

        bintangs = list(data_ai["komentar_sentiment"].value_counts().index)
        bintangs.sort(reverse=True)
        for bintang in bintangs:
            texts = " ".join(
                data_ai[data_ai["komentar_sentiment"] == bintang]["komentar"])
            if texts.strip() != "":
                st.markdown(f"**Bintang {bintang}**")
                st.pyplot(make_wordcloud(texts))
            else:
                st.markdown(f"**Bintang {bintang}**")
                st.text("Tidak ada komentar")
    else:
        st.text("Centang Sentiment Analysis terlebih dahulu!")


# with trend_sekitar:
#     if not button:
#         st.text("masukkan URL terlebih dahulu!")
#     else:
#         st.markdown("**Trend Pariwisata di Jawa Barat**")
#         st.text("Tableaunya mas ravie")

with download:
    if not button:
        st.text("masukkan URL terlebih dahulu!")
    else:
        # st.markdown("**Ringkasan**")
        st.download_button(
            label="Download data as CSV",
            data=data.to_csv(index=False).encode("utf-8"),
            file_name='data_pariwisata.csv',
            mime='text/csv',
        )


st.markdown("----")
st.markdown("#### Penjelasan tiap tab")
st.markdown("""
1. tab `sample data` adalah 10 data teratas dari hasil scraping
1. tab `hasil user` adalah hasil analisis dari bintang/rating yang diberikan oleh user
2. tab `hasil analisis sentimen` adalah hasil analisis dari bintang/rating yang diperoleh dari analisis sentimen. Berfungsi sebagai pembanding
4. tab `download` adalah adalah tempat untuk mengunduh data hasil scraping
""")

st.markdown("#### FAQ")
st.markdown("""
**Q1**: Bagaimana cara mendapatkan link google review? \\
**A1**: Panduan bisa cek [di sini](https://docs.google.com/document/d/1wdX40kgx7M0cJXkMH46_CHfeNBEL4eYkG1Y_l6qi7jo/edit?usp=sharing)
""")
