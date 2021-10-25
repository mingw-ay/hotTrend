import requests

headers = {
    'cookie':
    'tt_webid=7009637787465680415; ttcid=00bc2fa788004311b7da7442686d524226; csrftoken=c59b6047f660e65a1f661a7bd19a498a; MONITOR_WEB_ID=7009637787465680415; _tea_utm_cache_2018=undefined; MONITOR_DEVICE_ID=17fb5952-8c0d-45d0-8936-ace6b7a53bed; _S_WIN_WH=1280_648; _S_DPR=1.5; _S_IPAD=0; passport_csrf_token=01d3ce90f6f6ffe1550a2b5abb15034f; s_v_web_id=verify_kv63qbuq_JzRCrAcM_FTpd_42Yl_9jcj_BRFlDHYaea86; __ac_nonce=061762cf6000dca8074ac; __ac_signature=_02B4Z6wo00f01oWWS2AAAIDCBZSxIxFJFiaFsk.AAMAfHhs2fgLFxacCOLX7tffxD7FAlb6qId0SRodY9nT1uZHODuGAQhwCQdpseE-ok8mJCTwW7Om4Xz5tk6oySIBTaErOnZojycIIZMot81; ttwid=1|vDphOqId7_obutMpiY7XCvxRu6UY7ufKW5OwLC1xWZg|1635134713|fb61471947e4dff74d87acf5b652ba9cae4d7551c84d88c0996a869dc44a26b9; tt_scid=mIG4baDm93s5dZ1itp.04tZSNkcWvdibnCewqF2KbzVQLfrQNNYdWRgx3kKRnbTF41c3',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

url = 'https://www.toutiao.com/api/pc/list/feed?channel_id=0&max_behot_time=1635132703&category=pc_profile_recommend&_signature=_02B4Z6wo00101J6z2OgAAIDAHrEiqzjbVMSel9xAAEbffhnTrlaiMc3pAczIPwgyTRU1Nm7bWpUtGg9EzC-eMorr8lQtSduIq5zs3Q3l0ThrzxSiQPaq0vMv8.JD3amYoPukmpgk6sr44vTF32'
feeds = requests.get(url, headers=headers).json()['data']
print(feeds[2]['title'])
