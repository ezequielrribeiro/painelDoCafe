from interface import PainelCafeApp
from src.scraping.load_promo import LoadPromos



if __name__ == "__main__":
    promoScrap = LoadPromos()
    promoScrap.scrape_promos()

    app = PainelCafeApp()
    app.set_promo_markdown(promoScrap.get_promos_markdown())
    app.run()
