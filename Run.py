import os
import time
import datetime
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

base_url = "https://indonesiaindicator.com/home"
output_dir = os.path.join(os.getcwd(), "Generated Report")
screenshots_dir = os.path.join(output_dir, "screenshots")

service_driver = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service_driver)
## driver.maximize_window()
driver.implicitly_wait(10)

os.makedirs(output_dir, exist_ok=True)
os.makedirs(screenshots_dir, exist_ok=True)

test_results = []

def take_screenshot(name_prefix):
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{name_prefix}_{ts}.png")
    try:
        driver.save_screenshot(path)
    except Exception:
        path = ""
    return path

try:
    scenario_name = "Navigate 'Who We Are'"
    print(f"\n[1/4] Running: {scenario_name}")
    try:
        driver.get(base_url)
        time.sleep(2)
        menu = driver.find_element(By.PARTIAL_LINK_TEXT, "Who We Are")
        menu.click()
        time.sleep(2)
        current_url = driver.current_url
        if "who" in current_url.lower() or "who-we-are" in current_url.lower():
            status = "PASS"
            message = "Successfully navigated to Who We Are page."
        else:
            status = "FAIL"
            message = f"Unexpected URL after click: {current_url}"
        img = take_screenshot("who_we_are")
        test_results.append({"name": scenario_name, "status": status, "message": message, "screenshot": img})
        print(f"Result: {status} - {message}")
    except Exception as e:
        img = take_screenshot("who_we_are_error")
        test_results.append({"name": scenario_name, "status": "ERROR", "message": str(e), "screenshot": img})
        print(f"Result: ERROR - {e}")

    scenario_name = "Navigate 'News'"
    print(f"\n[2/4] Running: {scenario_name}")
    try:
        driver.get(base_url)
        time.sleep(2)
        menu = driver.find_element(By.PARTIAL_LINK_TEXT, "News")
        menu.click()
        time.sleep(2)
        current_url = driver.current_url
        if "news" in current_url.lower():
            status = "PASS"
            message = "Successfully navigated to News page."
        else:
            status = "FAIL"
            message = f"Unexpected URL after click: {current_url}"
        img = take_screenshot("news")
        test_results.append({"name": scenario_name, "status": status, "message": message, "screenshot": img})
        print(f"Result: {status} - {message}")
    except Exception as e:
        img = take_screenshot("news_error")
        test_results.append({"name": scenario_name, "status": "ERROR", "message": str(e), "screenshot": img})
        print(f"Result: ERROR - {e}")

    scenario_name = "Footer Social Media Link"
    print(f"\n[3/4] Running: {scenario_name}")
    try:
        driver.get(base_url)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        social = driver.find_element(By.XPATH, "//a[contains(@href,'linkedin')]")
        driver.execute_script("arguments[0].click();", social)
        time.sleep(2)
        handles = driver.window_handles
        if len(handles) > 1:
            driver.switch_to.window(handles[-1])
            status = "PASS"
            message = f"New tab opened: {driver.current_url}"
            img = take_screenshot("social_new_tab")
            driver.close()
            driver.switch_to.window(handles[0])
        else:
            status = "PASS"
            message = "Social link clicked (no new tab opened)."
            img = take_screenshot("social_clicked")
        test_results.append({"name": scenario_name, "status": status, "message": message, "screenshot": img})
        print(f"Result: {status} - {message}")
    except Exception as e:
        img = take_screenshot("social_error")
        test_results.append({"name": scenario_name, "status": "ERROR", "message": str(e), "screenshot": img})
        print(f"Result: ERROR - {e}")


    scenario_name = "Intentional fail: Find non-existent element"
    print(f"\n[4/4] Running: {scenario_name}")
    try:
        driver.get(base_url)
        time.sleep(2)
        driver.find_element(By.ID, "this-element-does-not-exist").click()
        time.sleep(1)
        img = take_screenshot("intentional_fail_unexpected_pass")
        test_results.append({"name": scenario_name, "status": "FAIL", "message": "Element unexpectedly found and clicked", "screenshot": img})
        print("Result: FAIL - Element unexpectedly found")
    except Exception as e:
        img = take_screenshot("intentional_fail_caught")
        test_results.append({"name": scenario_name, "status": "ERROR", "message": str(e), "screenshot": img})
        print(f"Result: ERROR - {e}")

finally:
    print("\n[Tests finished. Closing browser...]")
    driver.quit()

print("Generating HTML test report...")
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
report_file = os.path.join(output_dir, f"Test_Report_{timestamp}.html")

html_head = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Automated Test Report</title>
<style>
body{{font-family:Arial, Arial, sans-serif;padding:20px;background:#f4f4f4}}
table{{border-collapse:collapse;width:100%;background:#ecedf0}}
th,td{{border:1px solid #ddd;padding:8px;text-align:left}}
th{{background:#9c2832;color:#ecedf0}}
img{{width:120px;border:1px solid #ccc;cursor:pointer}}
.PASS{{color:green;font-weight:bold}}
.FAIL{{color:red;font-weight:bold}}
.ERROR{{color:orange;font-weight:bold}}
</style>
</head><body>
<h2>Test Report</h2>
<p>Target: {base_url} | Generated: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} using Selenium</p>
<table>
<tr><th>Scenario</th><th>Status</th><th>Message</th><th>Screenshot</th></tr>
"""

rows = []
for r in test_results:
    img_html = ""
    path = r.get("screenshot") or ""
    if path and os.path.exists(path):
        try:
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                img_html = f'<img src="data:image/png;base64,{b64}" alt="screenshot">'
        except Exception:
            img_html = "Image load error"
    rows.append(f"<tr><td>{r['name']}</td><td class='{r['status']}'>{r['status']}</td><td>{r['message']}</td><td>{img_html}</td></tr>")

html_tail = "</table></body></html>"

with open(report_file, "w", encoding="utf-8") as f:
    f.write(html_head + "\n".join(rows) + html_tail)

failed = [r for r in test_results if r['status'] in ('FAIL', 'ERROR')]
print(f"\nTotal tests: {len(test_results)} | Failed/Error: {len(failed)}")
print(f"Report created: {report_file}")