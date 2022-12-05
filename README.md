# Anomaly Detection
Running the docker :

first enter the StreamlitApp directory and enter the next commands:

1.pipenv install streamlit pandas

2.pipenv shell

3.pipenv requirements > requirements.txt // dont run this command we already made this file.

4.sudo docker build -t mystapp:latest .

5.sudo docker run -p 8501:8501 mystapp:latest 

After entering this commands you should have the docker built and deployed.

Confusion Matrix:

We thought we just needed to create a csv with 3 columns , record ID | ALGORITHM RESULT | LABLED GIVEN RESULT | ERROR

ERROR is if the algorithm result didn't match the labled given result.

result.csv:

a csv with the results of our algorithm , same structure as the labled csv.



