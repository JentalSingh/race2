import os
import time
import random
import string
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def generate_random_string(length=7):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_super_strong_password():
    lower = ''.join(random.choices(string.ascii_lowercase, k=3))
    upper = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=3))
    special = ''.join(random.choices("@#$!", k=2))
    password_list = list(lower + upper + digits + special)
    random.shuffle(password_list)
    return ''.join(password_list)

def get_random_proxy():
    proxy_candidates = ['Webshare proxies', 'Webshare proxies.txt', 'proxies.txt']
    for candidate in proxy_candidates:
        if os.path.exists(candidate):
            with open(candidate, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
                if proxies:
                    selected_proxy = random.choice(proxies)
                    print(f"📡 [PROXY]: Layer enabled -> '{selected_proxy}'")
                    tokens = selected_proxy.split(':')
                    if len(tokens) == 2:
                        return {"server": f"http://{tokens[0]}:{tokens[1]}"}
                    elif len(tokens) == 4:
                        return {
                            "server": f"http://{tokens[0]}:{tokens[1]}",
                            "username": tokens[2],
                            "password": tokens[3]
                        }
    return None

def solve_recaptcha_via_api(site_key, page_url):
    api_key = os.getenv("TWOCAPTCHA_API_KEY")
    if not api_key:
        print("[CAPTCHA_API]: ERROR - API Key missing inside .env!")
        return None
        
    submit_url = f"https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={site_key}&pageurl={page_url}&json=1"
    try:
        response = requests.get(submit_url).json()
    except Exception as e:
        print(f"[CAPTCHA_API]: Network error: {str(e)}")
        return None
        
    if response.get("status") != 1:
        print(f"[CAPTCHA_API]: API Error -> {response.get('request')}")
        return None
        
    request_id = response.get("request")
    poll_url = f"https://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"
    
    print("[CAPTCHA_API]: Resolving captcha grids...")
    while True:
        time.sleep(5)
        try:
            result = requests.get(poll_url).json()
        except Exception:
            continue
            
        if result.get("status") == 1:
            print("[CAPTCHA_API]: Verification cleared.")
            return result.get("request")
        elif result.get("request") == "CAPCHA_NOT_READY":
            continue
        else:
            print(f"[CAPTCHA_API]: Failed -> {result.get('request')}")
            return None

def execute_race_equality_signup():
    company_name = f"{generate_random_string(6).capitalize()} Ltd"
    email = f"employer.{generate_random_string(5)}.{random.randint(100, 999)}@gmail.com"
    password = generate_super_strong_password()
    target_url = "https://raceequalitymatters.com/jobs/employer-registration/"
    logo_filename = "sample_resume.pdf" 

    proxy_server = get_random_proxy()

    with sync_playwright() as p:
        print("[RACE_EQUALITY]: Initializing Human-Like Architecture...")
        
        browser_arguments = [
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--no-sandbox",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process"
        ]
        
        config = {"headless": False, "args": browser_arguments}
        if proxy_server:
            config["proxy"] = proxy_server

        browser = p.chromium.launch(**config)
        
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
        """)

        print("[RACE_EQUALITY]: Navigating to portal URL...")
        page.goto(target_url, timeout=90000, wait_until="networkidle")
        
        print("[RACE_EQUALITY]: Waiting for security handshake...")
        time.sleep(12)

        # Cookie Consent Clear
        try:
            cookie_btn = page.locator("button.cky-btn-accept, button[data-cky-tag='accept-button']").first
            if cookie_btn.count() > 0:
                cookie_btn.click()
                time.sleep(2)
        except:
            pass

        print("[RACE_EQUALITY]: Filling credentials profile fields...")
        
        password_field = page.locator("#user_password").first
        password_field.wait_for(state="visible", timeout=20000)
        password_field.type(password, delay=random.randint(60, 120))

        confirm_password_field = page.locator("#user_password2").first
        confirm_password_field.type(password, delay=random.randint(60, 120))

        company_email_field = page.locator("#user_email").first
        company_email_field.type(email, delay=random.randint(50, 100))

        company_name_field = page.locator("#company_name").first
        company_name_field.type(company_name, delay=random.randint(50, 100))
        time.sleep(2)

        # कंपनी लोगो फ़ाइल अपलोड
        print("[RACE_EQUALITY]: Attaching company logo assets...")
        file_input = page.locator("input[type='file']").first
        if file_input.count() > 0:
            if os.path.exists(logo_filename):
                file_input.set_input_files(logo_filename)
                print(f"✅ Asset attached successfully.")
                time.sleep(3)
            else:
                print(f"⚠️ Local asset file missing.")

        # 🎯 रिच टेक्स्ट एडिटर फिक्स (आपके स्क्रीनशॉट स्क्रिप्ट के आधार पर)
        print("[RACE_EQUALITY]: Injecting content inside TinyMCE Rich Text Editor Frame...")
        try:
            # कंपनी इन्फो या डिस्क्रिप्शन iframe आईडी का पता लगाना (Rem साइट पर 'company_info_ifr' या 'description_ifr' होता है)
            page.evaluate("""
                () => {
                    const iframe = document.getElementById('company_info_ifr') || document.getElementById('description_ifr') || document.querySelector('iframe[id*="content_ifr"]');
                    if (iframe) {
                        const doc = iframe.contentDocument || iframe.contentWindow.document;
                        if (doc && doc.body) {
                            // HTML कंटेंट सेट करना जैसा स्क्रीनशॉट में था
                            doc.body.innerHTML = '<p>We provide professional guidance.</p>';
                            // साइट के आंतरिक बदलावों को ट्रिगर करने के लिए इवेंट डिस्पैच करना
                            doc.body.dispatchEvent(new Event('change', { bubbles: true }));
                            doc.body.dispatchEvent(new Event('input', { bubbles: true }));
                            return true;
                        }
                    }
                    return false;
                }
            """)
            print("✅ Description text injected smoothly via Frame JS execution.")
            time.sleep(2)
        except Exception as iframe_err:
            print(f"⚠️ Rich Text Frame Error: {str(iframe_err)}")

        region_dropdown = page.locator("select[name*='region'], select[id*='region']").first
        if region_dropdown.count() > 0:
            region_dropdown.select_option(label="South West")
            time.sleep(2)

        # Captcha Extraction & Advanced Injection
        captcha_iframe = page.locator("iframe[src*='recaptcha/api2/anchor']").first
        if captcha_iframe.count() > 0:
            src_attr = captcha_iframe.get_attribute("src")
            site_key = src_attr.split("k=")[1].split("&")[0]
            token = solve_recaptcha_via_api(site_key, target_url)
            
            if token:
                print("[RACE_EQUALITY]: Finalizing captcha token mapping...")
                page.evaluate("""
                    (tokenValue) => {
                        const textarea = document.getElementById("g-recaptcha-response");
                        if (textarea) {
                            textarea.innerHTML = tokenValue;
                            textarea.value = tokenValue;
                            textarea.dispatchEvent(new Event('change', { bubbles: true }));
                            textarea.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    }
                """, token)
                time.sleep(4)

        print("[RACE_EQUALITY]: Submitting the finalized form data...")
        register_button = page.locator("input[type='submit'][value='Register'], #wpjb_submit").first
        register_button.scroll_into_view_if_needed()
        time.sleep(2)
        
        register_button.hover()
        time.sleep(1)
        register_button.click(delay=random.randint(200, 400))

        print("[RACE_EQUALITY]: Analyzing landing redirection...")
        
        success_confirmed = False
        final_url = ""
        
        for i in range(30):
            time.sleep(1)
            final_url = page.url
            page_text = page.locator("body").inner_text().lower()
            
            if "dashboard" in final_url.lower() or "employer-dashboard" in final_url.lower():
                success_confirmed = True
                break
            if "registration successful" in page_text or "thank you for registering" in page_text or "response has been recorded" in page_text:
                success_confirmed = True
                break

        final_url = page.url
        print(f"[RACE_EQUALITY]: Landing Node -> {final_url}")
        
        if success_confirmed:
            print("\n" + "="*70)
            print("🚀 🎉 [SUCCESS]: ACCOUNT CREATED & VERIFIED! 🎉 🚀")
            print("="*70)
            print(f"  Login Email    : {email}")
            print(f"  Login Password : {password}")
            print("="*70 + "\n")
            
            env_file_path = os.path.join(os.getcwd(), '.env')
            lines = []
            if os.path.exists(env_file_path):
                with open(env_file_path, 'r') as f:
                    lines = f.readlines()
            
            new_lines = [line for line in lines if not line.startswith("LAST_REGISTERED_EMAIL") and not line.startswith("LAST_REGISTERED_PASSWORD")]
            new_lines.append(f"LAST_REGISTERED_EMAIL={email}\n")
            new_lines.append(f"LAST_REGISTERED_PASSWORD={password}\n")
            
            with open(env_file_path, 'w') as f:
                f.writelines(new_lines)
        else:
            print(f"\n❌ [ERROR]: Session verification failed or text mismatched.")
            page.screenshot(path="submission_debug.png")

        browser.close()

if __name__ == "__main__":
    execute_race_equality_signup()