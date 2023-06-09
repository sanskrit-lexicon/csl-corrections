dictlo=$1
echo "BEGIN: update local installation of $dictlo"
echo "-------------------------------------------"
cd ../csl-pywork/v02
sh generate_dict.sh $dictlo  ../../$dictlo
echo "-------------------------------------------"
echo "check $dictlo.xml validity"
sh xmlchk_xampp.sh $dictlo
echo "-------------------------------------------"
echo
echo "update csl-orig for $dictlo user corrections"
cd ../../csl-orig
git add v02/$dictlo/$dictlo.txt
git commit -m "$dictlo: User correction(s)"
echo "push csl-orig to github"
git push
echo
echo "-------------------------------------------"
echo "DONE: update local installation of $dictlo"
