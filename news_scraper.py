"""
Live News Scraper for Indian News Sources
Supports multiple Indian news websites across different languages
"""

import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import pandas as pd
from typing import List, Dict
import time
from langdetect import detect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsHeadlineScraper:
    """Scrapes live news headlines from multiple Indian news sources"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # RSS feeds and direct sources for Indian news
        self.news_sources = {
            'Times of India': 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
            'NDTV': 'https://feeds.feedburner.com/ndtvnews-top-stories',
            'Hindu': 'https://www.thehindu.com/news/national/?service=rss',
            'Indian Express': 'https://indianexpress.com/feed/',
            'News18': 'https://www.news18.com/rss/india.xml',
            'Zee News': 'https://zeenews.india.com/rss/india-national-news.xml',
            'Hindustan Times': 'https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml',
            'Dainik Bhaskar (Hindi)': 'https://www.bhaskar.com/rss-feed/1001/',
            'Amar Ujala (Hindi)': 'https://www.amarujala.com/rss/national-news.xml',
        }
        
    def scrape_rss_feed(self, source_name: str, url: str) -> List[Dict]:
        """Scrape headlines from RSS feeds"""
        headlines = []
        try:
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:15]:  # Get top 15 headlines
                try:
                    headline = {
                        'source': source_name,
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.get('published', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'language': self._detect_language(entry.title)
                    }
                    headlines.append(headline)
                except Exception as e:
                    logger.warning(f"Error parsing entry from {source_name}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            
        return headlines
    
    def scrape_times_of_india_direct(self) -> List[Dict]:
        """Direct scraping from Times of India main page"""
        headlines = []
        try:
            response = requests.get('https://timesofindia.indiatimes.com/', 
                                   headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find headline elements
            headline_elements = soup.find_all('a', class_='w_tle')[:10]
            
            for elem in headline_elements:
                try:
                    headlines.append({
                        'source': 'Times of India (Direct)',
                        'title': elem.get_text(strip=True),
                        'link': elem.get('href', ''),
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'language': self._detect_language(elem.get_text(strip=True))
                    })
                except Exception as e:
                    continue
                    
        except Exception as e:
            logger.error(f"Error in direct TOI scraping: {e}")
            
        return headlines
    
    def scrape_ndtv_direct(self) -> List[Dict]:
        """Direct scraping from NDTV"""
        headlines = []
        try:
            response = requests.get('https://www.ndtv.com/', 
                                   headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find headline elements
            headline_elements = soup.find_all('h2', class_='newsHdng')[:10]
            
            for elem in headline_elements:
                try:
                    link_elem = elem.find('a')
                    if link_elem:
                        headlines.append({
                            'source': 'NDTV (Direct)',
                            'title': link_elem.get_text(strip=True),
                            'link': link_elem.get('href', ''),
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'language': self._detect_language(link_elem.get_text(strip=True))
                        })
                except Exception as e:
                    continue
                    
        except Exception as e:
            logger.error(f"Error in direct NDTV scraping: {e}")
            
        return headlines
    
    def _detect_language(self, text: str) -> str:
        """Detect language of the text"""
        try:
            lang = detect(text)
            lang_map = {
                'hi': 'Hindi',
                'en': 'English',
                'ta': 'Tamil',
                'te': 'Telugu',
                'bn': 'Bengali',
                'mr': 'Marathi',
                'gu': 'Gujarati',
                'kn': 'Kannada',
                'ml': 'Malayalam',
                'pa': 'Punjabi'
            }
            return lang_map.get(lang, lang)
        except:
            return 'Unknown'
    
    def scrape_all_sources(self) -> pd.DataFrame:
        """Scrape headlines from all configured sources"""
        all_headlines = []
        
        logger.info("Starting live news scraping...")
        
        # Scrape RSS feeds
        for source_name, url in self.news_sources.items():
            logger.info(f"Scraping {source_name}...")
            headlines = self.scrape_rss_feed(source_name, url)
            all_headlines.extend(headlines)
            time.sleep(0.5)  # Be respectful to servers
        
        # Scrape direct sources
        logger.info("Scraping direct sources...")
        all_headlines.extend(self.scrape_times_of_india_direct())
        time.sleep(0.5)
        all_headlines.extend(self.scrape_ndtv_direct())
        
        logger.info(f"Total headlines scraped: {len(all_headlines)}")
        
        # Convert to DataFrame
        df = pd.DataFrame(all_headlines)
        
        if not df.empty:
            # Remove duplicates based on title
            df = df.drop_duplicates(subset=['title'], keep='first')
            df = df.reset_index(drop=True)
        
        return df


if __name__ == "__main__":
    scraper = NewsHeadlineScraper()
    headlines_df = scraper.scrape_all_sources()
    print(f"\nScraped {len(headlines_df)} unique headlines")
    print("\nSample headlines:")
    print(headlines_df.head())
