import requests
import json

CRYPTO_URL = "https://api.coingecko.com/api/v3/coins/markets"
WEATHER_URL = "https://wttr.in/{}?format=j1"

def get_weather():
    city = input("Enter city name for weather: ").strip()
    try:
        response = requests.get(WEATHER_URL.format(city), timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data["current_condition"][0]
        desc = current["weatherDesc"][0]["value"]
        temp_c = current["temp_C"]
        feels = current["FeelsLikeC"]
        humidity = current["humidity"]
        print(f"\n--- Weather in {city.upper()} ---")
        print(f"  Condition  : {desc}")
        print(f"  Temperature: {temp_c}°C")
        print(f"  Feels Like : {feels}°C")
        print(f"  Humidity   : {humidity}%")
    except requests.exceptions.ConnectionError:
        print("Network error. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except (KeyError, json.JSONDecodeError):
        print("Could not parse weather data. Try a different city name.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def get_crypto():
    search = input("Enter crypto name to search (e.g. bitcoin, ethereum): ").strip().lower()
    try:
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": False
        }
        response = requests.get(CRYPTO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = [coin for coin in data if search in coin["name"].lower() or search in coin["symbol"].lower()]
        if not results:
            print(f"\nNo crypto found matching '{search}'.")
        else:
            print(f"\n--- Crypto Results for '{search}' ---")
            for coin in results[:5]:
                print(f"\n  Name         : {coin['name']} ({coin['symbol'].upper()})")
                print(f"  Price (USD)  : ${coin['current_price']:,.4f}")
                print(f"  Market Cap   : ${coin['market_cap']:,.0f}")
                print(f"  24h Change   : {coin['price_change_percentage_24h']:.2f}%")
                print(f"  24h High     : ${coin['high_24h']:,.4f}")
                print(f"  24h Low      : ${coin['low_24h']:,.4f}")
    except requests.exceptions.ConnectionError:
        print("Network error. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except (KeyError, json.JSONDecodeError):
        print("Could not parse crypto data.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def get_news():
    keyword = input("Enter keyword to search news (e.g. technology, sports): ").strip()
    try:
        url = f"https://api.currentsapi.services/v1/search?keywords={keyword}&language=en&apiKey=demo"
        response = requests.get(
            f"https://gnews.io/api/v4/search?q={keyword}&lang=en&max=5&token=demo",
            timeout=10
        )
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            print(f"\nNo news articles found for '{keyword}'.")
            print("(Note: A valid GNews API key is needed for full results. Get one free at https://gnews.io)")
        else:
            print(f"\n--- News Results for '{keyword}' ---")
            for i, article in enumerate(articles, 1):
                print(f"\n  [{i}] {article.get('title', 'No title')}")
                print(f"      Source : {article.get('source', {}).get('name', 'Unknown')}")
                print(f"      URL    : {article.get('url', 'N/A')}")
    except requests.exceptions.ConnectionError:
        print("Network error. Check your internet connection.")
    except Exception as e:
        print(f"Could not fetch news: {e}")
        print("Tip: Get a free API key at https://gnews.io and replace 'demo' in the script.")

def show_menu():
    print("\n" + "=" * 40)
    print("     API INTEGRATION TOOL")
    print("=" * 40)
    print("  1. Weather Info")
    print("  2. Crypto Prices")
    print("  3. Latest News")
    print("  4. Exit")
    print("=" * 40)

while True:
    show_menu()
    choice = input("Select an option (1-4): ").strip()
    if choice == "1":
        get_weather()
    elif choice == "2":
        get_crypto()
    elif choice == "3":
        get_news()
    elif choice == "4":
        print("\nGoodbye!")
        break
    else:
        print("Invalid choice. Please enter 1 to 4.")
