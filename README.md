# Telugu–English Clitic Dataset

A small Streamlit page for viewing the approved Telugu–English sentence and clitic fields alongside the audio clip identified by each sentence's `Index`.

## Project files

- `app.py` displays the dataset and reads clips from the local `audio/` folder.
- `data/sentences.json` contains the exact sentence and clitic values exported from the workbook. Only rows with `swaroopa` equal to `yes` are included (case-insensitive, surrounding spaces ignored).
- `prepare_data.py` recreates that JSON from an Excel workbook using Pandas and OpenPyXL. It does not modify the workbook.
- `audio/` contains local WAV clips named `Index_EnglishSentence.wav`. The app matches only the `Index_` filename prefix.

## Run the application

Python 3.9 or newer is recommended.

1. Install the packages:

   ```powershell
   pip install -r requirements.txt
   ```

2. Ensure the authorized audio clips are in `audio/` and their filenames begin with the matching sentence index, for example `5_You_want_this.wav`.

3. Start Streamlit from this project directory:

   ```powershell
   streamlit run app.py
   ```

The app uses paths relative to its own project directory. If a clip is missing for a sentence, the card displays a message and the rest of the page remains available.

## Refresh the sentence data

To regenerate `data/sentences.json` from an Excel workbook, run:

```powershell
python prepare_data.py "C:\path\to\unique_sentences.xlsx"
```

The preparer checks the actual required column names, reads the workbook with the OpenPyXL engine, filters only on the `swaroopa` column, and writes the five requested sentence/clitic fields plus `Index`. `Semantic Match` is not used. The original workbook is read-only for this process and is not included in this repository.

## GitHub

1. Create a new repository at [github.com/new](https://github.com/new), enter `Telugu_English_Clitic_Dataset`, and choose **Public** only if the sentence data and all files you plan to publish are authorized for public distribution.
2. In this project directory, initialize and push the source:

   ```powershell
   git init
   git add app.py prepare_data.py requirements.txt README.md .gitignore data/sentences.json
   git commit -m "Add Telugu-English clitic dataset app"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/Telugu_English_Clitic_Dataset.git
   git push -u origin main
   ```

Audio files are ignored by Git by default. Do not publish copyrighted web-series audio without permission. Keep those clips local/private, or only publish clips explicitly authorized for public distribution. If you have distribution rights and intend to publish approved clips, review `.gitignore` and GitHub's file-size limits before adding them.