#!/usr/bin/env python3
"""
NOS EPG Generator for UHF App
Generates XMLTV format EPG from NOS Portugal TV guide
"""

import urllib.request
import json
import ssl
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, ElementTree
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NOSEPGGenerator:
    """Generate XMLTV EPG from NOS Portugal"""

    # NOS API Configuration
    API_BASE = 'https://api.clg.nos.pt/nostv/ott'
    CLIENT_ID = 'xe1dgrShwdR1DVOKGmsj8Ut4QLlGyOFI'
    ICON_BASE_URL = 'https://raw.githubusercontent.com/pereiraru/meo-epg-generator/main/channel_icons/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
        'x-apikey': CLIENT_ID,
        'X-Core-DeviceType': 'WEB',
        'Origin': 'https://nostv.pt',
        'Referer': 'https://nostv.pt/'
    }

    def __init__(self, days=7):
        self.days = days
        self.channels = {}
        self.programs = {}
        # Create SSL context that doesn't verify certificates
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def _indent(self, elem, level=0):
        """Add indentation to XML for pretty printing (compatible with Python < 3.9)"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def _make_request(self, url):
        """Make HTTP request to NOS API"""
        try:
            req = urllib.request.Request(url, headers=self.HEADERS)
            with urllib.request.urlopen(req, context=self.ssl_context) as response:
                return json.loads(response.read())
        except Exception as e:
            logger.error(f'Request failed for {url}: {e}')
            return None

    def fetch_channels(self):
        """Fetch channels from NOS API"""
        logger.info('Fetching channels from NOS API...')
        url = f'{self.API_BASE}/channels/guest?client_id={self.CLIENT_ID}'

        channels_data = self._make_request(url)
        if not channels_data:
            logger.error('Failed to fetch channels')
            return False

        for channel in channels_data:
            channel_id = str(channel.get('ChannelId', ''))
            service_id = str(channel.get('ServiceId', ''))
            if not service_id:
                continue

            # Get channel icon filename and convert to GitHub URL
            icon_filename = ''
            images = channel.get('Images', [])
            for img in images:
                if img.get('Type') == 16:  # Channel icon type
                    nos_url = img.get('Url', '')
                    if nos_url:
                        # Extract filename from NOS internal URL
                        icon_filename = nos_url.split('/')[-1]
                    break

            # Build GitHub raw URL for icon
            icon_url = f'{self.ICON_BASE_URL}{icon_filename}' if icon_filename else f'{self.ICON_BASE_URL}placeholder.svg'

            self.channels[service_id] = {
                'id': service_id,
                'channel_id': channel_id,
                'name': channel.get('Name', ''),
                'number': channel.get('Position', 0),
                'icon': icon_url,
                'icon_filename': icon_filename,
            }

        logger.info(f'Found {len(self.channels)} channels')
        return len(self.channels) > 0

    def fetch_schedule(self):
        """Fetch EPG schedule for all channels"""
        logger.info(f'Fetching {self.days} days of schedule...')

        # Get channel IDs as comma-separated string
        channel_ids = ','.join(self.channels.keys())

        for day_offset in range(self.days):
            date = datetime.now() + timedelta(days=day_offset)
            min_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            max_date = date.replace(hour=23, minute=59, second=59, microsecond=0)

            # Format dates for API
            min_date_str = min_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            max_date_str = max_date.strftime('%Y-%m-%dT%H:%M:%SZ')

            url = (f'{self.API_BASE}/schedule/range/contents/guest?'
                   f'channels={channel_ids}&'
                   f'minDate={min_date_str}&'
                   f'maxDate={max_date_str}&'
                   f'isDateInclusive=true&'
                   f'client_id={self.CLIENT_ID}')

            logger.info(f'Fetching day {day_offset + 1}/{self.days} ({min_date.strftime("%Y-%m-%d")})')

            schedule_data = self._make_request(url)
            if not schedule_data:
                logger.warning(f'Failed to fetch schedule for day {day_offset + 1}')
                continue

            # Process programs
            for program in schedule_data:
                program_id = program.get('CoreId', '')
                if not program_id:
                    continue

                # Get channel info
                airing_channel = program.get('AiringChannel', {})
                service_id = str(airing_channel.get('ServiceId', ''))
                if service_id not in self.channels:
                    continue

                # Get program metadata
                metadata = program.get('Metadata', {})

                # Parse start and end times
                start_time = program.get('UtcDateTimeStart', '')
                end_time = program.get('UtcDateTimeEnd', '')

                if not start_time or not end_time:
                    continue

                # Get program description
                title = metadata.get('Title', 'Unknown')
                subtitle = metadata.get('SubTitle', '')
                description = metadata.get('Description', '')

                # Combine title and subtitle if available
                full_title = title
                if subtitle:
                    full_title = f'{title} - {subtitle}'

                # Build program info
                self.programs[program_id] = {
                    'channel': service_id,
                    'start': start_time,
                    'stop': end_time,
                    'title': title,
                    'subtitle': subtitle,
                    'description': description,
                    'genre': metadata.get('GenreDisplay', ''),
                    'season': metadata.get('Season'),
                    'episode': metadata.get('Episode'),
                    'year': metadata.get('ReleaseYear', ''),
                    'rating': metadata.get('RatingDisplay', ''),
                }

            logger.info(f'  Added {len([p for p in self.programs.values() if p["start"].startswith(min_date.strftime("%Y-%m-%d"))])} programs')

        logger.info(f'Total programs fetched: {len(self.programs)}')
        return True

    def generate_xmltv(self):
        """Generate XMLTV format EPG"""
        logger.info('Generating XMLTV...')

        # Create root element
        tv = Element('tv')
        tv.set('generator-info-name', 'NOS EPG Generator')
        tv.set('generator-info-url', 'https://github.com/pereiraru/meo-epg-generator')

        # Add channels
        for channel_id, channel_info in sorted(self.channels.items(), key=lambda x: x[1]['number']):
            channel = SubElement(tv, 'channel')
            channel.set('id', channel_id)

            display_name = SubElement(channel, 'display-name')
            display_name.text = channel_info['name']

            display_name_num = SubElement(channel, 'display-name')
            display_name_num.text = str(channel_info['number'])

            if channel_info['icon']:
                icon = SubElement(channel, 'icon')
                icon.set('src', channel_info['icon'])

        # Add programs
        for program_id, prog_info in sorted(self.programs.items(), key=lambda x: (x[1]['channel'], x[1]['start'])):
            programme = SubElement(tv, 'programme')

            # Convert ISO format to XMLTV format (YYYYMMDDHHmmss +0000)
            start_dt = datetime.fromisoformat(prog_info['start'].replace('Z', '+00:00'))
            stop_dt = datetime.fromisoformat(prog_info['stop'].replace('Z', '+00:00'))

            programme.set('start', start_dt.strftime('%Y%m%d%H%M%S +0000'))
            programme.set('stop', stop_dt.strftime('%Y%m%d%H%M%S +0000'))
            programme.set('channel', prog_info['channel'])

            title = SubElement(programme, 'title')
            title.set('lang', 'pt')
            title.text = prog_info['title']

            if prog_info['subtitle']:
                sub_title = SubElement(programme, 'sub-title')
                sub_title.set('lang', 'pt')
                sub_title.text = prog_info['subtitle']

            if prog_info['description']:
                desc = SubElement(programme, 'desc')
                desc.set('lang', 'pt')
                desc.text = prog_info['description']

            if prog_info['genre']:
                category = SubElement(programme, 'category')
                category.set('lang', 'pt')
                category.text = prog_info['genre']

            if prog_info['year']:
                date = SubElement(programme, 'date')
                date.text = str(prog_info['year'])

            if prog_info['season'] is not None and prog_info['episode'] is not None:
                episode_num = SubElement(programme, 'episode-num')
                episode_num.set('system', 'xmltv_ns')
                # XMLTV episode numbering: season.episode.part (all 0-indexed)
                episode_num.text = f'{prog_info["season"] - 1}.{prog_info["episode"] - 1}.'

            if prog_info['rating']:
                rating = SubElement(programme, 'rating')
                value = SubElement(rating, 'value')
                value.text = prog_info['rating']

        # Pretty print
        self._indent(tv)

        return ElementTree(tv)

    def save_xmltv(self, filename='guide.xml'):
        """Save XMLTV to file"""
        logger.info(f'Saving XMLTV to {filename}...')
        tree = self.generate_xmltv()
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        logger.info(f'Successfully saved {filename}')

    def run(self):
        """Run the EPG generator"""
        logger.info('Starting NOS EPG Generator')

        if not self.fetch_channels():
            logger.error('Failed to fetch channels')
            return False

        if not self.fetch_schedule():
            logger.error('Failed to fetch schedule')
            return False

        self.save_xmltv()
        logger.info('EPG generation complete!')
        return True


if __name__ == '__main__':
    generator = NOSEPGGenerator(days=7)
    success = generator.run()
    exit(0 if success else 1)
