import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from pathlib import Path

# Style setup per styleguide.md
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Charter', 'Georgia', 'DejaVu Serif', 'Times New Roman'],
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'axes.edgecolor': 'black',
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': False,
})

FILL_COLOR = '#D4C4B0'
LINE_COLOR = 'black'

# Configuration for the four papers
PAPERS = [
    {
        'file': 'QuantumCompPhot.txt',
        'title': 'Han-Sen Zhong et al.,\nQuantum computational advantage using photons',
        'output': 'quantum-computational-photons.svg',
    },
    {
        'file': 'SPDC.txt',
        'title': 'Paul G. Kwiat et al.,\nNew High-Intensity Source of Polarization-Entangled Photon Pairs',
        'output': 'polarization-entangled-photon-pairs.svg',
    },
    {
        'file': 'QSDC.txt',
        'title': 'G. L. Long and X. S. Liu,\nTheoretically efficient high-capacity quantum-key-distribution scheme',
        'output': 'qsdc-quantum-key-distribution.svg',
    },
    {
        'file': 'ExpQuantTel.txt',
        'title': 'Dik Bouwmeester et al.,\nExperimental quantum teleportation',
        'output': 'experimental-quantum-teleportation.svg',
    },
]

# Number of countries to display (reduced for readability with flags)
NUM_COUNTRIES = 8


def load_and_process_data(file_path, num_countries=NUM_COUNTRIES):
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
        'IRAN': 'Iran',
        'SCOTLAND': 'United Kingdom',
    }

    df['Country'] = df['Country'].replace(country_mappings)
    df = df.groupby('Country')['Citations'].sum().reset_index()
    df = df.sort_values('Citations', ascending=False).head(num_countries)

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
        f'https://flagcdn.com/w80/{code.lower()}.png',
        f'https://flagsapi.com/{code.upper()}/flat/64.png',
        f'https://raw.githubusercontent.com/hampusborgos/country-flags/main/png250px/{code.lower()}.png'
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                return img
        except Exception:
            continue

    print(f"Could not load flag for {country_name}")
    return None


def create_plot(df, title):
    """Create a horizontal bar chart following the style guide."""
    fig, ax = plt.subplots(figsize=(8, 5))

    # Reverse order so highest is at top
    df_plot = df.iloc[::-1].reset_index(drop=True)

    y_positions = range(len(df_plot))

    bars = ax.barh(
        y_positions,
        df_plot['Citations'],
        color=FILL_COLOR,
        edgecolor=LINE_COLOR,
        linewidth=0.8,
        height=0.7
    )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(df_plot['Country'], fontsize=10)

    # Title: left-aligned above plot
    ax.set_title(title, loc='left', fontsize=12, pad=10)

    ax.set_xlabel('Citations', fontsize=11)
    ax.tick_params(axis='x', labelsize=10)

    # Extend x-axis for flags
    xmax = max(df_plot['Citations']) * 1.20
    ax.set_xlim(0, xmax)

    # Add flags at the end of each bar
    flag_width = xmax * 0.06
    flag_offset = xmax * 0.02

    for idx, (_, row) in enumerate(df_plot.iterrows()):
        flag = get_country_flag(row['Country'])
        if flag:
            flag = flag.convert('RGB')
            flag_array = np.array(flag)

            x_pos = row['Citations'] + flag_offset
            y_pos = idx

            # Calculate flag dimensions in data coordinates
            aspect = flag_array.shape[1] / flag_array.shape[0]
            data_height = 0.5
            data_width = data_height * aspect * (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0] + 1) * 0.8

            flag_ax = ax.inset_axes([
                x_pos,
                y_pos - data_height / 2,
                data_width,
                data_height
            ], transform=ax.transData)

            flag_ax.imshow(flag_array)
            flag_ax.set_xticks([])
            flag_ax.set_yticks([])
            # Add black frame around flag
            for spine in flag_ax.spines.values():
                spine.set_visible(True)
                spine.set_color('black')
                spine.set_linewidth(0.5)

    # Attribution
    fig.text(0.02, 0.02, 'Markus Leipe (2025)', fontsize=8, color='#666666')
    fig.text(0.98, 0.02, 'Data source: Web of Science',
             fontsize=8, ha='right', color='#666666')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12, top=0.88, left=0.18, right=0.88)

    return fig


def main():
    script_dir = Path(__file__).parent

    print("Generating citation analysis plots...")
    print(f"Using style: fill={FILL_COLOR}, line={LINE_COLOR}")
    print(f"Showing top {NUM_COUNTRIES} countries per paper\n")

    for paper in PAPERS:
        file_path = script_dir / paper['file']
        output_path = script_dir / paper['output']

        print(f"Processing: {paper['file']}")

        if not file_path.exists():
            print(f"  Warning: {file_path} not found, skipping")
            continue

        df = load_and_process_data(file_path)
        fig = create_plot(df, paper['title'])

        # Save as SVG (preferred per style guide)
        fig.savefig(output_path, format='svg', bbox_inches='tight')
        print(f"  Saved: {output_path}")

        plt.close(fig)

    print("\nDone! All plots generated.")


if __name__ == "__main__":
    main()
