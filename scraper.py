#!/usr/bin/env python3
"""
MEO EPG Generator for UHF App
Generates XMLTV format EPG from MEO Portugal TV guide
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, ElementTree
import logging
import time
from urllib.parse import urljoin
import re

logging.basicConfig(
          level=logging.INFO,
          format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MEOEPGGenerator:
          """Generate XMLTV EPG from MEO Portugal"""

    BASE_URL = "https://www.meo.pt/tv/canais-programacao/guia-tv"
    CHANNEL_LIST_URL = "https://www.meo.pt/api/tv/channels"  # Possível endpoint da API

    # Mapeamento de IDs de canais para nomes e números
    CHANNEL_MAP = {
                  'RTP1': {'name': 'RTP 1', 'number': 1, 'icon': 'https://www.meo.pt/PublishingImages/rtp1.png'},
                  'RTP2': {'name': 'RTP 2', 'number': 2, 'icon': 'https://www.meo.pt/PublishingImages/rtp2.png'},
                  'SIC': {'name': 'SIC', 'number': 3, 'icon': 'https://www.meo.pt/PublishingImages/sic.png'},
                  'TVI': {'name': 'TVI', 'number': 4, 'icon': 'https://www.meo.pt/PublishingImages/tvi.png'},
                  'SICNOT': {'name': 'SIC Notícias', 'number': 5, 'icon': 'https://www.meo.pt/PublishingImages/sicnoticias.png'},
                  'RTPNOT': {'name': 'RTP Notícias', 'number': 6, 'icon': 'https://www.meo.pt/PublishingImages/rtpnoticias.png'},
                  'CNN': {'name': 'CNN Portugal', 'number': 7, 'icon': 'https://www.meo.pt/PublishingImages/cnn.png'},
                  'DISCOVERY': {'name': 'Discovery', 'number': 90, 'icon': 'https://www.meo.pt/PublishingImages/discovery.png'},
                  'CARTOON': {'name': 'Cartoon Network', 'number': 101, 'icon': 'https://www.meo.pt/PublishingImages/cartoon.png'},
    }

    def __init__(self, days=7):
                  self.days = days
                  self.session = requests.Session()
                  self.session.headers.update({
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                  })
                  self.channels = {}
                  self.programs = {}

    def fetch_channels(self):
                  """Fetch all channels from MEO"""
                  logger.info("Fetching channels from MEO...")
                  try:
                                    response = self.session.get(self.BASE_URL, timeout=10)
                                    response.encoding = 'utf-8'
                                    soup = BeautifulSoup(response.content, 'html.parser')

            # Procurar por todos os links de canais
            channel_links = soup.find_all('a', href=re.compile(r'/guia-tv/canal/'))

            for link in channel_links:
                                  href = link.get('href', '')
                                  match = re.search(r'/canal/([A-Z0-9]+)', href)
                                  if match:
                                                            channel_id = match.group(1)

                    if channel_id not in self.channels:
                                                  # Procurar pela imagem do canal
                                                  section = link.find_parent('section')
                                                  img = section.find('img') if section else None
                                                  img_src = img.get('src') or img.get('data-src') if img else ''

                        channel_info = self.CHANNEL_MAP.get(channel_id, {
                                                          'name': link.get_text(strip=True)[:30] or channel_id,
                                                          'number': 0,
                                                          'icon': img_src or ''
                        })

                        self.channels[channel_id] = {
                                                          'id': channel_id,
                                                          'name': channel_info.get('name', channel_id),
                                                          'number': channel_info.get('number', 0),
                                                          'icon': channel_info.get('icon', img_src if img_src else ''),
                                                          'url': href
                        }
                        logger.debug(f"Added channel: {channel_id} - {channel_info.get('name')}")

            logger.info(f"Found {len(self.channels)} channels")
            return len(self.channels) > 0

except Exception as e:
            logger.error(f"Error fetching channels: {e}")
            return False

    def fetch_schedule(self):
                  """Fetch schedule for multiple days"""
                  logger.info(f"Fetching schedule for {self.days} days...")
                  try:
                                    for day_offset in range(self.days):
                                                          date = datetime.now() + timedelta(days=day_offset)
                                                          date_str = date.strftime('%Y-%m-%d')

                logger.info(f"Fetching programs for {date_str}...")

                # Adicionar programas de exemplo (em produção, fazer scraping real)
                self._fetch_day_programs(date_str)

                time.sleep(1)  # Respeitar rate limiting

            logger.info(f"Fetched programs for {len(self.programs)} time slots")
            return True

except Exception as e:
            logger.error(f"Error fetching schedule: {e}")
            return False

    def _fetch_day_programs(self, date_str):
                  """Fetch programs for a specific date"""
                  try:
                                    params = {'date': date_str}
                                    response = self.session.get(
                                                          f"{self.BASE_URL}/dados",
                                                          params=params,
                                                          timeout=10
                                    )

            if response.status_code == 200:
                                  soup = BeautifulSoup(response.content, 'html.parser')

                # Procurar por programas (blocos com horários)
                program_elements = soup.find_all('div', class_=re.compile(r'programme|program|epg'))

                for prog in program_elements:
                                          try:
                                                                        # Extrair título
                                                                        title_elem = prog.find(['h3', 'h4', 'span'], class_=re.compile(r'title|name'))
                                                                        title = title_elem.get_text(strip=True) if title_elem else 'Unknown'

                        # Extrair horários
                        time_elem = prog.find(['time', 'span'], class_=re.compile(r'time|hour'))
                        time_text = time_elem.get_text(strip=True) if time_elem else ''

                        # Extrair canal
                        channel_elem = prog.find('a', href=re.compile(r'/canal/'))
                        channel_id = None
                        if channel_elem:
                                                          href = channel_elem.get('href', '')
                                                          match = re.search(r'/canal/([A-Z0-9]+)', href)
                                                          channel_id = match.group(1) if match else None

                        if title and channel_id and channel_id in self.channels:
                                                          prog_key = f"{date_str}_{channel_id}_{time_text}_{title}"
                                                          self.programs[prog_key] = {
                                                                                                'date': date_str,
                                                                                                'channel': channel_id,
                                                                                                'title': title,
                                                                                                'time': time_text,
                                                                                                'description': prog.get_text(strip=True)[:200]
                                                          }
except Exception as e:
                        logger.debug(f"Error parsing program: {e}")

except Exception as e:
            logger.error(f"Error fetching programs for {date_str}: {e}")

    def generate_xmltv(self) -> str:
                  """Generate XMLTV format EPG"""
                  logger.info("Generating XMLTV...")

        tv = Element('tv')
        tv.set('generator-info-name', 'MEO EPG Generator')
        tv.set('generator-info-url', 'https://github.com/pereiraru/meo-epg-generator')

        # Adicionar canais
        for channel_id, channel_data in sorted(self.channels.items()):
                          channel_elem = SubElement(tv, 'channel')
                          channel_elem.set('id', channel_id)

            display_name = SubElement(channel_elem, 'display-name')
            display_name.set('lang', 'pt')
            display_name.text = channel_data.get('name', channel_id)

            # Adicionar número do canal se disponível
            if channel_data.get('number'):
                                  display_name_num = SubElement(channel_elem, 'display-name')
                                  display_name_num.set('lang', 'pt')
                                  display_name_num.text = str(channel_data['number'])

            # Adicionar ícone se disponível
            if channel_data.get('icon'):
                                  icon = SubElement(channel_elem, 'icon')
                                  icon.set('src', channel_data['icon'])
                                  icon.set('width', '200')
                                  icon.set('height', '112')

        # Adicionar programas
        for prog_id, prog_data in sorted(self.programs.items()):
                          try:
                                                channel_id = prog_data['channel']
                                                if channel_id not in self.channels:
                                                                          continue

                # Parse datetime
                date_str = prog_data['date']
                time_str = prog_data.get('time', '00:00')

                # Formatar como YYYYMMDDHHMMSS +0000
                try:
                                          start_dt = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
                                      except:
                    start_dt = datetime.strptime(date_str, '%Y-%m-%d')

                # Assumir duração de 30 minutos se não especificado
                end_dt = start_dt + timedelta(minutes=30)

                prog_elem = SubElement(tv, 'programme')
                prog_elem.set('start', start_dt.strftime('%Y%m%d%H%M%S +0000'))
                prog_elem.set('stop', end_dt.strftime('%Y%m%d%H%M%S +0000'))
                prog_elem.set('channel', channel_id)

                title = SubElement(prog_elem, 'title')
                title.set('lang', 'pt')
                title.text = prog_data.get('title', 'Unknown Program')

                if prog_data.get('description'):
                                          desc = SubElement(prog_elem, 'desc')
                                          desc.set('lang', 'pt')
                                          desc.text = prog_data['description']

except Exception as e:
                logger.debug(f"Error creating programme element: {e}")

        # Converter para string
        return ElementTree(tv)

    def save(self, filename='guide.xml'):
                  """Save EPG to file"""
                  logger.info(f"Saving EPG to {filename}...")
                  try:
                                    xmltree = self.generate_xmltv()
                                    xmltree.write(
                                                          filename,
                                                          encoding='UTF-8',
                                                          xml_declaration=True
                                    )
                                    logger.info(f"EPG saved successfully to {filename}")
                                    return True
except Exception as e:
            logger.error(f"Error saving EPG: {e}")
            return False


def main():
          """Main entry point"""
          logger.info("Starting MEO EPG Generator")

    try:
                  generator = MEOEPGGenerator(days=7)

        # Fetch channels
        if not generator.fetch_channels():
                          logger.error("Failed to fetch channels")
                          return 1

        # Fetch schedule
        if not generator.fetch_schedule():
                          logger.warning("Some issues while fetching schedule, but continuing...")

        # Save EPG
        if not generator.save('guide.xml'):
                          logger.error("Failed to save EPG")
                          return 1

        logger.info("MEO EPG Generator completed successfully")
        return 0

except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
          exit(main())
