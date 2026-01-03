# EPG Setup for UHF App

## EPG URL
Use this URL in your UHF App EPG settings:

```
https://raw.githubusercontent.com/pereiraru/meo-epg-generator/main/guide.xml
```

Or for the compressed version (recommended):
```
https://raw.githubusercontent.com/pereiraru/meo-epg-generator/main/guide.xml.gz
```

## File Information
- **Format**: XMLTV
- **Channels**: 163 NOS Portugal TV channels
- **Programs**: ~35,000 programs across 7 days
- **File Size**: 
  - Uncompressed: 18 MB
  - Compressed (.gz): 1.8 MB
- **Update Frequency**: Daily at 2:00 AM UTC (via GitHub Actions)

## EPG Data
- Source: NOS Portugal API
- Days of EPG: 7 days (today + 6 days ahead)
- Updated automatically every day
- Includes: titles, descriptions, genres, episode info, ratings

## Troubleshooting

### Download Failed Error
If you get "download failed" in UHF:

1. **Try the compressed URL** - some apps have size limits
2. **Check your internet connection** - file is 18MB uncompressed
3. **Verify URL format** - make sure you're using the raw.githubusercontent.com URL
4. **Wait for cache** - GitHub caches files for 5 minutes, try again after a few minutes
5. **Check app settings** - some apps need specific URL patterns or file extensions

### Alternative URLs
If the raw URL doesn't work, try:
- `https://github.com/pereiraru/meo-epg-generator/raw/main/guide.xml`
- `https://github.com/pereiraru/meo-epg-generator/raw/main/guide.xml.gz`

### Manual Download
You can manually download and inspect the file:
```bash
curl -o guide.xml https://raw.githubusercontent.com/pereiraru/meo-epg-generator/main/guide.xml
```

### Validate XML
To verify the XML is valid:
```bash
xmllint --noout guide.xml
```
