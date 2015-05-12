from django.db import migrations


class Migration(migrations.Migration):

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE `MySQLCache_table` (
                cache_key varchar(255) CHARACTER SET utf8 NOT NULL PRIMARY KEY,
                value longblob NOT NULL,
                value_type char(1) CHARACTER SET latin1 NOT NULL DEFAULT 'p',
                expires BIGINT UNSIGNED NOT NULL
            );
            """,
            "DROP TABLE `MySQLCache_table`;"
        ),
    ]
