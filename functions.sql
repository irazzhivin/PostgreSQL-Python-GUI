
------------------- UPDATE factory -------------------
CREATE OR REPLACE FUNCTION 
	update_factory(p_id integer, new_name text, new_foundation_date date, new_address text, new_car_number integer) 
RETURNS void AS $$
BEGIN
	UPDATE factorys
	SET name = new_name,
		foundation_date = new_foundation_date,
		address = new_address,
		car_number = new_car_number
	WHERE id = p_id;
END
$$ LANGUAGE plpgsql;


------------------- UPDATE car -------------------
CREATE OR REPLACE FUNCTION 
	update_car(p_id integer, new_name text, new_year integer, new_factory_id integer) 
RETURNS void AS $$
BEGIN
	UPDATE cars
	SET name = new_name,
		year = new_year,
		factory_id = new_factory_id
	WHERE id = p_id;
END
$$ LANGUAGE plpgsql;


------------------- DELETE factory BY ID -------------------
CREATE OR REPLACE FUNCTION delete_factory(p_id integer) 
RETURNS void AS $$
BEGIN
	DELETE FROM factorys
	WHERE id = p_id;
END
$$ LANGUAGE plpgsql;


------------------- DELETE car BY ID -------------------
CREATE OR REPLACE FUNCTION delete_car(f_id integer) 
RETURNS void AS $$
BEGIN
	DELETE FROM cars
	WHERE id = f_id;
END
$$ LANGUAGE plpgsql;


------------------- DELETE factory BY NAME -------------------
CREATE OR REPLACE FUNCTION delete_factorys_by_name(name_to_find text) 
RETURNS void AS $$
BEGIN
	DELETE FROM factorys
	WHERE name = name_to_find;
END
$$ LANGUAGE plpgsql;


------------------- DELETE car BY name -------------------
CREATE OR REPLACE FUNCTION delete_cars_by_name(name_to_find text) 
RETURNS void AS $$
BEGIN
	DELETE FROM cars
	WHERE name = name_to_find;
END
$$ LANGUAGE plpgsql;


------------------- FIND factory -------------------
CREATE OR REPLACE FUNCTION find_factorys(name_to_find text) 
RETURNS TABLE(id integer, name text, foundation_date date, address text, car_number integer) 
AS $func$
BEGIN
	RETURN QUERY
	SELECT * FROM factorys p
	WHERE p.name = name_to_find;
END
$func$ LANGUAGE plpgsql;


------------------- FIND car -------------------
CREATE OR REPLACE FUNCTION find_cars(name_to_find text) 
RETURNS TABLE(id integer, name text, year integer, factory_id integer) 
AS $func$
BEGIN
	RETURN QUERY
	SELECT * FROM cars f
	WHERE f.name = name_to_find;
END
$func$ LANGUAGE plpgsql;


------------------- INSERT factory -------------------
CREATE OR REPLACE FUNCTION insert_factory(p_id integer, name text, foundation_date date, address text, car_number integer)
RETURNS void AS $$
BEGIN
	INSERT INTO factorys VALUES
	(p_id, name, foundation_date, address, (SELECT COUNT(*) FROM cars f WHERE f.factory_id = p_id))
	ON CONFLICT DO NOTHING; 
END
$$ LANGUAGE plpgsql;


------------------- INSERT car -------------------
CREATE OR REPLACE FUNCTION insert_car(id integer, name text, year integer, factory_id integer) 
RETURNS void AS $$
BEGIN
	INSERT INTO cars VALUES
	(id, name, year, factory_id)
	ON CONFLICT DO NOTHING; 
END
$$ LANGUAGE plpgsql;


------------------- DELETE ALL factory -------------------
CREATE OR REPLACE FUNCTION delete_all_factorys() 
RETURNS void AS $$
BEGIN
	DELETE FROM factorys;
END
$$ LANGUAGE plpgsql;


------------------- DELETE ALL car -------------------
CREATE OR REPLACE FUNCTION delete_all_cars() 
RETURNS void AS $$
BEGIN
	DELETE FROM cars;
END
$$ LANGUAGE plpgsql;


------------------- SELECT ALL factory -------------------
CREATE OR REPLACE FUNCTION get_factorys() 
RETURNS TABLE(id integer, name text, foundation_date date, address text, car_number integer) 
AS $func$
BEGIN
	RETURN QUERY
	SELECT * FROM factorys;
END
$func$ LANGUAGE plpgsql;


------------------- SELECT ALL car -------------------
CREATE OR REPLACE FUNCTION get_cars() 
RETURNS TABLE(id integer, name text, year integer, factory_id integer) 
AS $func$
BEGIN
	RETURN QUERY
	SELECT * FROM cars;
END
$func$ LANGUAGE plpgsql;


------------------- TRIGGER FUNCTION -------------------
CREATE OR REPLACE FUNCTION update_number() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE factorys
			SET car_number = (SELECT COUNT(*) FROM cars f WHERE f.factory_id = NEW.factory_id)
			WHERE id = NEW.factory_id;
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
		UPDATE factorys
			SET car_number = (SELECT COUNT(*) FROM cars f WHERE f.factory_id = OLD.factory_id)
			WHERE id = OLD.factory_id;
		UPDATE factorys
			SET car_number = (SELECT COUNT(*) FROM cars f WHERE f.factory_id = NEW.factory_id)
			WHERE id = NEW.factory_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
		UPDATE factorys
			SET car_number = (SELECT COUNT(*) FROM cars f WHERE f.factory_id = OLD.factory_id)
			WHERE id = OLD.factory_id;
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;


------------------- CREATE TABLES -----------------
CREATE OR REPLACE FUNCTION create_tables(dbname text, username text, passwd text) RETURNS void AS $$
	BEGIN
			CREATE TABLE factorys(
			id integer PRIMARY KEY,
			name text NOT NULL,
			foundation_date date NOT NULL,
			address text NOT NULL,
			car_number integer NOT NULL DEFAULT 0
			);

			CREATE TABLE cars(
			id integer PRIMARY KEY,
			name text NOT NULL,
			year integer NOT NULL,
			factory_id integer NOT NULL);

			CREATE INDEX on cars(name);
			CREATE INDEX on factorys(name);

			CREATE TRIGGER car_number_updater
			AFTER INSERT OR UPDATE OR DELETE ON
				cars FOR EACH ROW EXECUTE PROCEDURE update_number();
	END
$$ LANGUAGE plpgsql;