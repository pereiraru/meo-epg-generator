#!/usr/bin/env python3
"""
MEO EPG Generator for UHF App
Generates XMLTV format EPG from MEO Portugal TV guide
"""

from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, ElementTree
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MEOEPGGenerator:
    """Generate XMLTV EPG from MEO Portugal"""

    # Complete mapping of MEO TV channels
    CHANNEL_MAP = {
        'RTP1': {'name': 'RTP 1', 'number': 1, 'icon': 'https://www.meo.pt/PublishingImages/rtp1.png'},
        'RTP2': {'name': 'RTP 2', 'number': 2, 'icon': 'https://www.meo.pt/PublishingImages/rtp2.png'},
        'SIC': {'name': 'SIC', 'number': 3, 'icon': 'https://www.meo.pt/PublishingImages/sic.png'},
        'TVI': {'name': 'TVI', 'number': 4, 'icon': 'https://www.meo.pt/PublishingImages/tvi.png'},
        'SICNOT': {'name': 'SIC Notícias', 'number': 5, 'icon': 'https://www.meo.pt/PublishingImages/sicnoticias.png'},
        'RTPNOT': {'name': 'RTP Notícias', 'number': 6, 'icon': 'https://www.meo.pt/PublishingImages/rtpnoticias.png'},
        'CNN': {'name': 'CNN Portugal', 'number': 7, 'icon': 'https://www.meo.pt/PublishingImages/cnn.png'},
        'TVICNN': {'name': 'TVI Reality', 'number': 8, 'icon': 'https://www.meo.pt/PublishingImages/tvireality.png'},
        'ARTP': {'name': 'RTP Açores', 'number': 10, 'icon': 'https://www.meo.pt/PublishingImages/rtpacores.png'},
        'MRTP': {'name': 'RTP Madeira', 'number': 11, 'icon': 'https://www.meo.pt/PublishingImages/rtpmadeira.png'},
        'RTPI': {'name': 'RTP Internacional', 'number': 12, 'icon': 'https://www.meo.pt/PublishingImages/rtpinternacional.png'},
        'RTP3': {'name': 'RTP 3', 'number': 13, 'icon': 'https://www.meo.pt/PublishingImages/rtp3.png'},
        'SIC': {'name': 'SIC', 'number': 15, 'icon': 'https://www.meo.pt/PublishingImages/sic.png'},
        'TVI': {'name': 'TVI', 'number': 16, 'icon': 'https://www.meo.pt/PublishingImages/tvi.png'},
        'RTPMEM': {'name': 'RTP Memória', 'number': 18, 'icon': 'https://www.meo.pt/PublishingImages/rtpmemoria.png'},
        'TVIInt': {'name': 'TVI Internacional', 'number': 20, 'icon': 'https://www.meo.pt/PublishingImages/tviinternacional.png'},
        'ARTV': {'name': 'ARTV', 'number': 30, 'icon': 'https://www.meo.pt/PublishingImages/artv.png'},
        'PORTOCANAL': {'name': 'Porto Canal', 'number': 35, 'icon': 'https://www.meo.pt/PublishingImages/portocanal.png'},
        'EURON': {'name': 'Euronews', 'number': 40, 'icon': 'https://www.meo.pt/PublishingImages/euronews.png'},
        'CART': {'name': 'Cartoon Network', 'number': 41, 'icon': 'https://www.meo.pt/PublishingImages/cartoon.png'},
        'PANDA': {'name': 'Canal Panda', 'number': 42, 'icon': 'https://www.meo.pt/PublishingImages/canalpanda.png'},
        'DISNEY': {'name': 'Disney Channel', 'number': 43, 'icon': 'https://www.meo.pt/PublishingImages/disney.png'},
        'NICKJR': {'name': 'Nick Jr.', 'number': 44, 'icon': 'https://www.meo.pt/PublishingImages/nickjr.png'},
        'NICK': {'name': 'Nickelodeon', 'number': 45, 'icon': 'https://www.meo.pt/PublishingImages/nickelodeon.png'},
        'DISNEY': {'name': 'Disney Junior', 'number': 46, 'icon': 'https://www.meo.pt/PublishingImages/disneyjunior.png'},
        'BABYTV': {'name': 'Baby TV', 'number': 47, 'icon': 'https://www.meo.pt/PublishingImages/babytv.png'},
        'JIMJAM': {'name': 'Jim Jam', 'number': 48, 'icon': 'https://www.meo.pt/PublishingImages/jimjam.png'},
        'BLAST': {'name': 'BLAST', 'number': 49, 'icon': 'https://www.meo.pt/PublishingImages/blast.png'},
        'SPORT': {'name': 'Sport TV 1', 'number': 50, 'icon': 'https://www.meo.pt/PublishingImages/sporttv1.png'},
        'SPORT2': {'name': 'Sport TV 2', 'number': 51, 'icon': 'https://www.meo.pt/PublishingImages/sporttv2.png'},
        'SPORT3': {'name': 'Sport TV 3', 'number': 52, 'icon': 'https://www.meo.pt/PublishingImages/sporttv3.png'},
        'SPORT4': {'name': 'Sport TV 4', 'number': 53, 'icon': 'https://www.meo.pt/PublishingImages/sporttv4.png'},
        'SPORT5': {'name': 'Sport TV 5', 'number': 54, 'icon': 'https://www.meo.pt/PublishingImages/sporttv5.png'},
        'SPORT6': {'name': 'Sport TV 6', 'number': 55, 'icon': 'https://www.meo.pt/PublishingImages/sporttv6.png'},
        'BENFICA': {'name': 'Benfica TV', 'number': 56, 'icon': 'https://www.meo.pt/PublishingImages/benficatv.png'},
        'SPORTING': {'name': 'Sporting TV', 'number': 57, 'icon': 'https://www.meo.pt/PublishingImages/sportingtv.png'},
        'ELEV': {'name': 'Eleven Sports 1', 'number': 58, 'icon': 'https://www.meo.pt/PublishingImages/eleven1.png'},
        'ELEV2': {'name': 'Eleven Sports 2', 'number': 59, 'icon': 'https://www.meo.pt/PublishingImages/eleven2.png'},
        'DAZN': {'name': 'DAZN', 'number': 60, 'icon': 'https://www.meo.pt/PublishingImages/dazn.png'},
        'HOLHD': {'name': 'Hollywood', 'number': 61, 'icon': 'https://www.meo.pt/PublishingImages/hollywood.png'},
        'FOXMOVHD': {'name': 'FOX Movies', 'number': 62, 'icon': 'https://www.meo.pt/PublishingImages/foxmovies.png'},
        'AMCHD': {'name': 'AMC', 'number': 63, 'icon': 'https://www.meo.pt/PublishingImages/amc.png'},
        'AXN': {'name': 'AXN', 'number': 70, 'icon': 'https://www.meo.pt/PublishingImages/axn.png'},
        'AXNW': {'name': 'AXN White', 'number': 71, 'icon': 'https://www.meo.pt/PublishingImages/axnwhite.png'},
        'AXNMOVIES': {'name': 'AXN Movies', 'number': 72, 'icon': 'https://www.meo.pt/PublishingImages/axnmovies.png'},
        'FOX': {'name': 'FOX', 'number': 73, 'icon': 'https://www.meo.pt/PublishingImages/fox.png'},
        'FOXLIFE': {'name': 'FOX Life', 'number': 74, 'icon': 'https://www.meo.pt/PublishingImages/foxlife.png'},
        'FOXCRIME': {'name': 'FOX Crime', 'number': 75, 'icon': 'https://www.meo.pt/PublishingImages/foxcrime.png'},
        'FOXCOMEDY': {'name': 'FOX Comedy', 'number': 76, 'icon': 'https://www.meo.pt/PublishingImages/foxcomedy.png'},
        'COSMO': {'name': 'Cosmopolitan', 'number': 77, 'icon': 'https://www.meo.pt/PublishingImages/cosmopolitan.png'},
        'E': {'name': 'E! Entertainment', 'number': 78, 'icon': 'https://www.meo.pt/PublishingImages/eentertainment.png'},
        'TVS': {'name': 'TV Série', 'number': 79, 'icon': 'https://www.meo.pt/PublishingImages/tvserie.png'},
        'CINEMUNDO': {'name': 'Cinemundo', 'number': 80, 'icon': 'https://www.meo.pt/PublishingImages/cinemundo.png'},
        'SYFY': {'name': 'SyFy', 'number': 81, 'icon': 'https://www.meo.pt/PublishingImages/syfy.png'},
        'DISC': {'name': 'Discovery Channel', 'number': 90, 'icon': 'https://www.meo.pt/PublishingImages/discovery.png'},
        'NATGEO': {'name': 'National Geographic', 'number': 91, 'icon': 'https://www.meo.pt/PublishingImages/natgeo.png'},
        'NATGEOWILD': {'name': 'Nat Geo Wild', 'number': 92, 'icon': 'https://www.meo.pt/PublishingImages/natgeowild.png'},
        'HIST': {'name': 'History Channel', 'number': 93, 'icon': 'https://www.meo.pt/PublishingImages/history.png'},
        'ODISSEIA': {'name': 'Odisseia', 'number': 94, 'icon': 'https://www.meo.pt/PublishingImages/odisseia.png'},
        'CACAV': {'name': 'Caça e Pesca', 'number': 95, 'icon': 'https://www.meo.pt/PublishingImages/cacaepesca.png'},
        'TRAV': {'name': 'Travel Channel', 'number': 96, 'icon': 'https://www.meo.pt/PublishingImages/travel.png'},
        'CRIME': {'name': 'Crime + Investigation', 'number': 97, 'icon': 'https://www.meo.pt/PublishingImages/crime.png'},
        '24KIT': {'name': '24 Kitchen', 'number': 100, 'icon': 'https://www.meo.pt/PublishingImages/24kitchen.png'},
        'TVCINE1': {'name': 'TVCine Top', 'number': 105, 'icon': 'https://www.meo.pt/PublishingImages/tvcinetop.png'},
        'TVCINE2': {'name': 'TVCine Edition', 'number': 106, 'icon': 'https://www.meo.pt/PublishingImages/tvcineedition.png'},
        'TVCINE3': {'name': 'TVCine Emotion', 'number': 107, 'icon': 'https://www.meo.pt/PublishingImages/tvcineemotion.png'},
        'TVCINE4': {'name': 'TVCine Action', 'number': 108, 'icon': 'https://www.meo.pt/PublishingImages/tvcineaction.png'},
        'AMCBRE': {'name': 'AMC Break', 'number': 109, 'icon': 'https://www.meo.pt/PublishingImages/amcbreak.png'},
        'VH1': {'name': 'VH1', 'number': 111, 'icon': 'https://www.meo.pt/PublishingImages/vh1.png'},
        'MTV': {'name': 'MTV Portugal', 'number': 112, 'icon': 'https://www.meo.pt/PublishingImages/mtv.png'},
        'MCM': {'name': 'MCM Pop', 'number': 113, 'icon': 'https://www.meo.pt/PublishingImages/mcm.png'},
        'AFROMU': {'name': 'Afro Music', 'number': 114, 'icon': 'https://www.meo.pt/PublishingImages/afromusic.png'},
        'MEZZO': {'name': 'Mezzo', 'number': 115, 'icon': 'https://www.meo.pt/PublishingImages/mezzo.png'},
        'FUEL': {'name': 'Fuel TV', 'number': 120, 'icon': 'https://www.meo.pt/PublishingImages/fueltv.png'},
        'MOTORS': {'name': 'Motors TV', 'number': 121, 'icon': 'https://www.meo.pt/PublishingImages/motorstv.png'},
        'CASACOZ': {'name': 'Casa e Cozinha', 'number': 122, 'icon': 'https://www.meo.pt/PublishingImages/casaecozinha.png'},
        'FASHIONTV': {'name': 'Fashion TV', 'number': 123, 'icon': 'https://www.meo.pt/PublishingImages/fashiontv.png'},
        'LUXE': {'name': 'Luxe TV', 'number': 124, 'icon': 'https://www.meo.pt/PublishingImages/luxetv.png'},
        'TOROS': {'name': 'Toros TV', 'number': 125, 'icon': 'https://www.meo.pt/PublishingImages/torostv.png'},
        'FINE': {'name': 'Fine Living', 'number': 126, 'icon': 'https://www.meo.pt/PublishingImages/fineliving.png'},
    }

    def __init__(self, days=7):
        self.days = days
        self.channels = {}
        self.programs = {}

    def fetch_channels(self):
        """Load channels from CHANNEL_MAP"""
        logger.info("Loading channels from CHANNEL_MAP...")

        for channel_id, channel_info in self.CHANNEL_MAP.items():
            self.channels[channel_id] = {
                'id': channel_id,
                'name': channel_info.get('name', channel_id),
                'number': channel_info.get('number', 0),
                'icon': channel_info.get('icon', ''),
            }

        logger.info(f"Loaded {len(self.channels)} channels")
        return len(self.channels) > 0

    def fetch_schedule(self):
        """Generate placeholder schedule data"""
        logger.info(f"Generating placeholder schedule for {self.days} days...")

        # Note: Since MEO's website now requires authentication and is fully JavaScript-rendered,
        # we generate a minimal valid EPG structure. Users can still see the channel list.
        # In the future, this could be enhanced with an authenticated API approach.

        for day_offset in range(self.days):
            date = datetime.now() + timedelta(days=day_offset)
            date_str = date.strftime('%Y-%m-%d')

            for channel_id in self.channels.keys():
                # Create a placeholder program for each channel/day
                # This ensures the EPG is valid even without actual program data
                prog_key = f"{date_str}_{channel_id}_placeholder"
                self.programs[prog_key] = {
                    'date': date_str,
                    'channel': channel_id,
                    'title': f'Ver {self.channels[channel_id]["name"]}',
                    'time': '00:00',
                    'description': 'Consulte a programação em www.meo.pt'
                }

        logger.info(f"Generated {len(self.programs)} placeholder programs")
        return True

    def generate_xmltv(self):
        """Generate XMLTV format EPG"""
        logger.info("Generating XMLTV...")

        tv = Element('tv')
        tv.set('generator-info-name', 'MEO EPG Generator')
        tv.set('generator-info-url', 'https://github.com/pereiraru/meo-epg-generator')

        # Add channels
        for channel_id, channel_data in sorted(self.channels.items(), key=lambda x: x[1].get('number', 999)):
            channel_elem = SubElement(tv, 'channel')
            channel_elem.set('id', channel_id)

            display_name = SubElement(channel_elem, 'display-name')
            display_name.set('lang', 'pt')
            display_name.text = channel_data.get('name', channel_id)

            # Add channel number if available
            if channel_data.get('number'):
                display_name_num = SubElement(channel_elem, 'display-name')
                display_name_num.set('lang', 'pt')
                display_name_num.text = str(channel_data['number'])

            # Add icon if available
            if channel_data.get('icon'):
                icon = SubElement(channel_elem, 'icon')
                icon.set('src', channel_data['icon'])

        # Add programs
        for prog_id, prog_data in sorted(self.programs.items()):
            try:
                channel_id = prog_data['channel']
                if channel_id not in self.channels:
                    continue

                # Parse datetime
                date_str = prog_data['date']
                time_str = prog_data.get('time', '00:00')

                # Format as YYYYMMDDHHMMSS +0000
                try:
                    start_dt = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
                except:
                    start_dt = datetime.strptime(date_str, '%Y-%m-%d')

                # Set program duration to full day for placeholder programs
                end_dt = start_dt + timedelta(hours=24)

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
    logger.info("Note: MEO website now requires authentication. Generating EPG with channel list only.")

    try:
        generator = MEOEPGGenerator(days=7)

        # Load channels
        if not generator.fetch_channels():
            logger.error("Failed to load channels")
            return 1

        # Generate schedule
        if not generator.fetch_schedule():
            logger.warning("Some issues while generating schedule, but continuing...")

        # Save EPG
        if not generator.save('guide.xml'):
            logger.error("Failed to save EPG")
            return 1

        logger.info("MEO EPG Generator completed successfully")
        logger.info(f"Generated EPG with {len(generator.channels)} channels for {generator.days} days")
        return 0

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())
