# cuntoir
Progressive To-do web app with a vanilla Javascript front-end, a Python back-end and a MySQL database

To get it up and running you'll need to provide key files for ssl, web push notifications and stripe, or else rip out the stripe 
payment integration. You'll also need to set up a mysql database called "fin" with the following tables, and a file called "pass.conf"
containing the password for a MySQL user, alse called "fin", who has full usage of the "fin" database. Another file called dbHosts.conf
should contain the address of the MySQL database host, with fallbacks appended after the primary database.


Database tables (MySQL "show tables;"):


+---------------+

| Tables_in_fin |

+---------------+

| authCodes     |

| duePushes     |

| pushInfo      |

| stripe        |

| tasks         |

| users         |

+---------------+


"describe authCodes;"


+------------+---------+------+-----+---------+----------------+

| Field      | Type    | Null | Key | Default | Extra          |

+------------+---------+------+-----+---------+----------------+

| id         | int(11) | NO   | PRI | NULL    | auto_increment |

| username   | text    | NO   |     | NULL    |                |

| authCode   | text    | NO   |     | NULL    |                |

| createTime | double  | NO   |     | NULL    |                |

+------------+---------+------+-----+---------+----------------+


"describe duePushes;"


+----------+---------+------+-----+---------+----------------+

| Field    | Type    | Null | Key | Default | Extra          |

+----------+---------+------+-----+---------+----------------+

| id       | int(11) | NO   | PRI | NULL    | auto_increment |

| title    | text    | NO   |     | NULL    |                |

| username | text    | NO   |     | NULL    |                |

| pushTime | double  | NO   |     | NULL    |                |

| text     | text    | NO   |     | NULL    |                |

| taskId   | int(11) | NO   |     | NULL    |                |

+----------+---------+------+-----+---------+----------------+


"describe pushInfo;"


+------------+---------+------+-----+---------+----------------+

| Field      | Type    | Null | Key | Default | Extra          |

+------------+---------+------+-----+---------+----------------+

| id         | int(11) | NO   | PRI | NULL    | auto_increment |

| username   | text    | NO   |     | NULL    |                |

| subString  | text    | NO   |     | NULL    |                |

| lastReturn | text    | NO   |     | NULL    |                |

+------------+---------+------+-----+---------+----------------+


"describe stripe;"


+----------+---------+------+-----+---------+----------------+

| Field    | Type    | Null | Key | Default | Extra          |

+----------+---------+------+-----+---------+----------------+

| id       | int(11) | NO   | PRI | NULL    | auto_increment |

| stripeId | text    | NO   |     | NULL    |                |

| email    | text    | NO   |     | NULL    |                |

| username | text    | NO   |     | NULL    |                |

| subId    | text    | NO   |     | NULL    |                |

+----------+---------+------+-----+---------+----------------+


"describe tasks;"


+-------------------+----------+------+-----+---------+----------------+

| Field             | Type     | Null | Key | Default | Extra          |

+-------------------+----------+------+-----+---------+----------------+

| id                | int(11)  | NO   | PRI | NULL    | auto_increment |

| username          | text     | NO   |     | NULL    |                |

| createTime        | double   | NO   |     | NULL    |                |

| dueTime           | double   | NO   |     | NULL    |                |

| text              | longtext | NO   |     | NULL    |                |

| done              | text     | NO   |     | NULL    |                |

| title             | text     | NO   |     | NULL    |                |

| tags              | text     | NO   |     | NULL    |                |

| pushScheduled     | text     | NO   |     | NULL    |                |

| notificationHours | int(11)  | NO   |     | NULL    |                |

| recurring         | text     | NO   |     | NULL    |                |

+-------------------+----------+------+-----+---------+----------------+


"describe users;"


+------------+---------+------+-----+---------+----------------+

| Field      | Type    | Null | Key | Default | Extra          |

+------------+---------+------+-----+---------+----------------+

| id         | int(11) | NO   | PRI | NULL    | auto_increment |

| username   | text    | NO   |     | NULL    |                |

| pass       | text    | NO   |     | NULL    |                |

| sendPushes | text    | YES  |     | NULL    |                |

| premium    | text    | NO   |     | NULL    |                |

+------------+---------+------+-----+---------+----------------+


I'm afraid you'll have to create these tables yourself if you want to self-host, right now I haven't built a setup utility.
On the other hand, feel free to fork this repo and write one, or submit a pr.

You'll need an empty file called "invite.conf", which you can fill with an invite code if you want to stop random signups, or leave
empty to allow anyone to register. Your web-push keys go into repo/pushKeys, as private_key.pem and public_key.pem, and your ssl keys
go in repo/ssl as cert.pem, chain.pem and priv.key. Your stripe private key goes into repo/stripeKeys as stripe.key, the public key is
"hard-coded" in line 29 of repo/static/upgrade.html

Enjoy!
