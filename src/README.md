# Εγκατάσταση απαιτούμενων Python πακέτων 

Για την εκτέλεση του Project, συνίσταται η χρήστη ενός `Python virtual environment`. Θα πρέπει να έχετε `python3`, `pip` και `virtualenv3`. Στην συνέχεια, εκτελέστε τις παρακάτω εντολές :

```bash
git clone https://github.com/st1069364/CarBazaar.git #clone repo
cd CarBazaar/src
python3 -m venv venv #create a Python virtual environment inside the src directory
source venv/bin/activate # source the virtenv activation script
pip3 install -r requirements.txt #install the required packages through the requirements.txt
```

# Περιγραφή δομής αρχείων

Στο αρχείο *classes.py* περιέχεται ο κώδικας των κλάσεων του Domain Model του Project. Σε πρώτη φάση, οι κλάσεις περιέχουν μόνο τα attributes.

Στον φάκελο **ui** βρίσκεται ο κώδικας του GUI.

## Φάκελος ui

To αρχείο *app_res_rc.py* αποτελεί compiled έκδοση του *qt_ui/app_res.qrc* resource file.

Τα .py αρχεία, περιέχουν τον κώδικα τον οθονών που αντιστοιχούν στο use case του αντίστοιχου ονόματος. Για παράδειγμα, το αρχείο *post_lst.py*, περιέχει τον κώδικα του Use case 'Ανάρτηση Αγγελίας Πώλησης Οχήματος'. Στην παρούσα φάση, περιέχει μόνο τον κώδικα για τις UI οθόνες, καθώς και για τις μεταβάσεις μεταξύ αυτών. Συγκεκριμένα, κάνοντας κλικ στο κουμπί 'Continue', γίνεται μετάβαση στην επόμενη οθόνη, και κάνοντας κλικ στο κουμπί 'Back', γίνεται μετάβαση στην προηγούμενη οθόνη.

Στον φάκελο *qml*, βρίσκονται τα QML αρχεία.

Στον φάκελο *qt_ui*, βρίσκονται τα .ui αρχεία που προκύπτουν από τον Qt Designer, και μέσω αυτών προκύπτουν οι υλοποιημένες με Python κώδικα, οθόνες.
Επίσης, στον φάκελο αυτό υπάρχει το .qrc αρχείο, που χρησιμοποιείται ως Qt Resource αρχείο, για την ομαδοποίηση όλων των resources.

Στον φάκελο *qt_ui/resources*, βρίσκονται τα απαραίτητα resources.

