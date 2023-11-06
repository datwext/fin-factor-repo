import random

from requests import get
from base64 import b64decode
from zipfile import ZipFile
import os
import time

headers_lk = {
    "accept": "*/*",
    "accept-language": "ru,en;q=0.9",
    "content-type": "application/json",
    "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"YaBrowser\";v=\"23\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "cookie": "_ga=GA1.2.2094377184.1665555168; ___wbu=4ac1a508-a4ea-409e-942f-e41a13b818e2.1665555171; _ym_uid=16681664101029377433; _ym_d=1668166410; external-locale=ru; WILDAUTHNEW_V3=DAFD4B27B2CE683ABAFC4C26BBB3F6BB7FDD1E2B4A4B5E97783ACE910A55F735458AD9B7C59A8EEBB5D305F2287E8BBFB2C527650BDBE935C77DC611CD48A95859BA6A97C30F92235298CA55649BD70400FA75E542DB6FED3B4CB523BBC8174424E5C283163C68FCBBDC4114EC58241E57CB450390E0AFFAE58E173D874D8B6563549BA85881AC260D58ADD30BA48A118ABD663D859CB344260404B1B4D6409FE1E5A4A1DA6764136BA242FDC7DD6B1418B2A3271F6690ED1D3903CEA8EC8B5945C55BFDB553A94891BA8A087C0D930181A3EF292C08D8F35C8153A6101931F2ECB7FC84F7D03D3AFA8F4C6EB19919465E7F68DA077C5938F3C345FBEA9F9FADE806D3DA95C8E7F606124D53E92A72CAAB012771908A790D57F45401FA5FF6CE072FEECF01175B061FF2771EBBF9E76A2CD294FF; _wbauid=3925505621697093997; wbx-validation-key=82639c45-a1e8-48de-b2be-89b6ebbf8e07; WBToken=Ap2viByCwKDUDILox9YMVI_9VR97cYVAfprBlS806JD9IFumpUQl7T1TjYig2G_8Z9FYonhZDA3X1NDvd-EBsKqE1O3YZNgNa7k59Wp5iwSgbXsXFn2b840O9Fvql7o2LIChWA; x-supplier-id-external=1f887b2d-305d-5025-bc81-caab0465bb07",
    "Referer": "https://seller.wildberries.ru/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}


def get_list_weekly_reports():
    link = "https://seller-weekly-report.wildberries.ru/ns/realization-reports/suppliers-portal-analytics/api/v1/reports?dateFrom=&dateTo=&limit=500&searchBy=&skip=0&type=2"
    response = get(link, headers=headers_lk)
    reports_body = response.json()["data"]["reports"]
    reports_id = []
    for body in reports_body:
        reports_id.append(str(body["id"]))
    return reports_id


def get_b64_zip(reports_id):
    count1 = 0
    count2 = 0
    for id_r in reports_id:
        goNext = False
        while not goNext:
            goNext = True
            link = "https://seller-weekly-report.wildberries.ru/ns/realization-reports/suppliers-portal-analytics/api/v1/reports/" + id_r + "/details/archived-excel"
            try:
                time.sleep(random.uniform(0, 0.6))
                response = get(link, headers=headers_lk)
                print(response.json()["data"]["file"])
                file = open(id_r + '.zip', 'wb')
                file.write(b64decode(response.json()["data"]["file"], validate=True))
                file.close()
                with ZipFile(id_r + '.zip', 'r') as myzip:
                    myzip.extract('0.xlsx')
                os.remove(id_r + '.zip')
                os.rename('0.xlsx', id_r + '.xlsx')
                count1 += 1
            except Exception as e:
                print(e, id_r)
                count2 += 1
                goNext = False
                time.sleep(15.02)

    print(count1, count2)


def main():
    get_b64_zip(
        get_list_weekly_reports()
    )


if __name__ == '__main__':
    main()
