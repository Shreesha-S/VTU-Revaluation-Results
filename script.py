import requests
from bs4 import BeautifulSoup

for year in ["14", "13", "12", "11"]:
    for branch in ["CS", "IS","EC", "ME"]:
        for i in range (1, 200):
            try:
                # Store the USN
                usn = '1PE'+year+branch+str(i).zfill(3)
                data_file = open('Reval-Data', 'a')
                print "Processing... Look for the file `Reval-Data.txt` for the results."
                
                # Store the request payload to be sent to the VTU servers
                payload = {'rid':usn, 'submit':'SUBMIT'}
                response = requests.post("http://results.vtu.ac.in/vitavireval.php", data=payload)
                
                count = 0
                string = ""

                """ Take into consideration only those lines in the source page...
                    ... which contains the results and store it as single string.
                """
                for line in response.iter_lines():
                    if line[0:5] == '</TR>' and count > 0:
                        break
                    elif line[0:3] == '<B>' or count > 0:
                        strin = str(line)
                        string = string + strin
                        count += 1

                soup = BeautifulSoup(string)
                # Write the Name and USN of the student
                data_file.write(soup.find_all("b")[0].string.strip())
                data_file.write("\n")
                # Ignore strings like "Semester", "Result", "Total", etc
                county = -10
                soupy = soup.find_all("td")
                for i in soupy:
                    county += 1 
                    try:
                        if (county > 1):
                            # Write the subject name/code and marks to the file.
                            data_file.write("    ")
                            data_file.write(i.string.strip())
                            data_file.write("\n")
                    except:
                        pass
            except:
                pass
