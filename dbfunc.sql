------------------- CREATE DATABASE -------------------
CREATE EXTENSION IF NOT EXISTS dblink;
CREATE OR REPLACE FUNCTION create_db(dbname text, username text, passwd text) RETURNS void AS $$
	BEGIN
		IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'secondlaba') THEN
			PERFORM dblink_exec('user=' || username
								' password=' || passwd
								' dbname=' || current_database(),
								'CREATE DATABASE ' || dbname || ' WITH OWNER ' || username);
		END IF;
	END
$$ LANGUAGE plpgsql;


------------------- DELETE DATABASE -----------------
CREATE OR REPLACE FUNCTION drop_db(dbname text, username text, passwd text) RETURNS void AS $$
	BEGIN
		PERFORM dblink_exec(
			'user=' || username ||
			' password=' || passwd ||
			' dbname=' || current_database(),
			'DROP DATABASE IF EXISTS ' || dbname);
	END
$$ LANGUAGE plpgsql;
