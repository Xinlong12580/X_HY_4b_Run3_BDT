files=" "

while IFS= read -r line; do
    files=$files" "$line
done < 2024__MC_TTBarJets__TTto4Q_reduced.txt
echo $files
hadd all_ttbar.root $files
 

