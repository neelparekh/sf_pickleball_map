"""
Simple API discovery using requests and analyzing the loaded JavaScript bundles.

Since we can't easily use Playwright, let's analyze the Next.js bundles to find API endpoints.
"""

import requests
import json
import re
import warnings
from urllib.parse import urlparse, urljoin

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def extract_api_patterns_from_js(js_content):
    """Extract potential API endpoints from JavaScript code."""
    
    patterns = []
    
    # Look for URL patterns
    url_patterns = [
        r'["\']https?://[^"\']+/api/[^"\']+["\']',  # Full URLs with /api/
        r'["\'](/api/[^"\']+)["\']',  # Relative /api/ URLs
        r'["\']https?://api\.[^"\']+["\']',  # api. subdomain
        r'fetch\(["\']([^"\']+)["\']',  # fetch() calls
        r'axios\.[^(]+\(["\']([^"\']+)["\']',  # axios calls
        r'\.get\(["\']([^"\']+)["\']',  # .get() calls
        r'\.post\(["\']([^"\']+)["\']',  # .post() calls
    ]
    
    for pattern in url_patterns:
        matches = re.findall(pattern, js_content)
        patterns.extend(matches)
    
    # Look for location/availability related endpoints
    keywords = ['location', 'availability', 'schedule', 'slot', 'booking', 'calendar', 'reservation']
    for keyword in keywords:
        keyword_patterns = re.findall(rf'["\']([^"\']*{keyword}[^"\']*)["\']', js_content, re.IGNORECASE)
        patterns.extend([p for p in keyword_patterns if '/' in p and len(p) > 5])
    
    return list(set(patterns))  # Remove duplicates


def analyze_rec_us_structure():
    """Analyze rec.us page structure and extract API information."""
    
    print("\n" + "="*70)
    print("REC.US API DISCOVERY - JAVASCRIPT ANALYSIS")
    print("="*70 + "\n")
    
    base_url = "https://www.rec.us/buenavista"
    
    # Fetch the main page
    print(f"📄 Fetching: {base_url}")
    response = requests.get(base_url, verify=False)
    html = response.text
    
    # Extract Next.js data
    next_data_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
    if next_data_match:
        next_data = json.loads(next_data_match.group(1))
        location_id = next_data.get('query', {}).get('locationId')
        build_id = next_data.get('buildId')
        
        print(f"✓ Location ID: {location_id}")
        print(f"✓ Build ID: {build_id}\n")
    else:
        print("✗ Could not find __NEXT_DATA__\n")
        return
    
    # Find all script sources
    script_urls = re.findall(r'<script[^>]+src="([^"]+)"', html)
    print(f"📦 Found {len(script_urls)} JavaScript files\n")
    
    all_api_patterns = set()
    
    # Analyze each script
    for i, script_url in enumerate(script_urls[:10], 1):  # Limit to first 10 to save time
        if not script_url.startswith('http'):
            script_url = urljoin(base_url, script_url)
        
        print(f"{i}. Analyzing: {script_url.split('/')[-1][:50]}...")
        
        try:
            script_response = requests.get(script_url, verify=False, timeout=5)
            patterns = extract_api_patterns_from_js(script_response.text)
            
            if patterns:
                print(f"   ✓ Found {len(patterns)} potential API patterns")
                for p in patterns[:5]:  # Show first 5
                    print(f"     - {p}")
                if len(patterns) > 5:
                    print(f"     ... and {len(patterns) - 5} more")
                all_api_patterns.update(patterns)
            else:
                print(f"   - No API patterns found")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        print()
    
    # Try common Next.js API patterns
    print("="*70)
    print("TESTING COMMON NEXT.JS API PATTERNS")
    print("="*70 + "\n")
    
    test_patterns = [
        f"/api/locations/{location_id}",
        f"/api/locations/{location_id}/availability",
        f"/api/locations/{location_id}/schedule",
        f"/api/locations/{location_id}/slots",
        f"/api/availability?locationId={location_id}",
        f"/_next/data/{build_id}/locations/{location_id}.json",
        f"/locations/{location_id}/availability",
        f"/v1/locations/{location_id}/availability",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': base_url
    }
    
    working_apis = []
    
    for pattern in test_patterns:
        url = urljoin(base_url, pattern)
        print(f"Testing: {url}")
        
        try:
            resp = requests.get(url, headers=headers, verify=False, timeout=5)
            print(f"  Status: {resp.status_code}")
            
            if resp.status_code == 200:
                print(f"  ✓ SUCCESS!")
                try:
                    data = resp.json()
                    print(f"  Response preview: {str(data)[:200]}...")
                    working_apis.append({
                        'url': url,
                        'status': resp.status_code,
                        'response': data
                    })
                except:
                    print(f"  Response (not JSON): {resp.text[:200]}...")
            elif resp.status_code == 404:
                print(f"  ✗ Not found")
            elif resp.status_code in [401, 403]:
                print(f"  ⚠ Auth required")
            else:
                print(f"  ? Status {resp.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70 + "\n")
    
    if working_apis:
        print(f"✓ Found {len(working_apis)} working API endpoints!\n")
        for api in working_apis:
            print(f"  {api['url']}")
            print(f"  Status: {api['status']}")
            print()
        
        # Save results
        with open('backend/api_discovery_results.json', 'w') as f:
            json.dump({
                'location_id': location_id,
                'working_apis': working_apis,
                'all_patterns': list(all_api_patterns)
            }, f, indent=2)
        
        print("✓ Results saved to: backend/api_discovery_results.json\n")
    else:
        print("⚠️  No working API endpoints found through automated testing.\n")
        print("Possible reasons:")
        print("1. API requires authentication/session cookies")
        print("2. API uses non-standard endpoints")
        print("3. Data is rendered client-side from embedded JSON")
        print("4. Data is loaded via WebSocket or GraphQL\n")
        
        print("RECOMMENDATION:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Manual browser inspection needed:")
        print("1. Open https://www.rec.us/buenavista in Chrome")
        print("2. Open DevTools (F12) > Network tab")
        print("3. Filter by 'Fetch/XHR'")
        print("4. Interact with calendar/date picker")
        print("5. Look for requests with 'availability', 'schedule', 'slot'")
        print("6. Document the endpoint URL, method, and required headers\n")
    
    if all_api_patterns:
        print(f"\n📝 Found {len(all_api_patterns)} API-related patterns in JavaScript")
        print("    (Saved to results file for further analysis)\n")


if __name__ == "__main__":
    analyze_rec_us_structure()
