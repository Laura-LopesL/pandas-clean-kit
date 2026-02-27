import argparse
import pandas as pd

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--in', dest='inp', required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()

    df = pd.read_csv(a.inp)
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    for col in ['amount', 'price', 'quantity']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.to_parquet(a.out, index=False)
    print('OK ->', a.out)

if __name__ == '__main__':
    main()
