
import argparse, pandas as pd, matplotlib.pyplot as plt

def main(args):
    df = pd.read_csv(args.data)
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(subset=['Rating'])
    # clean installs
    if 'Installs' in df.columns:
        df['Installs'] = df['Installs'].astype(str).str.replace('[+,]', '', regex=True)
        df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
    # numeric price
    if 'Price' in df.columns:
        df['Price'] = df['Price'].astype(str).str.replace('$','', regex=False)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)

    summary = df.groupby('Category').agg(
        apps=('App','count'),
        avg_rating=('Rating','mean'),
        total_installs=('Installs','sum'),
        pct_paid=('Type', lambda s: (s=='Paid').mean()*100 if 'Paid' in s.values else 0)
    ).sort_values('total_installs', ascending=False)

    summary.to_csv(args.out, index=True)
    print(f"Wrote summary to {args.out}")

    # top 10 categories by installs
    top10 = summary.head(10)
    fig, ax = plt.subplots()
    top10['total_installs'].plot(kind='bar', ax=ax, title='Top 10 Categories by Installs')
    ax.set_ylabel('Installs')
    plt.tight_layout()
    fig.savefig(args.out.replace('.csv','_top10_installs.png'))
    print("Saved bar chart.")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--data', required=True)
    p.add_argument('--out', required=True)
    main(p.parse_args())
