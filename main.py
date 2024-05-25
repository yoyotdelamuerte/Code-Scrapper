import tkinter as tk
from tkinter import scrolledtext, ttk
from bs4 import BeautifulSoup
import requests
import os


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        return html_content, None
    except requests.exceptions.RequestException as e:
        return None, f"Erreur lors de la récupération de la page : {e}"


def save_to_file(content, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)
        file_size = os.path.getsize(file_name) / (1024 * 1024)
        return f"success: {file_name} ({file_size:.2f} Mo)"
    except Exception as e:
        return f"error: {file_name} - {e}"


def extract_and_save_css(soup, base_url, file_name):
    styles = []
    for style in soup.find_all('style'):
        styles.append(style.get_text())
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            if href.startswith(('http://', 'https://')):
                css_url = href
            else:
                css_url = os.path.join(base_url, href)
            try:
                response = requests.get(css_url)
                response.raise_for_status()
                styles.append(response.text)
            except requests.exceptions.RequestException as e:
                return f"Erreur lors de la récupération du fichier CSS : {e}"
    css_content = "\n".join(styles)
    return save_to_file(css_content, file_name)


def process_url():
    url = url_entry.get()
    html_content, error = get_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        html_message = save_to_file(soup.prettify(), "output.html")
        txt_message = save_to_file(soup.prettify(), "output.txt")
        css_message = extract_and_save_css(soup, url, "styles.scss")
        message = f"{html_message}\n{txt_message}\n{css_message}"
    else:
        message = error
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, message)


window = tk.Tk()
window.title("Web Scraper")

tk.Label(window, text="URL du site web:").grid(row=0, column=0, padx=5, pady=5)
url_entry = tk.Entry(window, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)
scrape_button = tk.Button(window, text="Recuperate and save", command=process_url)
scrape_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
output_text = scrolledtext.ScrolledText(window, width=60, height=10)
output_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()
