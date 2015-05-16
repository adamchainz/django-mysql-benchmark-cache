from django.db import migrations


class Migration(migrations.Migration):

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE `MySQLCache_Innodb_table` (
                cache_key varchar(255) CHARACTER SET utf8 COLLATE utf8_bin
                                       NOT NULL PRIMARY KEY,
                value longblob NOT NULL,
                value_type char(1) CHARACTER SET latin1 COLLATE latin1_bin
                                   NOT NULL DEFAULT 'p',
                expires BIGINT UNSIGNED NOT NULL
            );
            """,
            "DROP TABLE `MySQLCache_Innodb_table`;"
        ),
        migrations.RunSQL(
            """
            CREATE TABLE `MySQLCache_MyISAM_table` (
                cache_key varchar(255) CHARACTER SET utf8 COLLATE utf8_bin
                                       NOT NULL PRIMARY KEY,
                value longblob NOT NULL,
                value_type char(1) CHARACTER SET latin1 COLLATE latin1_bin
                                   NOT NULL DEFAULT 'p',
                expires BIGINT UNSIGNED NOT NULL
            ) ENGINE=MyISAM;
            """,
            "DROP TABLE `MySQLCache_MyISAM_table`;"
        ),
    ]
