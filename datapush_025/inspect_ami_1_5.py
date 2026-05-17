import os

def dump_folder_contents(input_folder, output_file):

    with open(output_file, "w", encoding="utf-8") as out:

        for root, dirs, files in os.walk(input_folder):

            for file in files:

                file_path = os.path.join(root, file)

                out.write("\n" + "="*100 + "\n")
                out.write(f"FILE: {file}\n")
                out.write(f"PATH: {file_path}\n")
                out.write("="*100 + "\n\n")

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        out.write(content)
                        out.write("\n\n")

                except Exception as e:
                    out.write(f"ERROR reading file: {e}\n\n")

    print(f"\n✅ Dump completed → {output_file}")


if __name__ == "__main__":

    # 🔹 CHANGE THIS PATH FOR DIFFERENT FOLDERS

    input_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\datasets\AMI automatic annotations v1.5.1\PlainText-format\ExtractiveSummaries"

    output_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\output_topics_1.txt"

    dump_folder_contents(input_path, output_path)