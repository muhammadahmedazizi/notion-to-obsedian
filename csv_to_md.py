import os
import pandas as pd
from collections import defaultdict

def convert_csvs_to_markdown(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(input_dir, file)
            try:
                df = pd.read_csv(file_path)

                # Normalize column names
                df.columns = [col.strip().lower() for col in df.columns]

                # Flexible column detection
                name_col = next((col for col in df.columns if col in ['name', 'title']), None)
                url_col = next((col for col in df.columns if col in ['url', 'link', 'source', 'href']), None)
                tag_col = next((col for col in df.columns if 'tag' in col), None)
                date_col = next((col for col in df.columns if 'date' in col), None)
                type_col = next((col for col in df.columns if col in ['type', 'category', 'section']), None)
                parent_url_col = next((col for col in df.columns if 'parent' in col and 'url' in col), None)

                print(f"Columns found in {file}: {df.columns.tolist()}")

                if not name_col:
                    print(f"Skipping {file} — name/title column not found.")
                    continue

                df[tag_col] = df[tag_col].fillna('') if tag_col else ''
                df[date_col] = df[date_col].fillna('') if date_col else ''
                df[type_col] = df[type_col].fillna('Misc') if type_col else 'Misc'

                grouped_entries = defaultdict(list)
                parent_url = df[parent_url_col].iloc[0] if parent_url_col and pd.notna(df[parent_url_col].iloc[0]) else None

                for _, row in df.iterrows():
                    name = row[name_col] if name_col else 'Untitled'
                    url = row[url_col] if url_col and pd.notna(row[url_col]) else None
                    tags = ', '.join([f"`{tag.strip()}`" for tag in str(row[tag_col]).split(',') if tag.strip()]) if tag_col else ''
                    date = row[date_col] if date_col and pd.notna(row[date_col]) else ''
                    section = row[type_col] if type_col and pd.notna(row[type_col]) else 'Misc'

                    # Build the markdown entry
                    if url:
                        entry = f"- **{name}**  \n  [View]({url})"
                    else:
                        entry = f"- **{name}**"

                    if tags:
                        entry += f" — Tags: {tags}"
                    if date:
                        entry += f" — Date: {date}"

                    grouped_entries[section].append(entry)

                md_lines = []
                if parent_url:
                    md_lines.append(f"## 🔗 Inspirations from [Design Scrapbook]({parent_url})\n")
                else:
                    md_lines.append("## 🔗 Inspirations\n")

                for section, entries in grouped_entries.items():
                    md_lines.append(f"### 🗂️ {section}")
                    md_lines.extend(entries)
                    md_lines.append("")

                output_file_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.md")
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(md_lines))

                print(f"✅ Processed: {file} → {output_file_path}")
            except Exception as e:
                print(f"⚠️ Error processing {file}: {e}")

# Example usage placeholder (you can uncomment and edit this to test)
# convert_csvs_to_markdown("your_input_directory", "your_output_directory")
# Example usage placeholder (won't run here directly)
convert_csvs_to_markdown("D:\PIAIC\PIAIC-PROJECTS\\notion-to-obsedian\exported-csv-files", "D:\PIAIC\PIAIC-PROJECTS\\notion-to-obsedian\output-data2")

