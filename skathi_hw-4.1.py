import pandas as pd
import re

# Read both input files
final_normal = pd.read_csv(r"C:\Users\skathi\Downloads\Final_Normal.csv")
final_tumor  = pd.read_csv(r"C:\Users\skathi\Downloads\Final_Tumor.csv")


final_normal["Sample_Type"] = "Normal"
final_tumor["Sample_Type"]  = "Tumor"
merged = pd.concat([final_normal, final_tumor], ignore_index=True)


variant_cols = ["chrom", "left", "ref_seq", "alt_seq"]
variants = merged[variant_cols + ["Sample_Type"]].copy()


CHR_PREFIX = re.compile(r"^(?i:chr)")

def clean_id(x):
    """Return chromosome ID without 'chr' prefix (1..22, X, Y, MT)."""
    s = str(x).strip()
    s = CHR_PREFIX.sub("", s)        # remove chr/CHR
    s = "MT" if s.upper() in {"M","MT"} else s  # normalize M -> MT
    return s

def to_int_pos(v):
    s = str(v).strip()
    # allow '12345.0' → 12345
    if re.fullmatch(r"\d+(\.0+)?", s):
        return int(float(s))
    return int(s)

def build_table(df, strand_value):
    """
    Produce columns with EXACT names:
      type, ID, position, Allele 1, Allele 2, strand
    - type: literal 'chromosome'
    - ID: chrom without 'chr'
    - position: left (int)
    - Allele 1: ref_seq (upper)
    - Allele 2: alt_seq (upper)
    - strand: '1' or '-1'
    """
    out = pd.DataFrame({
        "type": "chromosome",                                   # literal as requested
        "ID": df["chrom"].apply(clean_id),
        "position": df["left"].apply(to_int_pos),
        "Allele 1": df["ref_seq"].astype(str).str.strip().str.upper(),
        "Allele 2": df["alt_seq"].astype(str).str.strip().str.upper(),
        "strand": str(strand_value)
    })
    return out[["type","ID","position","Allele 1","Allele 2","strand"]]

# Split back by sample type, then build four outputs
normal_df = variants[variants["Sample_Type"] == "Normal"][variant_cols].copy()
tumor_df  = variants[variants["Sample_Type"] == "Tumor"][variant_cols].copy()

normal_positive_strand = build_table(normal_df, "1")
normal_negative_strand = build_table(normal_df, "-1")
tumor_positive_strand  = build_table(tumor_df,  "1")
tumor_negative_strand  = build_table(tumor_df,  "-1")

# Write as TSV (tabs). Set header=True since you want those column names.
normal_positive_strand.to_csv(r"C:\Users\skathi\Downloads\normal_positive_strand.tsv",
                              sep="\t", index=False, header=True)
normal_negative_strand.to_csv(r"C:\Users\skathi\Downloads\normal_negative_strand.tsv",
                              sep="\t", index=False, header=True)
tumor_positive_strand.to_csv(r"C:\Users\skathi\Downloads\tumor_positive_strand.tsv",
                             sep="\t", index=False, header=True)
tumor_negative_strand.to_csv(r"C:\Users\skathi\Downloads\tumor_negative_strand.tsv",
                             sep="\t", index=False, header=True)

print("Wrote 4 TSVs to Downloads.")





