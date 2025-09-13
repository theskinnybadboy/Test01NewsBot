import asyncio
import feedparser
from telegram import Bot
import json
import os 

# Keys

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

# Multiple Rss Feeds

RSS_FEEDS = {
    "BBC_MiddleEast" : "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "BBC_Africa" : "https://feeds.bbci.co.uk/news/world/africa/rss.xml",
    "BBC_LatinAmerica" : "https://feeds.bbci.co.uk/news/world/latin_america/rss.xml",
    "BBC_Asia" : "https://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "BBC_US_Canada" : "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
    "BBC_Europe" : "https://feeds.bbci.co.uk/news/world/europe/rss.xml",
    "BBC_Farsi" : "https://feeds.bbci.co.uk/persian/rss.xml",
    "BBC_Europe" : "https://feeds.bbci.co.uk/news/world/europe/rss.xml",
    "BBC_UK" : "https://feeds.bbci.co.uk/news/england/rss.xml",
    "BBC_NorthernIreland" : "https://feeds.bbci.co.uk/news/northern_ireland/rss.xml",
    "BBC_Scotland" : "https://feeds.bbci.co.uk/news/scotland/rss.xml",
    "BBC_Wales" : "https://feeds.bbci.co.uk/news/wales/rss.xml",
    "Democracy Now" : "https://www.democracynow.org/democracynow.rss",
    "Jacobin" : "https://jacobin.com/feed",
    "Al Jazeera" : "https://www.aljazeera.com/xml/rss/all.xml",
    "Politico - Congress" : "https://rss.politico.com/congress.xml",
    "Politico - Defense" : "https://rss.politico.com/defense.xml",
    "Politico - Economy" : "https://rss.politico.com/economy.xml",
    "Politico - Energy" : "https://rss.politico.com/energy.xml",
    "Politico - News" : "https://rss.politico.com/politics-news.xml",
    "Politico_eu" : "https://www.politico.eu/feed/",
    "Politico_News_MorningTech" : "https://rss.politico.com/morningtech.xml",
    "Politico_News_MorningMoney" : "https://rss.politico.com/morningmoney.xml",
    "Politico_News_Pluse" : "https://rss.politico.com/politicopulse.xml",
    "Politico_News_Influence" : "https://rss.politico.com/politicoinfluence.xml",
    "Politico_News_MorningEnergy" : "https://rss.politico.com/morningdefense.xml",
    "Politico_News_Transportation" : "https://rss.politico.com/morningtransportation.xml",
    "Politico_News_MorningEducation" : "https://rss.politico.com/morningeducation.xml",
    "Politico_News_MorningTax" : "https://rss.politico.com/morningtax.xml",
    "Politico_News_MorningCybersecurity" : "https://rss.politico.com/morningcybersecurity.xml",
    "Politico_News_MorningTrade" : "https://rss.politico.com/morningtrade.xml",
    "Financial Times - World" : "https://rss.app/feeds/F7pRTAPgNccNqRhh.xml",
    "Reuters" : "http://feeds.reuters.com/reuters/worldNews",
    "IranWire" : "https://iranwire.com/fa/feed/",
    "Tasnim_Politics" : "https://www.tasnimnews.com/fa/rss/feed/0/7/1/%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C",
    "Tasnim_Khameni" : "https://www.tasnimnews.com/fa/rss/feed/0/7/1127/%D8%A7%D9%85%D8%A7%D9%85-%D9%88-%D8%B1%D9%87%D8%A8%D8%B1%DB%8C",
    "Hammihan_Economics" : "https://hammihanonline.ir/fa/feeds/?p=Y2F0ZWdvcmllcz01",
    "Hammihan_International" : "https://hammihanonline.ir/fa/feeds/?p=Y2F0ZWdvcmllcz0yMA%2C%2C",
    "Hammihan_Diplomacy" : "https://hammihanonline.ir/fa/feeds/?p=Y2F0ZWdvcmllcz02",
    "Hammihan_Society" : "https://hammihanonline.ir/fa/feeds/?p=Y2F0ZWdvcmllcz0yMw%2C%2C",
    "Shargh_Politics" : "https://www.sharghdaily.com/fa/feeds/?p=Y2F0ZWdvcmllcz02",
    "Shargh_Economics" : "https://www.sharghdaily.com/fa/feeds/?p=Y2F0ZWdvcmllcz0xMg%2C%2C",
    "Shargh_Society" : "https://www.sharghdaily.com/fa/feeds/?p=Y2F0ZWdvcmllcz0yMjA%2C",
    "donya-e-eqtesad" : "https://donya-e-eqtesad.com/feeds/",
    "Eghtesadonline_price" : "https://www.eghtesadonline.com/fa/rss/5",
    "Eghtesadonline_cars" : "https://www.eghtesadonline.com/fa/rss/6",
    "Eghtesadonline_Iran" : "https://www.eghtesadonline.com/fa/rss/7",
    "Eghtesadonline-bourse" : "https://www.eghtesadonline.com/fa/rss/9",
    "Eghtesadonline_crypto" : "https://www.eghtesadonline.com/fa/rss/10",
    "Eghtesadonline_politics" : "https://www.eghtesadonline.com/fa/rss/11",
    "Jpost_Gaza" : "https://www.jpost.com/rss/rssfeedsgaza.aspx",
    "Jpost_Headlines" : "https://www.jpost.com/rss/rssfeedsheadlines.aspx",
    "Jpost_politicsdiplomacy" : "https://www.jpost.com/rss/rssfeedspoliticsdiplomacy.aspx",
    "Jpost_Iran" : "https://www.jpost.com/rss/rssfeedsiran",
    "Jpost_Middleeast" : "https://www.jpost.com/rss/rssfeedsmiddleeastnews.aspx",
    "Jpost_American" : "https://www.jpost.com/rss/rssfeedsamerican-politics",
    "WashingtonPost_Politics" : "https://www.washingtonpost.com/arcio/rss/category/politics/",
    "Middleeasteye" : "https://www.middleeasteye.net/rss",
    "Podcast_In bed with her right" : "https://media.rss.com/inbedwiththeright/feed.xml",
    "nytimes_World" : "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "nytime_Africa" : "https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml",
    "nytimes_Americas" : "https://rss.nytimes.com/services/xml/rss/nyt/Americas.xml",
    "nytimes_AsiaPacific" : "https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml",
    "nytimes_Europe" : "https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml",
    "nytimes_MidlleEast" : "https://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml",
    "nytimes_US" : "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
    "nytimes_US_education" : "https://rss.nytimes.com/services/xml/rss/nyt/Education.xml",
    "nytimes_US_Politics" : "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
    "nytimes_US_Economy" : "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml",
    "nytimes_EnergyEnvironment" : "rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml",
    "nytimes_Technology" : "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "theGuardian_World" : "https://www.theguardian.com/world/rss",
    "theGuardian_europe" : "https://www.theguardian.com/world/europe-news/rss",
    "theGaurdian_US" : "https://www.theguardian.com/us-news/rss",
    "theGaurdian_Americas" : "https://www.theguardian.com/world/americas/rss",
    "theGaurdian_Asia" : "https://www.theguardian.com/world/asia/rss",
    "theGaurdian_Australia" : "https://www.theguardian.com/australia-news/rss",
    "theGaurdian_Midleeast" : "https://www.theguardian.com/world/middleeast/rss",
    "theGaurdian_Africa" : "https://www.theguardian.com/world/africa/rss",
    "theGaurdian_Inequality" : "https://www.theguardian.com/inequality/rss",
    "theGaurdian_global-development" : "https://www.theguardian.com/global-development/rss",
    "ForeignPolicy" : "https://foreignpolicy.com/feed/",
    "Rusi_LatestPublications" : "https://www.rusi.org/rss/latest-publications.xml",
    "Rusi_What's New" : "https://www.rusi.org/rss/whats-new.xml",
    "Rusi_latest-commentary" : "https://www.rusi.org/rss/latest-commentary.xml",
    "Rusi_upcoming-events" : "https://www.rusi.org/rss/upcoming-events.xml",
    "warontherocks" : "https://warontherocks.com/feed/",
    "TheWallStreetJournal_Opnion" : "https://feeds.content.dowjones.io/public/rss/RSSOpinion",
    "TheWallStreetJournal_WorldNews" : "https://feeds.content.dowjones.io/public/rss/RSSWorldNews",
    "TheWallStreetJournal_USBusiness" : "https://feeds.content.dowjones.io/public/rss/WSJcomUSBusiness",
    "TheWallStreetJournal_MarketsMain" : "https://feeds.content.dowjones.io/public/rss/RSSMarketsMain",
    "TheWallStreetJournal_WSJD" : "https://feeds.content.dowjones.io/public/rss/RSSWSJD",
    "TheWallStreetJournal_USnews" : "https://feeds.content.dowjones.io/public/rss/RSSUSnews",
    "TheWallStreetJournal_SocialPolitics" : "https://feeds.content.dowjones.io/public/rss/socialpoliticsfeed",
    "TheWallStreetJournal_SocialEconomy" : "https://feeds.content.dowjones.io/public/rss/socialeconomyfeed",
    "TheWallStreetJournal_ArtsCulture" : "https://feeds.content.dowjones.io/public/rss/RSSArtsCulture",
    "TheWallStreetJournal_latestnewsrealestate" : "https://feeds.content.dowjones.io/public/rss/latestnewsrealestate",
    "TheWallStreetJournal_SocialHealth" : "https://feeds.content.dowjones.io/public/rss/socialhealth",
    "DW_World" : "https://rss.dw.com/rdf/rss-en-world",
    "DW_Europe" : "https://rss.dw.com/rdf/rss-en-eu",
    "DW_Enviroment" : "https://rss.dw.com/xml/rss_en_environment",
    "DW_Asia" : "https://rss.dw.com/rdf/rss-en-asia",
    "DW_TOP" : "https://rss.dw.com/rdf/rss-en-top",
    "DW_all" : "https://rss.dw.com/rdf/rss-en-all",
    "theDiplomat_all" : "https://thediplomat.com/feed/",
    "theDiplomat_Society" : "https://thediplomat.com/topics/society/feed/",
    "theDiplomat_Central_Asia" : "https://thediplomat.com/regions/central-asia/feed/",
    "theDiplomat_East_Asia" : "https://thediplomat.com/regions/east-asia/feed/",
    "theDiplomat_Oceania_region" : "https://thediplomat.com/regions/oceania-region/feed/",
    "theDiplomat_SouthAsia" : "https://thediplomat.com/regions/south-asia/feed/",
    "theDiplomat_SoutheastAsia" : "https://thediplomat.com/regions/southeast-asia/feed/",
    "theDiplomat_Diplomacy" : "https://thediplomat.com/topics/diplomacy/feed/",
    "theDiplomat_Economy" : "https://thediplomat.com/topics/economy/feed/",
    "theDiplomat_Environment" : "https://thediplomat.com/topics/environment/feed/",
    "theDiplomat_Opnion" : "https://thediplomat.com/topics/opinion/feed/",
    "theDiplomat_Politics" : "https://thediplomat.com/topics/politics/feed/",
    "theDiplomat_Security" : "https://thediplomat.com/topics/security/feed/", 
    "SCMP_News" : "https://www.scmp.com/rss/91/feed/",
    "SCMP_HONGKONG" : "https://www.scmp.com/rss/2/feed/",
    "SCMP_China" : "https://www.scmp.com/rss/4/feed/",
    "SCMP_ASIA" : "https://www.scmp.com/rss/3/feed/",
    "SCMP_WORLD" : "https://www.scmp.com/rss/5/feed/",
    "SCMP_PeopleCulture" : "https://www.scmp.com/rss/318202/feed/",
    "SCMP_CHINA-PoliciesPolitics" : "https://www.scmp.com/rss/318198/feed/",
    "SCMP_CHINA_DiplomacyDefence" : "https://www.scmp.com/rss/318199/feed/",
    "SCMP_CHINA_MoneyWealth" : "https://www.scmp.com/rss/318200/feed/",
    "SCMP_CHINA_Economy" : "https://www.scmp.com/rss/318421/feed/",
    "SCMP_CHINA_Society" : "https://www.scmp.com/rss/318202/feed/",
    "SCMP_HONGKONG_Politics" : "https://www.scmp.com/rss/318206/feed/",
    "SCMP_HONGKONG_Economy" : "https://www.scmp.com/rss/318210/feed/",
    "SCMP_HONGKONG_HealthEnvironment" : "https://www.scmp.com/rss/318208/feed/",
    "SCMP_HONGKONG_LawCrime" : "https://www.scmp.com/rss/318217/feed/",
    "SCMP_EducationCommunity" : "https://www.scmp.com/rss/318207/feed/",
    "SCMP_WORLD_USCanada" : "https://www.scmp.com/rss/322262/feed/",
    "SCMP_WORLD_Europe" : "https://www.scmp.com/rss/322263/feed/",
    "SCMP_WORLD_Middleeast" : "https://www.scmp.com/rss/322264/feed/",
    "SCMP_Americas" : "https://www.scmp.com/rss/322265/feed/",
    "SCMP_Africa" : "https://www.scmp.com/rss/322266/feed/",
    "SCMP_RusiiaCenteralAsia" : "https://www.scmp.com/rss/322514/feed/",
    "SCMP_ASIA_Australasia" : "https://www.scmp.com/rss/322243/feed/",
    "SCMP_Diplomacy" : "https://www.scmp.com/rss/318213/feed/",
    "SCMP_EastAsia" : "https://www.scmp.com/rss/318214/feed/",
    "SCMP_SoutheastAsia" : "https://www.scmp.com/rss/318215/feed/",
    "SCMP_SouthAsia" : "https://www.scmp.com/rss/318216/feed/",
    "SCMP_Business_ChinaEconomy" : "https://www.scmp.com/rss/318421/feed/",
    "nybooks" : "https://feeds.feedburner.com/nybooks",
    "theNation_Politics" : "https://www.thenation.com/politics/feed/",
    "theNation_Economy" : "https://www.thenation.com/economy/feed/",
    "theNation_Culture" : "https://www.thenation.com/culture/feed/",
    "theNation_Latest" : "https://www.thenation.com/latest/feed/",
    "theNation_Issue" : "https://www.thenation.com/issue/feed/",
    "theNation_Podcasts" : "https://www.thenation.com/podcasts/feed/",
    "theNation_World" : "https://www.thenation.com/world/feed/",
    "aeon" : "https://aeon.co/feed.rss",
    "independent" : "https://www.independent.co.uk/rss",
    "independent_NEWS_UK" : "https://www.independent.co.uk/news/uk/rss",
    "Independent_NEWS_US" : "https://www.independent.co.uk/us/rss",
    "Independent_NEWS_WORLD" : "https://www.independent.co.uk/news/world/rss",
    "Independent_GlobalAid" : "https://www.independent.co.uk/topic/rethinking-global-aid/rss",
    "independent_NEWS_UK_POLITICS" : "https://www.independent.co.uk/news/uk/politics/rss",
    "Independent_Money" : "https://www.independent.co.uk/money/rss",
    "TimeOfIsrael" : "https://www.timesofisrael.com/feed/",
    "Pravda" : "pravda.com.ua/eng/rss/",
    "aa" : "https://www.aa.com.tr/tr/rss/default?cat=guncel",
    



}








