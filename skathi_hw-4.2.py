import pandas as pd
import re


snp_normal = r"C:\Users\skathi\Downloads\Normal_SNP_merged.csv"
snp_tumor  = r"C:\Users\skathi\Downloads\Tumor_SNP_merged.csv"
fxf_normal = r"C:\Users\skathi\Downloads\Fathm_normal.txt"
fxf_tumor  = r"C:\Users\skathi\Downloads\Fathm_tumor.txt"
out_normal = r"C:\Users\skathi\Downloads\Normal_FATHMM_merged.csv"
out_tumor  = r"C:\Users\skathi\Downloads\Tumor_FATHMM_merged.csv"


def make_key(chrom, pos, ref, alt):
    chrom = str(chrom).replace("chr", "").upper().replace("M","MT")
    pos   = str(pos).split(".")[0]
    return f"{chrom}:{pos}:{ref}:{alt}"

def merge_one(snp_csv, fxf_txt, out_csv):
    snp = pd.read_csv(snp_csv, dtype=str).fillna("")
    fxf = pd.read_csv(fxf_txt, sep="\t", dtype=str).fillna("")

    
    fxf = fxf.rename(columns=lambda x: x.strip())

    
    snp["_KEY_"] = snp.apply(lambda r: make_key(r["chrom"], r["left"], r["ref_seq"], r["alt_seq"]), axis=1)
    fxf["_KEY_"] = fxf.apply(lambda r: make_key(r["# Chromosome"], r["Position"], r["Ref. Base"], r["Mutant Base"]), axis=1)

    
    add_cols = [c for c in fxf.columns if c not in ["# Chromosome","Position","Ref. Base","Mutant Base","_KEY_"]]

    merged = snp.merge(fxf[["_KEY_"] + add_cols], on="_KEY_", how="left").drop(columns="_KEY_")

    
    merged.to_csv(out_csv, index=False)
    print("Wrote:", out_csv)


merge_one(snp_normal, fxf_normal, out_normal)
merge_one(snp_tumor,  fxf_tumor,  out_tumor)




