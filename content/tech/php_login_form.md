Date: 2017-06-30 14:35
Title: PHP User Login
Description: Tutorial on how to manage users with PHP and MySQL/MariaDB
Tags: mysql php tutorial sql mariadb
Slug: php_user_logins

[TOC]

### Before we start
Managing user accounts is a extremely difficult thing to do correctly, so if you think you need to register and maintain a list of users for your site stop and think whether that's really the case. There's a number of ways to allow third parties to manage all of the responsibility for you and to have them authenticate users for you. [Facebook](https://developers.facebook.com/docs/facebook-login/web), [Google](https://developers.google.com/identity/sign-in/web/), [Twitter](https://dev.twitter.com/web/sign-in) and [Microsoft](https://msdn.microsoft.com/en-us/library/bb676633.aspx) all offer options whereby users can authenticate with them and you receive a token verifying the login. Alternatively if all you want is verified users for a comment section on your site, then a third-party service like [disqus](https://disqus.com/) is by far the best option. If really you want to manage comments yourself have users login via a third-party.

Having a user account for creating content on your site is one thing, having accounts for random people on the internet opens you up to a whole range of headaches; so let someone else do it for you. If you still think that user accounts and management is what you need then the rest of this post will describe how to do that. As with all things; I've made this as accurate and secure as possible at the time of writing.

### What we'll use
We'll be making use of [PHP](http://www.php.net/) and [MariaDB](https://mariadb.com/) in this tutorial, the installation of both of these is outside the scope of this post. If you haven't already setup a server then [xampp](https://www.apachefriends.org/index.html) is an easy to setup Apache, PHP and MySQL/MariaDB stack that you can use for local development and testing. We'll be using PHP version 7.0.x and MariaDB version 10.1.x.

### Setup of MariaDB
You'll need to connect to MariaDB as the `root` user so that we can create a database for our sites information and a user responsible for managing it. So if you've setup the database to have a password for the root user you'd run: `mysql -u root -p`

Once connected, simply create the database using:
```sql
CREATE DATABASE mysite CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

This will create a new empty database and set the character set to utf8mb4. Now that we've got the database we need to create the user that will have permissions on it. To create a new user we'll need to run:

```sql
CREATE USER 'my_user'@'localhost' IDENTIFIED BY 'my_password';
GRANT ALL ON mysite.* TO 'my_user'@'localhost';
FLUSH PRIVILEGES;
```

This will create a new user account, called `my_user` with a password of `my_password`. Once that's happen we grant all privileges for that user to every (`*`) table within the `mysite` database. Privileges are actions we want the user to be able to perform, for example we could create a read-only user for the site and just give that user `SELECT` privileges by using `GRANT SELECT ...` instead. Finally we reload the new permissions by calling `FLUSH`.

Now that we've created our user, exit the MariaDB prompt so we can begin creating the tables required.

### Creating Tables
Our users are going to have certain information stored about them; this includes the user name, the password and contact email address, all of which are required. Optionally we're going to store the first and family name of the user. To give us a little more control over what users can and can't do on our site we'll have the concept of roles. We'll create the following tables to store all of this information in, you can either run this SQL directly into MariaDB using the prompt or place it into a SQL script to run in the commands.

```sql
CREATE TABLE mysite.roles(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(50) NOT NULL
);
INSERT INTO mysite.roles(role) VALUES('admin'), ('user'), ('commenter');

CREATE TABLE mysite.users(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    family_name VARCHAR(255)
);
```

### Database Access
Database access will be via PHPs [PDO](http://ch1.php.net/manual/en/book.pdo.php), mainly because of the number of supported databases and the ease of migration to another database server in future if required.

The configuration for the database will be stored within a `config.inc.php` script:
```
<?php
    DEFINE('DB_TYPE', 'mysql');
    DEFINE('DB_HOST', 'localhost');
    DEFINE('DB_NAME', 'mysite');
    DEFINE('DB_USER', 'my_user');
    DEFINE('DB_PASS', 'my_password');
?>
```

To contain the database access for the users, we're going to create a new `class` to handle all of the interactions called `UserDAL`. We'll be added functions to this call through the tutorial, but the initial class will be:
```
<?php
require_once('config.inc.php');

class UserDAL {
    private $db = null;

    public function __construct() {
        try {
            $this->db = new PDO(DB_TYPE.':host='.DB_HOST.';dbname='.DB_NAME.';charset=utf8mb4', DB_USER, DB_PASS);
        } catch (PDOException $e) {
            print "Error: " . $e->getMessage() . "<br />";
            die();
        }
        $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
}
?>
```

### Creating Users
Each user is going to have a password stored with their accounts, we're going to do the following things for these passwords:

* Use a cryptographically strong hashing function
* Require strong passwords, we're going to define a strong password as one containing a minimum of 8 characters and have at least 3 of the following 4 rules:
    * Upper case letters
    * Lower case letters
    * Numbers
    * Symbols
* Place no limit on the upper number of characters allowed

To check to see if a user has entered a strong password; we'll make use of the following `user_funcs.php` script.
```
DEFINE('MIN_PASSWD_LEN', 8);
DEFINE('NUMBER_REGEX', '/[0-9]+/');
DEFINE('UPPER_CASE_REGEX', '/[A-Z]+/');
DEFINE('LOWER_CASE_REGEX', '/[a-z]+/');
DEFINE('SPECIAL_CHAR_REGEX', "/\W+/");

function password_strength_check($password, &$errors) {
    $inital_errors = $errors;

    echo "password = $password";
    if (strlen($password) < MIN_PASSWD_LEN) {
        $errors[] = "Password needs a minimum of " . MIN_PASSWD_LEN . " characters.";
    }

    if (!preg_match(NUMBER_REGEX, $password)) {
        $errors[] = "Password requires at least one number";
    }

    if (!preg_match(UPPER_CASE_REGEX, $password)) {
        $errors[] = "Password requires at least one upper case letter";
    }

    if (!preg_match(LOWER_CASE_REGEX, $password)) {
        $errors[] = "Password requires at least one lower case letter";
    }

    if (!preg_match(SPECIAL_CHAR_REGEX, $password)) {
        $errors[] = "Password much include at least one symbol";
    }

    return ($errors == $inital_errors);
}
```

Now that we're happy with the strength of our password we need to hash it securely, we'll do this using the [password_hash](http://php.net/manual/en/function.password-hash.php) function which creates a strong one-way hash, PHP will take care of creating a new salt for each hash. We'll be generating the hash using the Blowfish algorithm. Assuming our plain text password is stored in the `$password` variable we simply run:

```
$hashed_password = password_hash($password, PASSWORD_BCRYPT);
```

This is then simply verified by using the [password_verify](http://php.net/manual/en/function.password-verify.php) function, fro example if the password we wanted to store was in `$password` and the hash stored in `$passwd_hash` we'd run:

```
if (password_verify($password, $passwd_hash)) {
    echo "Password matches!";
} else {
    echo "Invalid password";
}
```