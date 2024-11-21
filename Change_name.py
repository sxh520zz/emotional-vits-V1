# Open the input file in read mode and output file in write mode
input_file = "/home/shixiaohan-toda/Desktop/Conferences/Interspeech_2025_EMO_TTS/emotional-vits-main/filelists/ljs_audio_text_val_filelist.txt.cleaned"  # Replace with your input file name
output_file = "/home/shixiaohan-toda/Desktop/Conferences/Interspeech_2025_EMO_TTS/emotional-vits-main/filelists/ljs_audio_text_val_filelist.txt.cleaned_1.txt"  # Replace with your output file name

# Open the input and output files
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    # Iterate through each line in the input file
    for line in infile:
        # Split the line into components using the first "|"
        parts = line.strip().split("|", 1)
        if len(parts) == 2:  # Ensure there are exactly two parts
            # Add the "0" as the second column
            new_line = f"{parts[0]}|0|{parts[1]}"
            # Write the new line to the output file
            outfile.write(new_line + "\n")