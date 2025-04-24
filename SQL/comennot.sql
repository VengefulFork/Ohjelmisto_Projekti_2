Käytettiin pohjana sieltä moodlen aivan lopusta löytyvää tiedostoa joka luo ainoastaan taulut airport ja country 
Tehtiin sillä uusi tietokanta jonka nimi on peli_projekti 

Alempi lähinnä helpottamaan tietokanta yhteyden luomista. 	
CREATE USER player IDENTIFIED BY '12345'
GRANT SELECT, INSERT, UPDATE ON peli_projekti.* TO player;

Tästä alaspäin on kaikki tietokannan muokkaamiseen käytetyt komennot
Joitakin kenttien nimissä olevia kirjoitusvirheitä korjasimme HEIDISQL:n GUI:n kautta.

Turhien kenttien poistaminen 
DELETE FROM airport 

WHERE ident NOT IN ("EFHK", "EFKT", "ESSA", "ENGM", "ENTC", "BIKF", "EGPD", "EGLL", "LFPG", "LEMD",
                   "LIRF", "LSZH", "EDDB", "EPWA", "EKBI", "EVRA", "LOWW", "LRBS", "LQSA", "LGAV", "EHAM")
				   
Uusi taulu joka sisältää kenttien väliset yhteydet 

create table yhteys (
ID int not null auto_increment,
aloituspiste varchar(40) NOT NULL,
lopetuspiste varchar(40) NOT NULL, 
primary key (ID),
foreign key (aloituspiste) REFERENCES airport(ident),
foreign key (lopetuspiste) REFERENCES airport(ident)

)ENGINE=InnoDB DEFAULT CHARSET=latin1;

Kenttien väliset yhteydet 

insert into yhteys (aloituspiste, lopetuspiste)
values ("EFHK", "ESSA"), ("EFHK", "ENGM"),("EFHK", "EFKT"), ("EFKT", "ENTC"),("ESSA", "ENGM"), ("BIKF", "ENTC"), ("BIKF", "EGLL"), ("BIKF", "EGPD"), ("EGLL", "LFPG"), 
		("EGPD", "ENGM"), ("LFPG", "LEMD"), ("LEMD", "LIRF"), ("LIRF", "LSZH"), ("LSZH", "EDDB"), ("EDDB", "EPWA"), ("EPWA", "EVRA"), ("EKBI", "ESSA"), ("EKBI", "EDDB"),
		("EVRA", "ENTC"), ("LOWW", "LSZH"), ("LOWW", "LQSA"), ("LOWW", "LRBS"), ("LRBS", "LQSA"), ("LGAV", "LIRF"), ("LGAV", "LEMD"), ("EHAM", "EGLL"), ("EHAM", "LFPG") ; 
		
insert into yhteys (aloituspiste, lopetuspiste)
values ("LQSA", "LGAV"), ("LRBS", "EPWA"), ("EKBI", "EHAM") ;  

Toinen uusi taulu joka sisältää edellisten pelien tiedot 

create table edelliset_pelit (
	ID int not null auto_increment,
	pelaajan_nimi varchar(40) NOT NULL,
	aloitus_kentta varchar(40) NOT NULL,
	maali varchar(40) NOT NULL,
	kuljettu_matka_km int not null,
	matkan_aika_min int not null, 
	tuotettu_co2_kg int not null, 
	pisteet int not null,
	primary key (ID)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;
		







