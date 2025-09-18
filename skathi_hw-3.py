import pandas as pd

# === Manually list Normal CSVs ===
normal_files = [
    r"C:\Users\skathi\Downloads\Normal_files\file1_normal.csv",
    r"C:\Users\skathi\Downloads\Normal_files\file2_normal.csv",
    r"C:\Users\skathi\Downloads\Normal_files\file3_normal.csv",
    r"C:\Users\skathi\Downloads\Normal_files\file4_normal.csv",
    r"C:\Users\skathi\Downloads\Normal_files\file5_normal.csv"
]

# === Manually list Tumor CSVs ===
tumor_files = [
    r"C:\Users\skathi\Downloads\Tumor_files\file1_tumor.csv",
    r"C:\Users\skathi\Downloads\Tumor_files\file2_tumor.csv",
    r"C:\Users\skathi\Downloads\Tumor_files\file3_tumor.csv",
    r"C:\Users\skathi\Downloads\Tumor_files\file4_tumor.csv",
    r"C:\Users\skathi\Downloads\Tumor_files\file5_tumor.csv"
]

# === A(i): Merge CSVs ===
Normal_df = pd.concat([pd.read_csv(f) for f in normal_files], ignore_index=True)
Tumor_df  = pd.concat([pd.read_csv(f) for f in tumor_files],  ignore_index=True)


def addALT_Seq(csv):
    alt = []
    for row in range(csv.shape[0]):
        ref_seq = csv["ref_seq"][row]
        if ref_seq == csv["var_seq1"][row]:
            alt.append(csv["var_seq2"][row])
        else:
            alt.append(csv["var_seq1"][row])
    csv.insert(csv.shape[1], "alt_seq", alt)
    return csv

Normal_df = addALT_Seq(Normal_df)
Tumor_df  = addALT_Seq(Tumor_df)



dedup_cols = ["chrom", "left", "ref_seq", "alt_seq", "Patient_ID"]
Final_Normal = Normal_df.drop_duplicates(subset=dedup_cols).reset_index(drop=True)
Final_Tumor  = Tumor_df.drop_duplicates(subset=dedup_cols).reset_index(drop=True)


Final_Tumor  = Final_Tumor.drop(columns=["Unnamed: 0"], errors="ignore")
Final_Normal = Final_Normal.drop(columns=["Unnamed: 0"], errors="ignore")


Final_Normal.to_csv(r"C:\Users\skathi\Downloads\Final_Normal.csv", index=False)
Final_Tumor.to_csv(r"C:\Users\skathi\Downloads\Final_Tumor.csv", index=False)


print("The number of (Rows, Columns) in Tumor:", Final_Tumor.shape)
print("The number of (Rows, Columns) in Normal:", Final_Normal.shape)



