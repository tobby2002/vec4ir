
/***********************************************************************************
    Author: Daniel Bouchard
    Date:   Nov. 18th, 2017

    Notes:
	   This is an adaptation of the mysql script key_abbreviations_english.sql for TSQL
***********************************************************************************/

-- Create Table

DROP TABLE IF EXISTS 
     dbo.key_abbreviations_english;

CREATE TABLE dbo.key_abbreviations_english (
    id INT IDENTITY(1,1) PRIMARY KEY,
    a  VARCHAR(255) NOT NULL,
    b  INT NOT NULL,
    p  BIT NOT NULL
           DEFAULT 0,
);

-- Add comments

EXEC sp_addextendedproperty 
     @name = N'Description',
     @value = 'A table mapping book abbreviations to the book they refer to',
     @level0type = N'Schema',
     @level0name = 'dbo',
     @level1type = N'Table',
     @level1name = 'key_abbreviations_english';

EXEC sp_addextendedproperty 
     @name = N'Description',
     @value = 'Abbreviation ID',
     @level0type = N'Schema',
     @level0name = 'dbo',
     @level1type = N'Table',
     @level1name = 'key_abbreviations_english',
     @level2type = N'Column',
     @level2name = 'id';

EXEC sp_addextendedproperty 
     @name = N'Description',
     @value = 'ID of book that is abbreviated',
     @level0type = N'Schema',
     @level0name = 'dbo',
     @level1type = N'Table',
     @level1name = 'key_abbreviations_english',
     @level2type = N'Column',
     @level2name = 'b';

EXEC sp_addextendedproperty 
     @name = N'Description',
     @value = 'Whether an abbreviation is the primary one for the book',
     @level0type = N'Schema',
     @level0name = 'dbo',
     @level1type = N'Table',
     @level1name = 'key_abbreviations_english',
     @level2type = N'Column',
     @level2name = 'p';

-- Insert Data

SET IDENTITY_INSERT dbo.key_abbreviations_english ON;

