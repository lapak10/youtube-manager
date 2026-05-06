#!/usr/bin/env python3
"""Run this once the API quota resets (midnight Pacific / ~12:30 PM IST)."""
import sys
sys.path.insert(0, '.')
from youtube_manager import YouTubeClient

client = YouTubeClient()

# Playlist IDs (already created)
SAIYAARA_PID = 'PL5CBMWWc-cmRMYBvB58NtNg6OLfwJCo84'
MENVSWOMEN_PID = 'PL5CBMWWc-cmQNlPkalzPSpp-5_HGlHPWw'

# Saiyaara videos
saiyaara_ids = [
    'hy47OdKzm8A', 'uIJby5PN9Og', 'Y0zrOdRg-9o',
    '4Ln322Xk-no', 'BoA08o-dMek', 'KHg5e2qWKsk', 'sKY8e4-SDQg',
]

# Men vs Women videos
menvswomen_ids = [
    'lX9ziSD4iKs', '0Vf9lm2qgF8', '-ZTU3ieg2rY',
    '1CGxheq7xd4', 'wzQS44kKI70', 'zroVlRKZXmo',
    'tufCrz_aUKM', '_WXmC6lvpDk', 'wHANoJm6-VQ',
    'voikJf_gZR0', 'ZGYNNo2U-tc',
]

for pid, name, ids in [
    (SAIYAARA_PID, 'Saiyaara Movie Roast', saiyaara_ids),
    (MENVSWOMEN_PID, 'Men vs Women', menvswomen_ids),
]:
    for vid in ids:
        try:
            client.add_to_playlist(pid, vid)
            print(f'  Added {vid} to {name}')
        except Exception as e:
            print(f'  Error {vid}: {e}')

print('\nDone!')
