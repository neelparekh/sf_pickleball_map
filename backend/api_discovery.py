"""
Network request interceptor for rec.us

Uses Playwright to load the page with JavaScript enabled and capture all API calls.
"""

import asyncio
import json
from playwright.async_api import async_playwright
import re


async def intercept_rec_us_requests(court_url):
    """
    Load rec.us page and intercept all network requests to find API endpoints.
    
    Args:
        court_url: URL like https://www.rec.us/buenavista
    """
    
    print(f"\n{'='*70}")
    print(f"INTERCEPTING NETWORK REQUESTS FROM: {court_url}")
    print(f"{'='*70}\n")
    
    captured_requests = []
    api_requests = []
    
    async def handle_request(request):
        """Capture all network requests."""
        url = request.url
        method = request.method
        resource_type = request.resource_type
        
        # Store all requests
        captured_requests.append({
            'url': url,
            'method': method,
            'type': resource_type,
            'headers': dict(request.headers) if request.headers else {}
        })
        
        # Flag potential API requests
        if any(pattern in url.lower() for pattern in [
            '/api/', '/graphql', '/v1/', '/v2/', '/availability', 
            '/schedule', '/booking', '/slots', '/calendar', '/locations'
        ]):
            api_requests.append({
                'url': url,
                'method': method,
                'type': resource_type,
                'headers': dict(request.headers) if request.headers else {}
            })
            print(f"🎯 API REQUEST: {method} {url}")
    
    async def handle_response(response):
        """Capture API responses."""
        url = response.url
        
        # Check if this is an API response
        if any(pattern in url.lower() for pattern in [
            '/api/', '/graphql', '/availability', '/schedule', '/slots'
        ]):
            try:
                # Try to get response body
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    body = await response.json()
                    print(f"📦 RESPONSE: {response.status} {url}")
                    print(f"   Preview: {str(body)[:200]}...\n")
                    
                    # Store response
                    for req in api_requests:
                        if req['url'] == url and 'response' not in req:
                            req['response'] = {
                                'status': response.status,
                                'body': body,
                                'headers': dict(response.headers)
                            }
                            break
            except Exception as e:
                print(f"   Could not parse response: {e}")
    
    try:
        async with async_playwright() as p:
            # Launch browser
            print("🌐 Launching browser...")
            browser = await p.chromium.launch(
                headless=True,
                args=['--ignore-certificate-errors']
            )
            
            # Create context and page
            context = await browser.new_context(
                ignore_https_errors=True,
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            
            # Set up request/response interception
            page.on('request', handle_request)
            page.on('response', handle_response)
            
            print(f"📄 Loading page: {court_url}")
            
            # Navigate to the page
            await page.goto(court_url, wait_until='networkidle', timeout=30000)
            
            print("✓ Page loaded, waiting for dynamic content...\n")
            
            # Wait a bit for any delayed requests
            await asyncio.sleep(3)
            
            # Try to interact with calendar/date selectors
            print("🖱️  Attempting to interact with page elements...")
            
            # Look for common calendar/date picker selectors
            selectors_to_try = [
                'button:has-text("Next")',
                'button:has-text("Calendar")',
                'input[type="date"]',
                '[class*="calendar"]',
                '[class*="date"]',
                '[data-testid*="calendar"]',
                '[role="button"]',
            ]
            
            for selector in selectors_to_try:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        print(f"   Found element: {selector}")
                        await element.click()
                        await asyncio.sleep(1)
                        break
                except:
                    pass
            
            # Wait for any additional requests
            await asyncio.sleep(2)
            
            # Take a screenshot for debugging
            await page.screenshot(path='backend/rec_us_screenshot.png')
            print("📸 Screenshot saved to: backend/rec_us_screenshot.png")
            
            # Close browser
            await browser.close()
            
    except Exception as e:
        print(f"❌ Error during browser automation: {e}")
        import traceback
        traceback.print_exc()
    
    # Analyze results
    print(f"\n{'='*70}")
    print("ANALYSIS")
    print(f"{'='*70}\n")
    
    print(f"Total requests captured: {len(captured_requests)}")
    print(f"Potential API requests: {len(api_requests)}\n")
    
    if api_requests:
        print("🎯 API ENDPOINTS DISCOVERED:\n")
        for i, req in enumerate(api_requests, 1):
            print(f"{i}. {req['method']} {req['url']}")
            if 'response' in req:
                print(f"   Status: {req['response']['status']}")
                print(f"   Preview: {str(req['response']['body'])[:150]}...")
            print()
    else:
        print("⚠️  No obvious API requests found.\n")
        print("Checking all requests for patterns...")
        
        # Look for any requests that might be data-related
        for req in captured_requests:
            url = req['url']
            if req['type'] == 'fetch' or req['type'] == 'xhr':
                print(f"   XHR/Fetch: {req['method']} {url}")
    
    # Save full results
    results = {
        'court_url': court_url,
        'total_requests': len(captured_requests),
        'api_requests': api_requests,
        'all_requests': captured_requests
    }
    
    with open('backend/api_discovery_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Full results saved to: backend/api_discovery_results.json")
    
    return api_requests


async def test_discovered_apis(api_requests):
    """
    Test if we can call the discovered APIs directly without a browser.
    """
    if not api_requests:
        print("\nNo APIs to test.")
        return
    
    print(f"\n{'='*70}")
    print("TESTING API ENDPOINTS DIRECTLY")
    print(f"{'='*70}\n")
    
    import requests
    
    for i, req in enumerate(api_requests, 1):
        url = req['url']
        method = req['method']
        headers = req.get('headers', {})
        
        print(f"{i}. Testing: {method} {url}")
        
        try:
            # Use the same headers from browser
            filtered_headers = {
                k: v for k, v in headers.items()
                if k.lower() in ['authorization', 'accept', 'content-type', 'user-agent']
            }
            
            if method == 'GET':
                response = requests.get(url, headers=filtered_headers, timeout=5, verify=False)
            elif method == 'POST':
                response = requests.post(url, headers=filtered_headers, timeout=5, verify=False)
            else:
                print(f"   Skipping {method} method")
                continue
            
            print(f"   ✓ Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✓ Got JSON response!")
                    print(f"   Preview: {str(data)[:200]}...")
                except:
                    print(f"   Response (first 200 chars): {response.text[:200]}")
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print()


async def main():
    """Run the API discovery process."""
    
    print("\n" + "="*70)
    print("REC.US API ENDPOINT DISCOVERY")
    print("="*70)
    
    # Test with Buena Vista Park
    court_url = "https://www.rec.us/buenavista"
    
    # Intercept requests
    api_requests = await intercept_rec_us_requests(court_url)
    
    # Test discovered APIs
    await test_discovered_apis(api_requests)
    
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\n1. Review backend/api_discovery_results.json")
    print("2. Review backend/rec_us_screenshot.png")
    print("3. If APIs found, implement scraper using those endpoints")
    print("4. If no APIs found, may need to scrape rendered page content\n")


if __name__ == "__main__":
    asyncio.run(main())