INSERT INTO dbo.key_abbreviations_english (
       id,
       a,
       b,
       p
) 
VALUES (
       1,'Gen',1,1
 ), (
       2,'Ge',1,0
 ), (
       3,'Gn',1,0
 ), (
       4,'Exo',2,1
 ), (
       5,'Ex',2,0
 ), (
       6,'Exod',2,0
 ), (
       7,'Lev',3,1
 ), (
       8,'Le',3,0
 ), (
       9,'Lv',3,0
 ), (
       10,'Num',4,1
 ), (
       11,'Nu',4,0
 ), (
       12,'Nm',4,0
 ), (
       13,'Nb',4,0
 ), (
       14,'Deut',5,1
 ), (
       15,'Dt',5,0
 ), (
       16,'Josh',6,1
 ), (
       17,'Jos',6,0
 ), (
       18,'Jsh',6,0
 ), (
       19,'Judg',7,1
 ), (
       20,'Jdg',7,0
 ), (
       21,'Jg',7,0
 ), (
       22,'Jdgs',7,0
 ), (
       23,'Rth',8,1
 ), (
       24,'Ru',8,0
 ), (
       25,'1 Sam',9,1
 ), (
       26,'1 Sa',9,0
 ), (
       27,'1Samuel',9,0
 ), (
       28,'1S',9,0
 ), (
       29,'I Sa',9,0
 ), (
       30,'1 Sm',9,0
 ), (
       31,'1Sa',9,0
 ), (
       32,'I Sam',9,0
 ), (
       33,'1Sam',9,0
 ), (
       34,'I Samuel',9,0
 ), (
       35,'1st Samuel',9,0
 ), (
       36,'First Samuel',9,0
 ), (
       37,'2 Sam',10,1
 ), (
       38,'2 Sa',10,0
 ), (
       39,'2S',10,0
 ), (
       40,'II Sa',10,0
 ), (
       41,'2 Sm',10,0
 ), (
       42,'2Sa',10,0
 ), (
       43,'II Sam',10,0
 ), (
       44,'2Sam',10,0
 ), (
       45,'II Samuel',10,0
 ), (
       46,'2Samuel',10,0
 ), (
       47,'2nd Samuel',10,0
 ), (
       48,'Second Samuel',10,0
 ), (
       49,'1 Kgs',11,1
 ), (
       50,'1 Ki',11,0
 ), (
       51,'1K',11,0
 ), (
       52,'I Kgs',11,0
 ), (
       53,'1Kgs',11,0
 ), (
       54,'I Ki',11,0
 ), (
       55,'1Ki',11,0
 ), (
       56,'I Kings',11,0
 ), (
       57,'1Kings',11,0
 ), (
       58,'1st Kgs',11,0
 ), (
       59,'1st Kings',11,0
 ), (
       60,'First Kings',11,0
 ), (
       61,'First Kgs',11,0
 ), (
       62,'1Kin',11,0
 ), (
       63,'2 Kgs',12,1
 ), (
       64,'2 Ki',12,0
 ), (
       65,'2K',12,0
 ), (
       66,'II Kgs',12,0
 ), (
       67,'2Kgs',12,0
 ), (
       68,'II Ki',12,0
 ), (
       69,'2Ki',12,0
 ), (
       70,'II Kings',12,0
 ), (
       71,'2Kings',12,0
 ), (
       72,'2nd Kgs',12,0
 ), (
       73,'2nd Kings',12,0
 ), (
       74,'Second Kings',12,0
 ), (
       75,'Second Kgs',12,0
 ), (
       76,'2Kin',12,0
 ), (
       77,'1 Chron',13,1
 ), (
       78,'1 Ch',13,0
 ), (
       79,'I Ch',13,0
 ), (
       80,'1Ch',13,0
 ), (
       81,'1 Chr',13,0
 ), (
       82,'I Chr',13,0
 ), (
       83,'1Chr',13,0
 ), (
       84,'I Chron',13,0
 ), (
       85,'1Chron',13,0
 ), (
       86,'I Chronicles',13,0
 ), (
       87,'1Chronicles',13,0
 ), (
       88,'1st Chronicles',13,0
 ), (
       89,'First Chronicles',13,0
 ), (
       90,'2 Chron',14,1
 ), (
       91,'2 Ch',14,0
 ), (
       92,'II Ch',14,0
 ), (
       93,'2Ch',14,0
 ), (
       94,'II Chr',14,0
 ), (
       95,'2Chr',14,0
 ), (
       96,'II Chron',14,0
 ), (
       97,'2Chron',14,0
 ), (
       98,'II Chronicles',14,0
 ), (
       99,'2Chronicles',14,0
 ), (
       100,'2nd Chronicles',14,0
 ), (
       101,'Second Chronicles',14,0
 ), (
       102,'Ezra',15,1
 ), (
       103,'Ezr',15,0
 ), (
       104,'Neh',16,1
 ), (
       105,'Ne',16,0
 ), (
       106,'Esth',17,1
 ), (
       107,'Es',17,0
 ), (
       108,'Job',18,1
 ), (
       109,'Job',18,0
 ), (
       110,'Jb',18,0
 ), (
       111,'Pslm',19,1
 ), (
       112,'Ps',19,0
 ), (
       113,'Psalms',19,0
 ), (
       114,'Psa',19,0
 ), (
       115,'Psm',19,0
 ), (
       116,'Pss',19,0
 ), (
       117,'Prov',20,1
 ), (
       118,'Pr',20,0
 ), (
       119,'Prv',20,0
 ), (
       120,'Eccles',21,1
 ), (
       121,'Ec',21,0
 ), (
       122,'Qoh',21,0
 ), (
       123,'Qoheleth',21,0
 ), (
       124,'Song',22,1
 ), (
       125,'So',22,0
 ), (
       126,'Canticle of Canticles',22,0
 ), (
       127,'Canticles',22,0
 ), (
       128,'Song of Songs',22,0
 ), (
       129,'SOS',22,0
 ), (
       130,'Isa',23,1
 ), (
       131,'Is',23,0
 ), (
       132,'Jer',24,1
 ), (
       133,'Je',24,0
 ), (
       134,'Jr',24,0
 ), (
       135,'Lam',25,1
 ), (
       136,'La',25,0
 ), (
       137,'Ezek',26,1
 ), (
       138,'Eze',26,0
 ), (
       139,'Ezk',26,0
 ), (
       140,'Dan',27,1
 ), (
       141,'Da',27,0
 ), (
       142,'Dn',27,0
 ), (
       143,'Hos',28,1
 ), (
       144,'Ho',28,0
 ), (
       145,'Joel',29,1
 ), (
       146,'Joe',29,0
 ), (
       147,'Jl',29,0
 ), (
       148,'Amos',30,1
 ), (
       149,'Am',30,0
 ), (
       150,'Obad',31,1
 ), (
       151,'Ob',31,0
 ), (
       152,'Jnh',32,1
 ), (
       153,'Jon',32,0
 ), (
       154,'Micah',33,1
 ), (
       155,'Mic',33,0
 ), (
       156,'Nah',34,1
 ), (
       157,'Na',34,0
 ), (
       158,'Hab',35,1
 ), (
       159,'Zeph',36,1
 ), (
       160,'Zep',36,0
 ), (
       161,'Zp',36,0
 ), (
       162,'Haggai',37,1
 ), (
       163,'Hag',37,0
 ), (
       164,'Hg',37,0
 ), (
       165,'Zech',38,1
 ), (
       166,'Zec',38,0
 ), (
       167,'Zc',38,0
 ), (
       168,'Mal',39,1
 ), (
       169,'Mal',39,0
 ), (
       170,'Ml',39,0
 ), (
       171,'Matt',40,1
 ), (
       172,'Mt',40,0
 ), (
       173,'Mrk',41,1
 ), (
       174,'Mk',41,0
 ), (
       175,'Mr',41,0
 ), (
       176,'Luk',42,1
 ), (
       177,'Lk',42,0
 ), (
       178,'John',43,1
 ), (
       179,'Jn',43,0
 ), (
       180,'Jhn',43,0
 ), (
       181,'Acts',44,1
 ), (
       182,'Ac',44,0
 ), (
       183,'Rom',45,1
 ), (
       184,'Ro',45,0
 ), (
       185,'Rm',45,0
 ), (
       186,'1 Cor',46,1
 ), (
       187,'1 Co',46,0
 ), (
       188,'I Co',46,0
 ), (
       189,'1Co',46,0
 ), (
       190,'I Cor',46,0
 ), (
       191,'1Cor',46,0
 ), (
       192,'I Corinthians',46,0
 ), (
       193,'1Corinthians',46,0
 ), (
       194,'1st Corinthians',46,0
 ), (
       195,'First Corinthians',46,0
 ), (
       196,'2 Cor',47,1
 ), (
       197,'2 Co',47,0
 ), (
       198,'II Co',47,0
 ), (
       199,'2Co',47,0
 ), (
       200,'II Cor',47,0
 ), (
       201,'2Cor',47,0
 ), (
       202,'II Corinthians',47,0
 ), (
       203,'2Corinthians',47,0
 ), (
       204,'2nd Corinthians',47,0
 ), (
       205,'Second Corinthians',47,0
 ), (
       206,'Gal',48,1
 ), (
       207,'Ga',48,0
 ), (
       208,'Ephes',49,1
 ), (
       209,'Eph',49,0
 ), (
       210,'Phil',50,1
 ), (
       211,'Php',50,0
 ), (
       212,'Col',51,1
 ), (
       213,'Col',51,0
 ), (
       214,'1 Thess',52,1
 ), (
       215,'1 Th',52,0
 ), (
       216,'I Th',52,0
 ), (
       217,'1Th',52,0
 ), (
       218,'I Thes',52,0
 ), (
       219,'1Thes',52,0
 ), (
       220,'I Thess',52,0
 ), (
       221,'1Thess',52,0
 ), (
       222,'I Thessalonians',52,0
 ), (
       223,'1Thessalonians',52,0
 ), (
       224,'1st Thessalonians',52,0
 ), (
       225,'First Thessalonians',52,0
 ), (
       226,'2 Thess',53,1
 ), (
       227,'2 Th',53,0
 ), (
       228,'II Th',53,0
 ), (
       229,'2Th',53,0
 ), (
       230,'II Thes',53,0
 ), (
       231,'2Thes',53,0
 ), (
       232,'II Thess',53,0
 ), (
       233,'2Thess',53,0
 ), (
       234,'II Thessalonians',53,0
 ), (
       235,'2Thessalonians',53,0
 ), (
       236,'2nd Thessalonians',53,0
 ), (
       237,'Second Thessalonians',53,0
 ), (
       238,'1 Tim',54,1
 ), (
       239,'1 Ti',54,0
 ), (
       240,'I Ti',54,0
 ), (
       241,'1Ti',54,0
 ), (
       242,'I Tim',54,0
 ), (
       243,'1Tim',54,0
 ), (
       244,'I Timothy',54,0
 ), (
       245,'1Timothy',54,0
 ), (
       246,'1st Timothy',54,0
 ), (
       247,'First Timothy',54,0
 ), (
       248,'2 Tim',55,1
 ), (
       249,'2 Ti',55,0
 ), (
       250,'II Ti',55,0
 ), (
       251,'2Ti',55,0
 ), (
       252,'II Tim',55,0
 ), (
       253,'2Tim',55,0
 ), (
       254,'II Timothy',55,0
 ), (
       255,'2Timothy',55,0
 ), (
       256,'2nd Timothy',55,0
 ), (
       257,'Second Timothy',55,0
 ), (
       258,'Titus',56,1
 ), (
       259,'Tit',56,0
 ), (
       260,'Philem',57,1
 ), (
       261,'Phm',57,0
 ), (
       262,'Hebrews',58,1
 ), (
       263,'Heb',58,0
 ), (
       264,'James',59,1
 ), (
       265,'Jas',59,0
 ), (
       266,'Jm',59,0
 ), (
       267,'1 Pet',60,1
 ), (
       268,'1 Pe',60,0
 ), (
       269,'I Pe',60,0
 ), (
       270,'1Pe',60,0
 ), (
       271,'I Pet',60,0
 ), (
       272,'1Pet',60,0
 ), (
       273,'I Pt',60,0
 ), (
       274,'1 Pt',60,0
 ), (
       275,'1Pt',60,0
 ), (
       276,'I Peter',60,0
 ), (
       277,'1Peter',60,0
 ), (
       278,'1st Peter',60,0
 ), (
       279,'First Peter',60,0
 ), (
       280,'2 Pet',61,1
 ), (
       281,'2 Pe',61,0
 ), (
       282,'II Pe',61,0
 ), (
       283,'2Pe',61,0
 ), (
       284,'II Pet',61,0
 ), (
       285,'2Pet',61,0
 ), (
       286,'II Pt',61,0
 ), (
       287,'2 Pt',61,0
 ), (
       288,'2Pt',61,0
 ), (
       289,'II Peter',61,0
 ), (
       290,'2Peter',61,0
 ), (
       291,'2nd Peter',61,0
 ), (
       292,'Second Peter',61,0
 ), (
       293,'1 John',62,1
 ), (
       294,'1 Jn',62,0
 ), (
       295,'I Jn',62,0
 ), (
       296,'1Jn',62,0
 ), (
       297,'I Jo',62,0
 ), (
       298,'1Jo',62,0
 ), (
       299,'I Joh',62,0
 ), (
       300,'1Joh',62,0
 ), (
       301,'I Jhn',62,0
 ), (
       302,'1 Jhn',62,0
 ), (
       303,'1Jhn',62,0
 ), (
       304,'I John',62,0
 ), (
       305,'1John',62,0
 ), (
       306,'1st John',62,0
 ), (
       307,'First John',62,0
 ), (
       308,'2 John',63,1
 ), (
       309,'2 Jn',63,0
 ), (
       310,'II Jn',63,0
 ), (
       311,'2Jn',63,0
 ), (
       312,'II Jo',63,0
 ), (
       313,'2Jo',63,0
 ), (
       314,'II Joh',63,0
 ), (
       315,'2Joh',63,0
 ), (
       316,'II Jhn',63,0
 ), (
       317,'2 Jhn',63,0
 ), (
       318,'2Jhn',63,0
 ), (
       319,'II John',63,0
 ), (
       320,'2John',63,0
 ), (
       321,'2nd John',63,0
 ), (
       322,'Second John',63,0
 ), (
       323,'3 John',64,1
 ), (
       324,'3 Jn',64,0
 ), (
       325,'III Jn',64,0
 ), (
       326,'3Jn',64,0
 ), (
       327,'III Jo',64,0
 ), (
       328,'3Jo',64,0
 ), (
       329,'III Joh',64,0
 ), (
       330,'3Joh',64,0
 ), (
       331,'III Jhn',64,0
 ), (
       332,'3 Jhn',64,0
 ), (
       333,'3Jhn',64,0
 ), (
       334,'III John',64,0
 ), (
       335,'3John',64,0
 ), (
       336,'3rd John',64,0
 ), (
       337,'Third John',64,0
 ), (
       338,'Jude',65,1
 ), (
       339,'Jud',65,0
 ), (
       340,'Rev',66,1
 ), (
       341,'Re',66,0
 ), (
       342,'The Revelation',66,0
 ), (
       343,'Genesis',1,1
 ), (
       344,'Exodus',2,1
 ), (
       345,'Leviticus',3,1
 ), (
       346,'Numbers',4,1
 ), (
       347,'Deuteronomy',5,1
 ), (
       348,'Joshua',6,1
 ), (
       349,'Judges',7,1
 ), (
       350,'Ruth',8,1
 ), (
       351,'1 Samuel',9,1
 ), (
       352,'2 Samuel',10,1
 ), (
       353,'1 Kings',11,1
 ), (
       354,'2 Kings',12,1
 ), (
       355,'1 Chronicles',13,1
 ), (
       356,'2 Chronicles',14,1
 ), (
       357,'Ezra',15,1
 ), (
       358,'Nehemiah',16,2
 ), (
       359,'Esther',17,2
 ), (
       360,'Job',18,1
 ), (
       361,'Psalms',19,1
 ), (
       362,'Psalm',19,1
 ), (
       363,'Proverbs',20,1
 ), (
       364,'Ecclesiastes',21,1
 ), (
       365,'Song of Solomon',22,1
 ), (
       366,'Isaiah',23,1
 ), (
       367,'Jeremiah',24,1
 ), (
       368,'Lamentations',25,1
 ), (
       369,'Ezekiel',26,1
 ), (
       370,'Daniel',27,1
 ), (
       371,'Hosea',28,1
 ), (
       372,'Joel',29,1
 ), (
       373,'Amos',30,1
 ), (
       374,'Obadiah',31,1
 ), (
       375,'Jonah',32,1
 ), (
       376,'Micah',33,1
 ), (
       377,'Nahum',34,1
 ), (
       378,'Habakkuk',35,1
 ), (
       379,'Zephaniah',36,1
 ), (
       380,'Haggai',37,1
 ), (
       381,'Zechariah',38,1
 ), (
       382,'Malachi',39,1
 ), (
       383,'Matthew',40,1
 ), (
       384,'Mark',41,1
 ), (
       385,'Luke',42,1
 ), (
       386,'John',43,1
 ), (
       387,'Acts',44,1
 ), (
       388,'Romans',45,1
 ), (
       389,'1 Corinthians',46,1
 ), (
       390,'2 Corinthians',47,1
 ), (
       391,'Galatians',48,1
 ), (
       392,'Ephesians',49,1
 ), (
       393,'Philippians',50,1
 ), (
       394,'Colossians',51,1
 ), (
       395,'1 Thessalonians',52,1
 ), (
       396,'2 Thessalonians',53,1
 ), (
       397,'1 Timothy',54,1
 ), (
       398,'2 Timothy',55,1
 ), (
       399,'Titus',56,1
 ), (
       400,'Philemon',57,1
 ), (
       401,'Hebrews',58,1
 ), (
       402,'James',59,1
 ), (
       403,'1 Peter',60,1
 ), (
       404,'2 Peter',61,1
 ), (
       405,'1 John',62,1
 ), (
       406,'2 John',63,1
 ), (
       407,'3 John',64,1
 ), (
       408,'Jude',65,1
 ), (
       409,'Revelation',66,1
 );

SET IDENTITY_INSERT dbo.key_abbreviations_english OFF;
