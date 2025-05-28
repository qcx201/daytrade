# %%
import requests
from datetime import datetime

# %%
def get_summary(symbol):

    '''Get company summary from Yahoo Finance.'''

    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}'
    
    params = {
        'modules': 'summaryProfile,financialData,recommendationTrend,earnings,equityPerformance,summaryDetail,defaultKeyStatistics,calendarEvents,esgScores,price,pageViews,financialsTemplate,quoteUnadjustedPerformanceOverview,corporateActions',
        'crumb': 'PzviMJtbqgN'
    }

    headers = {
        'cookie': 'tbla_id=b24e82d1-970b-4fc7-8f92-6c95a3501717-tucte3a8897; OTH=v=2&s=0&d=eyJraWQiOiIwIiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiRTNMVkxKQzUzVFMzTEdWTFRDNEEyRlROTE0iLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJnaHkwY05FY0hOTWkifX0.jce2kAPKkx9BllZedYEWRE9bUVhdQPqYO9gXSG-a9idvQvTwhXvg9kn8ZXONhNCOull7Z7U_2LKpLDnhJ5AmDjUtF_AUn2nal23OinE-JoEnjp5ZckXSqPN6s1uVgsUiQ5AOBU95UXDsX51BmA682XeJMujYDbPO2kLqbHcalN4; OTHD=g=B3EAE7D6E93E5550B1CE3332572E4C5CD23D40997D3B075C53D14CA9D6333721&s=71188DDF7256CAA77C20B36FA354BEE2AE25D6E7D3D4A527F46806D7ACCA5C78&b=bid-clmlelhjju560&j=ca&bd=4717356ddcecdcd95a7d91fa4da4d734&gk=x1a9z-qJCjBBcc&sk=x1a9z-qJCjBBcc&bk=x1a9z-qJCjBBcc&iv=4FFE0808DC664345BF3D2B261864103A&v=1&u=0; F=d=G3A7c.E9vDfnvhmumk4AaRBqwFhZTNO0opAIPOqDAIdMv7V5sf0-; T=af=JnRzPTE3NDM1OTM0MjQmcHM9dUZ4ZEd3NUZFOGF3dlBEQlA1TEVoQS0t&d=bnMBeWFob28BZwFFM0xWTEpDNTNUUzNMR1ZMVEM0QTJGVE5MTQFhYwFBTUphSy5lQgFhbAFxY3guZWNvbkBnbWFpbC5jb20Bc2MBbWJyX3JlZ2lzdHJhdGlvbgFmcwFJdVZ6QVk5bjdSX1EBenoBUS9SN25CQTdFAWEBUUFFAWxhdAFRL1I3bkIBbnUBMA--&kt=EAAcuUvQd4dK5tMAFvPUcCwgA--~I&ku=FAAKJoNoTjFSmumohPcQC2hoHN8.V7It.UZ3bNEz0iWbjEmJFshulMtmg14rTRiv51gIYLCJpfcz82zP.cL_KC71FTD5IZoEyC6RrTDbXcHVfU.aJ_a6R4JUTcnUJLyupjGEcqDNYRGHdQdH1cENA0I9iLIwqbzQlcsx5hlTej3f6U-~E; PH=l=en-CA; Y=v=1&n=6i0c3tlkbrq6k&l=fpd0lcfjkifhe08bdc2xtt3fjhdlf8mvjg35i2e7/o&p=n30vvca00000000&r=1es&intl=ca; axids=gam=y-eWDDnRFG2uL1_t8UrTqFVOe4ahifgsBXl0FPUH8linbU.K6l_w---A&dv360=eS1IaUZTVDBGRTJ1RXA4WXdJcm1fSGdERVQ3ZkRHVEhrSEtKb0d0UUkzazlMZ1BsMUptVE8wT1dVaDdYQWUuSmFmZlZkZX5B&ydsp=y-YIwKMfJE2uJQcWV6VtSuwNZDITyZgpXkLhHQ6GSCPCOd6Vl2bz11p.ibX8679L9ZJ1uH~A&tbla=y-cxoR9UdG2uJ7RFqSPlCDnuXqo46H5IzEzWzILFV_LQPiAHigWg---A; GUC=AQEACAJn7mVoGkIkbQTG&s=AQAAAIIFkmyf&g=Z-0f4Q; A1=d=AQABBMAUP2cCEPOeje_KrxV8JHFGrqyu2soFEgEACAJl7mcaaCXUxyMA_eMDAAcIwBQ_Z6yu2soID97rTSTqyE-LbcnGXPRgYwkBBwoBEg&S=AQAAAj9VrtnxktUyGQwKfo4np0A; A3=d=AQABBMAUP2cCEPOeje_KrxV8JHFGrqyu2soFEgEACAJl7mcaaCXUxyMA_eMDAAcIwBQ_Z6yu2soID97rTSTqyE-LbcnGXPRgYwkBBwoBEg&S=AQAAAj9VrtnxktUyGQwKfo4np0A; cmp=t=1745441860&j=0&u=1---; gpp=DBAA; gpp_sid=-1; PRF=t%3DAAPL%252BBLDP%252BNMAX%252BNVDA%26ft%3DthemeSwitchEducation%26dock-collapsed%3Dtrue%26su-oo%3Dtrue; A1S=d=AQABBMAUP2cCEPOeje_KrxV8JHFGrqyu2soFEgEACAJl7mcaaCXUxyMA_eMDAAcIwBQ_Z6yu2soID97rTSTqyE-LbcnGXPRgYwkBBwoBEg&S=AQAAAj9VrtnxktUyGQwKfo4np0A',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    resp = requests.get(url, headers=headers, params=params)
    return resp.json()

# %%
def get_chart(symbol):

    '''Get historical data from Yahoo Finance.'''
    
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'

    today = datetime.today().timestamp()

    params = {
        'events': 'capitalGain%7Cdiv%7Csplit',
        'includeAdjustedClose': 'true',
        'interval': '1d',
        'period1': -6106060800,
        'period2': int(today),
    }

    headers = {
        'cookie': 'tbla_id=b24e82d1-970b-4fc7-8f92-6c95a3501717-tucte3a8897; OTH=v=2&s=0&d=eyJraWQiOiIwIiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiRTNMVkxKQzUzVFMzTEdWTFRDNEEyRlROTE0iLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJnaHkwY05FY0hOTWkifX0.jce2kAPKkx9BllZedYEWRE9bUVhdQPqYO9gXSG-a9idvQvTwhXvg9kn8ZXONhNCOull7Z7U_2LKpLDnhJ5AmDjUtF_AUn2nal23OinE-JoEnjp5ZckXSqPN6s1uVgsUiQ5AOBU95UXDsX51BmA682XeJMujYDbPO2kLqbHcalN4; OTHD=g=B3EAE7D6E93E5550B1CE3332572E4C5CD23D40997D3B075C53D14CA9D6333721&s=71188DDF7256CAA77C20B36FA354BEE2AE25D6E7D3D4A527F46806D7ACCA5C78&b=bid-clmlelhjju560&j=ca&bd=4717356ddcecdcd95a7d91fa4da4d734&gk=x1a9z-qJCjBBcc&sk=x1a9z-qJCjBBcc&bk=x1a9z-qJCjBBcc&iv=4FFE0808DC664345BF3D2B261864103A&v=1&u=0; F=d=G3A7c.E9vDfnvhmumk4AaRBqwFhZTNO0opAIPOqDAIdMv7V5sf0-; T=af=JnRzPTE3NDM1OTM0MjQmcHM9dUZ4ZEd3NUZFOGF3dlBEQlA1TEVoQS0t&d=bnMBeWFob28BZwFFM0xWTEpDNTNUUzNMR1ZMVEM0QTJGVE5MTQFhYwFBTUphSy5lQgFhbAFxY3guZWNvbkBnbWFpbC5jb20Bc2MBbWJyX3JlZ2lzdHJhdGlvbgFmcwFJdVZ6QVk5bjdSX1EBenoBUS9SN25CQTdFAWEBUUFFAWxhdAFRL1I3bkIBbnUBMA--&kt=EAAcuUvQd4dK5tMAFvPUcCwgA--~I&ku=FAAKJoNoTjFSmumohPcQC2hoHN8.V7It.UZ3bNEz0iWbjEmJFshulMtmg14rTRiv51gIYLCJpfcz82zP.cL_KC71FTD5IZoEyC6RrTDbXcHVfU.aJ_a6R4JUTcnUJLyupjGEcqDNYRGHdQdH1cENA0I9iLIwqbzQlcsx5hlTej3f6U-~E; PH=l=en-CA; Y=v=1&n=6i0c3tlkbrq6k&l=fpd0lcfjkifhe08bdc2xtt3fjhdlf8mvjg35i2e7/o&p=n30vvca00000000&r=1es&intl=ca; axids=gam=y-eWDDnRFG2uL1_t8UrTqFVOe4ahifgsBXl0FPUH8linbU.K6l_w---A&dv360=eS1IaUZTVDBGRTJ1RXA4WXdJcm1fSGdERVQ3ZkRHVEhrSEtKb0d0UUkzazlMZ1BsMUptVE8wT1dVaDdYQWUuSmFmZlZkZX5B&ydsp=y-YIwKMfJE2uJQcWV6VtSuwNZDITyZgpXkLhHQ6GSCPCOd6Vl2bz11p.ibX8679L9ZJ1uH~A&tbla=y-cxoR9UdG2uJ7RFqSPlCDnuXqo46H5IzEzWzILFV_LQPiAHigWg---A; GUC=AQEACAJn7mVoGkIkbQTG&s=AQAAAIIFkmyf&g=Z-0f4Q; A1=d=AQABBMAUP2cCEPOeje_KrxV8JHFGrqyu2soFEgEACAJl7mcaaCXUxyMA_eMDAAcIwBQ_Z6yu2soID97rTSTqyE-LbcnGXPRgYwkBBwoBEg&S=AQAAAj9VrtnxktUyGQwKfo4np0A; A3=d=AQABBMAUP2cCEPOeje_KrxV8JHFGrqyu2soFEgEACAJl7mcaaCXUxyMA_eMDAAcIwBQ_Z6yu2soID97rTSTqyE-LbcnGXPRgYwkBBwoBEg&S=AQAAAj9VrtnxktUyGQwKfo4np0A; cmp=t=1745441860&j=0&u=1---; gpp=DBAA; gpp_sid=-1; PRF=t%3DAAPL%252BBLDP%252BNMAX%252BNVDA%26ft%3DthemeSwitchEducation%26dock-collapsed%3Dtrue%26su-oo%3Dtrue; A1S=d=AQABBMAUP2cCEPOeje_KrxV8JHFGrqyu2soFEgEACAJl7mcaaCXUxyMA_eMDAAcIwBQ_Z6yu2soID97rTSTqyE-LbcnGXPRgYwkBBwoBEg&S=AQAAAj9VrtnxktUyGQwKfo4np0A',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    resp = requests.get(url, headers=headers, params=params)
    return resp.json()