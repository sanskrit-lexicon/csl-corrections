# Download app/correction_response/cfr.tsv from Cologne server
sh download_cfr.sh
Note: This first step is not ideal.
Reason: Cannot push csl-corrections from cologne server to Github.
------------
# edit cfr.tsv and remove 'bad lines'
 -- e.g. incomplete or hacker garbage)
------------------------------------
sh redo_cfr.sh
  This analyzes the 'new' items in cfr.tsv and marks
  in the relevant 'dictionaries/xxx/xxx_correctionform.txt files]
  Note: there may be 'bad line' messages.
    Edit cfr.tsv and either delete or revise the bad lines.
    rerun redo_cfr.sh

------------------------------------

Our task will be to
(a) make changes in local  cfr.tsv for pending items
    This may take one or more days to do!
(b) git add, commit, push local
(c) login to cologne and navigate to scans/csl-corrections/
(d) There may be new lines in cfr.tsv.
    Handle these in local version
    At cologne, git restore app/correction_response/cfr.tsv
(3) At cologne, git pull.
-----------------------------------------------
a. Get a new personal access token at Github
b. Modify /c/Users/<WINDOWS-USER/.bashrc
c. restart git bash and navigate back to csl-corrections
----------------------------------------------
sh post_github_issues.sh
   1. This creates issues at github.com/sanskrit-lexicon/csl-orig for
      pending items
      It modifies file 'last_cfr_line.txt'
      Prints messages: "uploaded issue pw:37314"  for each issue.
   2. There can only be about 20 at a time.  When this limit is exceeded,
      a '403' error will be posted:
      "Error posting: requests status =  403"
   3a. wait a few seconds (maybe a minute), and redo 1.
   3b. Keep doing this all are issues are initialized (no 403 message).
----------------------------------------------
corrections for mw
------------------
emacs: edit dictionaries/mw_correctionform.txt
emacs: edit csl-orig/v02/mw/mw.txt
browser: edit https://github.com/sanskrit-lexicon/csl-orig/issues
For each mw pending issue:
  make appropriate change in mw.txt
  mark cfr.tsv (in last field) add ':06-05-2023 corrected'
  If email given, add message to 'temp_replies.txt', copying from
    mw_correctionform.txt.  (see below for format of temp_replies.txt)
  When all 'mw' items resolved, again run 'sh redo_cfr.sh'.
Continue the above until all dictionaries with user submissions are handled.
------------------------------------------------------------
Do local installations.
At this point, we have changed csl-orig/v02/xxx/xxx.txt for all
 dictionaries with new user-submissions.
 Rerunning 'sh redo_cfr.sh' should show '0 cases are pending'
Make a list of those dictionaries (e.g. via 'git status' in csl-orig'.)
For each revised dictionary, remake the local version amd update csl-orig

# assume in local csl-corrections
sh update_user_corrections.sh ae
This does:
cd ../csl-pywork/v02
sh generate_dict.sh ae  ../../ae
sh xmlchk_xampp.sh ae
cd ../../csl-orig
git add v02/ae/ae.txt
git commit -m "ae: User correction(s)"
git push

sh update_user_corrections.sh ae # done
sh update_user_corrections.sh ap90 # done
sh update_user_corrections.sh bur # done
sh update_user_corrections.sh gra # done
sh update_user_corrections.sh md # done
sh update_user_corrections.sh mw # done
sh update_user_corrections.sh mwe # done
sh update_user_corrections.sh pw # done
sh update_user_corrections.sh pwg # done
sh update_user_corrections.sh skd # done
sh update_user_corrections.sh stc # done
sh update_user_corrections.sh vcp # done
sh update_user_corrections.sh wil # done

---------------------------------------------------
# update cologne
# login to cologne via ssh
cd ***csl-orig***
git pull
cd ../csl-pywork/v02
git pull # if csl-pywork has been modified
# remake all dictionaries changed

sh generate_dict.sh ae ../../AEScan/2020/ # done
sh generate_dict.sh ap90 ../../AP90Scan/2020/ # done
sh generate_dict.sh bur ../../BURScan/2020/ # done
sh generate_dict.sh gra ../../GRAScan/2020/ # done
sh generate_dict.sh md ../../MDScan/2020/ # done
sh generate_dict.sh mw ../../MWScan/2020/ # done
sh generate_dict.sh mwe ../../MWEScan/2020/ # done
sh generate_dict.sh pw ../../PWScan/2020/ # done
sh generate_dict.sh pwg ../../PWGScan/2020/ # done
sh generate_dict.sh skd ../../SKDScan/2020/ # done
sh generate_dict.sh stc ../../STCScan/2020/ # done
sh generate_dict.sh vcp ../../VCPScan/2020/ # done
sh generate_dict.sh wil ../../WILScan/2020/ # done
------------------------------------------------------
Send replies to users for their correction submissions.
See user_thankyou_sample.txt for the 'form letter' format.
During the correction phase,  update a TEMPORARY file
temp_replies.txt for all the form letters.
 (temporary, since we don't want the email addresses to be published on web.
When all the corrections have been installed on cologne,
the various form letter thankyou letters should be sent by email to the users.
-----------------------------------------------------
update of csl-corrections repository
This is complicated because I could not do an
initial push of the cologne repository to Github. (authentication problem).
1. Edit the cologne cfr.tsv file.
   Edit the local cfr.tsv file
   Go to bottom of both files.
   If there are any 'new' corrections not included in local cfr.tsv,
     then copy/paste these extra lines from cologne cfr.tsv to local cfr.tsv.
   These will be corrected at a future time.
   Save the local cfr.tsv, as amended.
   close the cologne cfr.tsv (no change to that file in editor.
2. Use putty to login to cologne
   cd to csl-corrections
   git restore app/correction_response/cfr.tsv
3. sync local copy of csl-corrections to github
     cd csl-corrections # local
     git add .
     git commit -m "update user corrections"
     git push
4. sync cologne copy of csl-corrections to github
    cd csl-corrections # cologne
    git pull
----------------------------------------------------
That's it.
Now we're ready for the next handling of user corrections.
---------------------------------------------------

