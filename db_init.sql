INSERT INTO user(username,password) VALUES('user12','sha256$UIyE0yoI$a89f5cac2c7431b1a4a62dc6c1d5e83c41683a7f1e4efe7a64a2ceb239dc02bd');
INSERT INTO user(username,password) VALUES('user13','sha256$UIyE0yoI$a89f5cac2c7431b1a4a62dc6c1d5e83c41683a7f1e4efe7a64a2ceb239dc02bd');

INSERT INTO band(id,user_id,name,rating,tags,url, state) VALUES(1,1,'Metallica',1.0,'','', 1);
INSERT INTO band(id,user_id,name,rating,tags,url, state) VALUES(2,1,'The Rolling Stones',0.5,'','', 1);
INSERT INTO band(id,user_id,name,rating,tags,url, state) VALUES(1,2,'Lady Gaga',1.0,'','', 1);

INSERT INTO band(id,user_id,name,rating,tags,url, state) VALUES(1,1,'Tsjuder',1.0,'','', 2);
INSERT INTO band(id,user_id,name,rating,tags,url, state) VALUES(2,1,'Behemoth',0.5,'','', 2);