# setup

bot = Bot(token = BOT_TOKEN)
SENT_FILE = "sent_links.json"

# Load previously sent links (avoid duplicates)
if os.path.exists(SENT_FILE):
    with open(SENT_FILE, "r", encoding = "utf-8") as f:
        sent_links = set(json.load(f))
else:
    sent_links = set()



async def send_feed():
    global sent_links
    for source, url in RSS_FEEDS.items():
            try:
                # polite delay between requests
                await asyncio.sleep(5) #wait 10 seconds between sites

                feed = feedparser.parse(url)

                if feed.bozo:
                    print(f"❌ Failed to parse {source}")
                    continue

                for entry in feed.entries[:5]: # limit per source
                    link = entry.link
                    if link not in sent_links:
                        title = entry.title
                        message = f"📰 [{source}] {title}\n🔗 {link}\n\n📌 @imreadingnews"


                        try:
                            await bot.send_message(chat_id = CHANNEL, text = message)
                            print(f"✅ Sent: [{source}] {title}")
                            sent_links.add(link)

                            # Prevent Flood Control
                            await asyncio.sleep(5) # wait 5 seconds before next message

                        except Exception as e:
                            print(f"⚠️ Error sending message:{e}") # wait if Telegram complains
        
                # Save sent links
                with open(SENT_FILE, "w", encoding = "utf-8") as f:
                    json.dump(list(sent_links), f, ensure_ascii=False)
        
            except Exception as e:
                print(f"⚠️ Error fetching RSS feed: {e}")
                continue

async def main ():
    while True:
        await send_feed()
        await asyncio.sleep(300) #run every 5 minutes

if __name__ == "__main__":
    asyncio.run(main())