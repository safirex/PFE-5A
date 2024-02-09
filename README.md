# PFE-5A
why streamlit : https://towardsdatascience.com/plotly-dash-vs-streamlit-which-is-the-best-library-for-building-data-dashboard-web-apps-97d7c98b938c


dernier df exclure/limit weekend
rajouter nom section
csv changeer nom généré
df par id show only stop choisi
df raw des stop choisis



données pleine nuit
df : nb arret par heure / arret
csv export bdd





df : attente max par stop entre 2 tram 
service on reboot/kill -9

etendue (naive)?




observ:




manque des entrées dans stop info

pfe=# select count(distinct trip_id) from rt_stop_info where arrival_time>1668236977 and stop_id like '3-1605';
 count
-------
  1964
(1 row)

pfe=# select count(distinct trip_id) from raw_rt_data where arrival_time>1668236977 and stop_id like '3-1605';
 count
-------
  2180
(1 row)

pfe=# select count(1) from raw_rt_data where arrival_time>1668236977 and stop_id like '3-1605';
 count
--------
 392146
(1 row)





pfe=# select count(distinct (trip_id,stop_id)) from rt_stop_info where arrival_time >1673420977;
 count
-------
    11
(1 row)

pfe=# select count(distinct (trip_id,stop_id)) from raw_rt_data where arrival_time >1673420977;
 count
-------
 89854

probleme pour données trip info inferieur a 1 jour ?

pfe=# select count(distinct trip_id) from rt_stop_info where arrival_time >1673420977;
 count
-------
    10
(1 row)
pfe=# select count(distinct trip_id) from raw_rt_data where arrival_time >1673420977;
 count
-------
  3597
(1 row)

select count(distinct trip_id) from raw_rt_data where arrival_time >1668150577 and arrival_time <1673420977;











select count(distinct trip_id) from raw_rt_data where arrival_time >1668150577 and arrival_time <1673420977;
             row
------------------------------
 (27-10-1-1-055900,3-10001)
 (27-10-1-1-055900,3-1204)
 (27-10-1-1-055900,3-1208)
 (27-10-1-1-055900,3-1230)
 (27-10-1-1-055900,3-1231)
 (27-10-1-1-055900,3-1243)
 (27-10-1-1-055900,3-1248)
 (27-10-1-1-055900,3-1287)
 (27-10-1-1-055900,3-1288)
 (27-10-1-1-055900,3-1344)
 (27-10-1-1-055900,3-145)
 (27-10-1-1-055900,3-146)
 (27-10-1-1-055900,3-148)
 (27-10-1-1-055900,3-149)
 (27-10-1-1-055900,3-150)
 (27-10-1-1-055900,3-151)
 (27-10-1-1-055900,3-152)
 (27-10-1-1-055900,3-153)
 (27-10-1-1-055900,3-154)
 (27-10-1-1-055900,3-155)
 (27-10-1-1-055900,3-39)
 (27-10-1-1-055900,3-40)
 (27-10-1-1-055900,3-42)
 (27-10-1-1-055900,3-43)
 (27-10-1-1-055900,3-435)



 pfe=# select distinct (trip_id,stop_id) from raw_rt_data where arrival_time >1673420977 limit 20;
            row
----------------------------
 (27-10-1-1-055900,3-10001)
 (27-10-1-1-055900,3-1204)
 (27-10-1-1-055900,3-1208)
 (27-10-1-1-055900,3-1230)
 (27-10-1-1-055900,3-1231)
 (27-10-1-1-055900,3-1243)
 (27-10-1-1-055900,3-1248)
 (27-10-1-1-055900,3-1287)
 (27-10-1-1-055900,3-1288)
 (27-10-1-1-055900,3-1344)
 (27-10-1-1-055900,3-145)
 (27-10-1-1-055900,3-146)
 (27-10-1-1-055900,3-148)
 (27-10-1-1-055900,3-149)
 (27-10-1-1-055900,3-150)
 (27-10-1-1-055900,3-151)
 (27-10-1-1-055900,3-152)
 (27-10-1-1-055900,3-153)
 (27-10-1-1-055900,3-154)
 (27-10-1-1-055900,3-155)