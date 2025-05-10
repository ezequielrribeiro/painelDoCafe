from interface import PainelCafeApp
from src.scraping.load_promo import LoadPromos



if __name__ == "__main__":
    promoScrap = LoadPromos()
    promoScrap.scrapePromos()

    app = PainelCafeApp()
    app.setPromoMarkdown(promoScrap.getPromosMarkdown())
    app.run()
