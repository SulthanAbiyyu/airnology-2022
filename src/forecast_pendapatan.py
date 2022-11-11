import logging
import pandas as pd
from prophet import Prophet

logging.basicConfig(level=logging.INFO)


def forecast_pendapatan(KOTA: str):

    logging.info("loading data..")
    data_specialize = pd.read_csv(
        "./data/od_15380_jml_pendapatan_asli_drh_bidang_pariwisata__sektor_wisa/data.jabarprov.go.id/disparbud-od_15380_jml_pendapatan_asli_drh_bidang_pariwisata__sektor_wisa_data.csv")
    data_specialize = data_specialize[data_specialize["nama_kabupaten_kota"] == KOTA]

    logging.info("preparing data..")
    hotel_pendapatan = pd.DataFrame()
    hotel_pendapatan["tahun"] = data_specialize["tahun"].unique()
    hotel_pendapatan["jumlah_pendapatan"] = data_specialize[data_specialize["sektor_wisata"]
                                                            == "HOTEL"].reset_index()["jumlah_pendapatan"]
    hotel_pendapatan = hotel_pendapatan.reset_index().rename(
        columns={"tahun": "ds", "jumlah_pendapatan": "y"}).drop(columns="index")

    rm_pendapatan = pd.DataFrame()
    rm_pendapatan["tahun"] = data_specialize["tahun"].unique()
    rm_pendapatan["jumlah_pendapatan"] = data_specialize[data_specialize["sektor_wisata"]
                                                         == "RESTORAN/RUMAH MAKAN"].reset_index()["jumlah_pendapatan"]
    rm_pendapatan = rm_pendapatan.reset_index().rename(
        columns={"tahun": "ds", "jumlah_pendapatan": "y"}).drop(columns="index")

    hiburan_pendapatan = pd.DataFrame()
    hiburan_pendapatan["tahun"] = data_specialize["tahun"].unique()
    hiburan_pendapatan["jumlah_pendapatan"] = data_specialize[data_specialize["sektor_wisata"]
                                                              == "HIBURAN"].reset_index()["jumlah_pendapatan"]
    hiburan_pendapatan = hiburan_pendapatan.reset_index().rename(
        columns={"tahun": "ds", "jumlah_pendapatan": "y"}).drop(columns="index")

    # Training
    logging.info("training model..")
    hiburan_model = Prophet(seasonality_mode='multiplicative')
    hiburan_model.fit(hiburan_pendapatan)

    hotel_model = Prophet(seasonality_mode='multiplicative')
    hotel_model.fit(hotel_pendapatan)

    rm_model = Prophet(seasonality_mode='multiplicative')
    rm_model.fit(rm_pendapatan)

    # Forecasting
    logging.info("forecasting..")
    hiburan_future = pd.DataFrame({
        "ds": [max(hiburan_pendapatan["ds"]) + i for i in range(1, 6)]
    })
    hiburan_future["y"] = hiburan_model.predict(hiburan_future)["yhat"]
    hiburan_gabung = pd.concat([hiburan_pendapatan, hiburan_future])
    hiburan_gabung = hiburan_gabung.rename(
        columns={"ds": "tahun", "y": "pendapatan"})

    hotel_future = pd.DataFrame({
        "ds": [max(hotel_pendapatan["ds"]) + i for i in range(1, 6)]
    })
    hotel_future["y"] = hotel_model.predict(hotel_future)["yhat"]
    hotel_gabung = pd.concat([hotel_pendapatan, hotel_future])
    hotel_gabung = hotel_gabung.rename(
        columns={"ds": "tahun", "y": "pendapatan"})

    rm_future = pd.DataFrame({
        "ds": [max(rm_pendapatan["ds"]) + i for i in range(1, 6)]
    })
    rm_future["y"] = rm_model.predict(rm_future)["yhat"]
    rm_gabung = pd.concat([rm_pendapatan, rm_future])
    rm_gabung = rm_gabung.rename(columns={"ds": "tahun", "y": "pendapatan"})

    hiburan_gabung["tahun"] = hiburan_gabung["tahun"].astype(str)
    hotel_gabung["tahun"] = hotel_gabung["tahun"].astype(str)
    rm_gabung["tahun"] = rm_gabung["tahun"].astype(str)
    return hiburan_gabung, hotel_gabung, rm_gabung


if __name__ == "__main__":
    print(forecast_pendapatan("KABUPATEN BANDUNG")[0])
