import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import textwrap

# Set Charter as the default font (with fallbacks)
# Try common Charter variants; falls back to serif if unavailable
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Charter', 'Bitstream Charter', 'XCharter', 'Georgia', 'DejaVu Serif']
plt.rcParams['font.size'] = 10

def load_and_process_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    data = []
    for line in lines:
        if '\t' not in line or 'Countries/Regions' in line:
            continue
        
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            country = parts[0].strip()
            count = float(parts[1].strip())
            data.append((country, count))
    
    df = pd.DataFrame(data, columns=['Country', 'Citations'])
    
    country_mappings = {
        'PEOPLES R CHINA': 'China',
        'CHINA': 'China',
        'USA': 'United States',
        'UNITED STATES': 'United States',
        'UK': 'United Kingdom',
        'ENGLAND': 'United Kingdom',
        'GERMANY': 'Germany',
        'CANADA': 'Canada',
        'ITALY': 'Italy',
        'JAPAN': 'Japan',
        'SPAIN': 'Spain',
        'AUSTRALIA': 'Australia',
        'FRANCE': 'France',
        'RUSSIA': 'Russia',
        'SINGAPORE': 'Singapore',
        'SOUTH KOREA': 'South Korea',
        'AUSTRIA': 'Austria',
        'NETHERLANDS': 'Netherlands',
        'SWITZERLAND': 'Switzerland',
        'SWEDEN': 'Sweden',
        'DENMARK': 'Denmark',
        'POLAND': 'Poland',
        'BRAZIL': 'Brazil',
        'ISRAEL': 'Israel',
        'INDIA': 'India',
        'TAIWAN': 'Taiwan',
        'SAUDI ARABIA': 'Saudi Arabia',
        'IRAN': 'Iran'
    }
    
    df['Country'] = df['Country'].replace(country_mappings)
    df = df.groupby('Country')['Citations'].sum().reset_index()
    df = df.sort_values('Citations', ascending=False).head(10)
    
    return df

def get_country_flag(country_name):
    country_codes = {
        'China': 'cn',
        'United States': 'us',
        'Germany': 'de',
        'United Kingdom': 'gb',
        'Canada': 'ca',
        'Italy': 'it',
        'Japan': 'jp',
        'Spain': 'es',
        'Australia': 'au',
        'France': 'fr',
        'Russia': 'ru',
        'Singapore': 'sg',
        'South Korea': 'kr',
        'Austria': 'at',
        'Netherlands': 'nl',
        'Switzerland': 'ch',
        'Sweden': 'se',
        'Denmark': 'dk',
        'Poland': 'pl',
        'Brazil': 'br',
        'Israel': 'il',
        'India': 'in',
        'Taiwan': 'tw',
        'Saudi Arabia': 'sa',
        'Iran': 'ir',
    }
    
    code = country_codes.get(country_name)
    if not code:
        return None
    
    urls = [
        f'https://flagsapi.com/{code.upper()}/flat/64.png',
        f'https://flagcdn.com/w80/{code.lower()}.png',
        f'https://raw.githubusercontent.com/hampusborgos/country-flags/main/png250px/{code.lower()}.png'
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                return img
        except:
            continue
    
    print(f"Could not load flag for {country_name}")
    return None

def create_plot(df, title):
    fig, ax = plt.subplots(figsize=(10, 7))
    
    bar_color = '#2AF4FE'
    edge_color = '#1AC8D0'
    
    bars = ax.bar(
        range(len(df)), 
        df['Citations'], 
        color=bar_color,
        edgecolor=edge_color,
        linewidth=1.5,
        alpha=0.75,
        width=0.7
    )
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#666666')
    ax.spines['bottom'].set_color('#666666')
    
    ax.yaxis.grid(True, linestyle='-', alpha=0.2, color='#666666')
    ax.set_axisbelow(True)
    
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df['Country'], rotation=45, ha='right', fontsize=10)
    
    wrapped_title = '\n'.join(textwrap.wrap(title, width=70))
    ax.set_title(wrapped_title, pad=15, fontsize=11, fontweight='medium')
    
    ax.set_ylabel('Citations', fontsize=10)
    ax.tick_params(axis='y', labelsize=9)
    
    ymax = max(df['Citations']) * 1.18
    ax.set_ylim(0, ymax)
    
    flag_size = 0.065
    vertical_offset = ymax * 0.02
    
    for idx, (bar, (_, row)) in enumerate(zip(bars, df.iterrows())):
        flag = get_country_flag(row['Country'])
        if flag:
            flag = flag.convert('RGB')
            flag_array = np.array(flag)
            
            x_pos = idx
            y_pos = bar.get_height() + vertical_offset
            
            data_width = np.diff(ax.get_xlim())[0] * flag_size
            data_height = np.diff(ax.get_ylim())[0] * flag_size
            
            flag_ax = ax.inset_axes([
                x_pos - data_width/2,
                y_pos,
                data_width,
                data_height
            ], transform=ax.transData)
            
            flag_ax.imshow(flag_array)
            flag_ax.axis('off')
    
    fig.text(0.02, 0.02, 'Markus Leipe (2025)', fontsize=8, color='#666666')
    fig.text(0.98, 0.02, 'Data source: Web of Science', 
             fontsize=8, ha='right', color='#666666')
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.18, top=0.90)
    
    return fig

def main():
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="Select Web of Science data file",
        filetypes=[("Text files", "*.txt")]
    )
    
    if not file_path:
        print("No file selected")
        return
    
    # Prompt for title
    title = input("Enter paper title (or press Enter for default): ").strip()
    if not title:
        title = "Top 10 Countries by Citations"
    
    df = load_and_process_data(file_path)
    fig = create_plot(df, title)
    
    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf"), ("PNG files", "*.png")],
        title="Save figure as"
    )
    
    if save_path:
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Figure saved to {save_path}")
    
    plt.close()

if __name__ == "__main__":
    main()
