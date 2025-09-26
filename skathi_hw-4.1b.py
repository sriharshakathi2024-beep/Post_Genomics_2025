import pandas as pd


orig_normal_csv = r"C:\Users\skathi\Downloads\Final_Normal.csv"
orig_tumor_csv  = r"C:\Users\skathi\Downloads\Final_Tumor.csv"
perv_normal_tsv = r"C:\Users\skathi\Downloads\Normal_pervariant.tsv"
perv_tumor_tsv  = r"C:\Users\skathi\Downloads\Tumor_pervariant.tsv"
# --------------------------

def make_key_from_original(df):
    
    key = (
        df["chrom"].astype(str).str.replace(r"^(?i:chr)", "", regex=True).str.upper().str.replace("M","MT")
        + ":" + df["left"].astype(str).str.replace(r"\.0+$","", regex=True)
        + ":" + df["ref_seq"].astype(str).str.upper().str.strip()
        + ":" + df["alt_seq"].astype(str).str.upper().str.strip()
    )
    return key

def make_key_from_pervariant(p):
    
    key = (
        p["chrom"].astype(str).str.upper().str.replace("M","MT")
        + ":" + p["position"].astype(str).str.replace(r"\.0+$","", regex=True)
        + ":" + p["ref"].astype(str).str.upper().str.strip()
        + ":" + p["alt"].astype(str).str.upper().str.strip()
    )
    return key

def merge_one(orig_csv, perv_tsv, out_csv):
    o = pd.read_csv(orig_csv, dtype=str).fillna("")
    p = pd.read_csv(perv_tsv, sep="\t", dtype=str).fillna("")

    
    o["_key"] = make_key_from_original(o)
    p["_key"] = make_key_from_pervariant(p)

    
    drop = {"id","chrom","position","ref","alt","_key"}
    add_cols = [c for c in p.columns if c not in drop]

    
    m = o.merge(p[["_key"] + add_cols], on="_key", how="left").drop(columns="_key")

    
    if "alt_seq" in m.columns:
        base = list(m.columns)
        new_order = []
        for col in base:
            new_order.append(col)
            if col == "alt_seq":
                new_order.extend([c for c in add_cols if c in base and c not in new_order])
        
        for c in add_cols:
            if c not in new_order and c in base:
                new_order.append(c)
        m = m[new_order]

    m.to_csv(out_csv, index=False)
    print("Wrote:", out_csv)


merge_one(orig_normal_csv, perv_normal_tsv, r"C:\Users\skathi\Downloads\Normal_SNP_merged.csv")
merge_one(orig_tumor_csv,  perv_tumor_tsv,  r"C:\Users\skathi\Downloads\Tumor_SNP_merged.csv")



