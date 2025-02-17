import random
import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


popular_sites = [
    "vnexpress.net",
    "zalo.me",
    "shopee.vn",
    "dienmayxanh.com",
    "viettel.com.vn",
    "fpt.com.vn",
    "vingroup.net",
    "momo.vn",
    "baomoi.com",
    "tiki.vn",
    "vinmec.com",
    "vietjetair.com",
    "benhvienk.vn",
    "vtv.vn",
    "congcaphe.com",
    "khanggia.com",
    "bigc.vn",
    "vnews.gov.vn",
    "vnpt.com.vn",
    "onemount.com",
    "truyenqqto.com",
    "24h.com.vn",
    "msn.com",
    "dantri.com.vn",
    "coccoc.com",
    "truyenfull.io",
    "thegioididong.com",
    "vietnamnet.vn",
    "kenh14.vn",
    "soha.vn",
    "tuoitre.vn",
    "thanhnien.vn",
    "vov.vn",
    "vietnamplus.vn",
    "thuvienphapluat.vn",
    "masothue.com",
    "laodong.vn",
    "bongdaplus.vn",
    "canva.com",
    "cafef.vn"
]

dkkd_sites = [
    "dangkykinhdoanh.gov.vn",
    "dichvuthongtin.dkkd.gov.vn",
    "dangkyquamang.dkkd.gov.vn",
    "hokinhdoanh.dkkd.gov.vn",
    "bocaodientu.dkkd.gov.vn",
    "bocaodientu.dkkd.gov.vn/egazette"
]

def simulate_browsing(driver, total=1, dkkd=False):
    sites = dkkd_sites if dkkd else popular_sites
    for _ in range(total):
        site = random.choice(sites)
        try:
            driver.execute_script(f"window.open('https://{site}', '_blank');") 
            driver.switch_to.window(driver.window_handles[-1]) 
            time.sleep(random.randint(4,8)/2)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])         
            time.sleep(1)
            logger.info(f"History simulated for {site}")
        except Exception as e:
            logger.error(f"Error while processing simulate for site {site}: {e}")

