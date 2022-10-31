# Install dash: pip install dash
# Install bootstrap: import dash_bootstrap_components as dbc
# visit http://127.0.0.1:8050/ in your web browser.

# BẤM CTRL '+' C ĐỂ TẮT APP ĐANG CHẠY
# import pathlib #Not Remove

import dash_bootstrap_components as dbc
import firebase_admin
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from firebase_admin import credentials, firestore
import numpy as np

# PATH = pathlib.Path(__file__).parent #Not Remove
# DATA_PATH = PATH.joinpath("data").resolve() #Not Remove

# TẢI DỮ LIỆU TỪ FIRESTORE

cred = credentials.Certificate("Private key from Firebase Admin SDK")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'collection').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)
df = df.sort_values(by=['YEAR_ID'])
df["YEAR_ID"] = df["YEAR_ID"].astype("str")

df["QTR_ID"] = df["QTR_ID"].astype("str")
df["TOTALPRICE"] = df["QUANTITYORDERED"]*df["PRICEEACH"]
df["LOINHUAN"] = df["SALES"] - df["TOTALPRICE"]
tong = df[(df['YEAR_ID'] == '2003')]['LOINHUAN'].sum()
tongDS = df["SALES"].sum()


tongLN = df["LOINHUAN"].sum()


year = ['2003', '2004', '2005']
lN_2003 = df[(df['YEAR_ID'] == '2003')]['LOINHUAN'].sum()
lN_2004 = df[(df['YEAR_ID'] == '2004')]['LOINHUAN'].sum()
lN_2005 = df[(df['YEAR_ID'] == '2005')]['LOINHUAN'].sum()
profit = [lN_2003, lN_2004, lN_2005]
topLN = max(profit)


dS_2003 = df[(df['YEAR_ID'] == '2003')]['SALES'].sum()
dS_2004 = df[(df['YEAR_ID'] == '2004')]['SALES'].sum()
dS_2005 = df[(df['YEAR_ID'] == '2005')]['SALES'].sum()
doanhSo = [dS_2003, dS_2004, dS_2005]
topDS = max(doanhSo)

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server #Not Remove
app.title = "Finance Data Analysis"

figDoanhSo = px.histogram(df, x="YEAR_ID", y="SALES", 
barmode="group", color="YEAR_ID", title='Tổng doanh số bán hàng theo năm', histfunc = "sum",
labels={'YEAR_ID':'Từ năm 2003, 2004 và 2005', 'Sum':'Tổng doanh số'})



figDoanhSoTheoDanhMuc = px.sunburst(data_frame=df, path=['YEAR_ID','CATEGORY'], values='SALES',
color='SALES',
labels={'parent':'Năm', 'labels':'Danh mục','SALES':'Doanh số sản phẩm'},
title='Tỉ lệ doanh số đóng góp theo danh mục hằng năm')

figLoiNhuan = px.line(data_frame=df, x=year, y=profit, title='Lợi nhuận bán hàng theo năm')

figLoiNhuanTheoDanhMuc = px.sunburst(data_frame=df, path=['YEAR_ID','CATEGORY'], values='LOINHUAN',
color='LOINHUAN',
labels={'parent':'Năm', 'labels':'Danh mục','LOINHUAN':'Lợi nhuận sản phẩm'},
title='Tỉ lệ lợi nhuận đóng góp theo danh mục hằng năm')


app.layout = dbc.Container(
    html.Div(
    children=[
        html.Div(
            children=[
                html.H3(
                    children=["XÂY DỰNG DANH MỤC SẢN PHẨM TIỀM NĂNG"], className="header-title02 text-center",
                )
            ],
            className="row",
        ),
        html.Div(
            children=[
                html.H3(
                    children=["TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP TP.HCM - DHHTTT15A - 19439671 - ĐẶNG NGỌC PHONG"], className="header-title01 text-center pt-0",
                )
            ],
            className="row",
        ),
        html.Div(
        children=[
                html.Div(
                    children=["DOANH SỐ BÁN HÀNG",
                    html.P(
                        children=[tongDS],
                        className="value"
                    )
                    ],
                    className="view col-3 text-center"
                ),
                html.Div(
                    children=["DOANH SỐ BÁN HÀNG",
                    html.P(
                        children=[tongLN],
                        className="value"
                    )
                    ],
                    className="view col-3 text-center"
                ),
                html.Div(
                    children=["DOANH SỐ BÁN HÀNG",
                    html.P(
                        children=[topDS],
                        className="value"
                    )
                    ],
                    className="view col-3 text-center"
                ),
                html.Div(
                    children=["DOANH SỐ BÁN HÀNG",
                    html.P(
                        children=[topLN],
                        className="value"
                    )
                    ],
                    className="view col-3 text-center"
                )],
            className="row p-2" 
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                    id='doanhSo-graph',
                    figure=figDoanhSo), #TỈ LỆ ĐÓNG GÓP CỦA DOANH SỐ THEO TỪNG DANH MỤC TRONG TỪNG NĂM (SUNBURST)
                    className="view02 col-md-6 col-sm-12"
                    # className="view02 col-6"
                ),html.Div(
                    children=dcc.Graph(
                    id='doanhSoTheoDanhMuc-Graph',
                    figure=figDoanhSoTheoDanhMuc), #TỈ LỆ ĐÓNG GÓP CỦA DOANH SỐ THEO TỪNG DANH MỤC TRONG TỪNG NĂM (SUNBURST)
                    className="view02 col-md-6 col-sm-12"
                    # className="view02 col-6"
                )
            ],
            className="row p-2"
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                    id='loiNhuan-Graph',
                    figure=figLoiNhuan,
                    ),#LỢI NHUẬN THEO TỪNG NĂM (LINE)
                 className="view02 col-md-6 col-sm-12"
                # className="view02 col-6"
                ),html.Div(
                    children=dcc.Graph(
                    id='loiNhuanTheoNam-graph',
                    figure=figLoiNhuanTheoDanhMuc,
                    ), #TỈ LỆ ĐÓNG GÓP CỦA LỢI NHUẬN THEO TỪNG DANH MỤC TRONG TỪNG NĂM (SUNBURST)
                    className="view02 col-md-6 col-sm-12"
                    # className="view02 col-6"
                )
            ],
            className="row p-2"
        ),
    ]), className="full"
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8090)